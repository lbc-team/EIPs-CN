---
eip: 2
title: Homestead 硬分叉变更
author: Vitalik Buterin (@vbuterin)
status: Final
type: Standards Track
category: Core
created: 2015-11-15
---

### 元参考

[Homestead](./eip-606.md).

### 参数

|   FORK_BLKNUM   | CHAIN_NAME  |
|-----------------|-------------|
|    1,150,000    | Main net    |
|   494,000       | Morden      |
|    0            | Future testnets    |

# 规范

如果 `block.number >= HOMESTEAD_FORK_BLKNUM`，执行以下操作：

1. *通过交易创建合约*的 gas 成本从 21,000 增加到 53,000，即如果您发送一笔交易并且 to 地址是空字符串，则最初扣除的 gas 是 53,000 加上交易数据的 gas 成本，而不是像目前情况下的 21,000。 从使用 `CREATE` 操作码的合约创建合约不受影响。
2. 所有 s 值大于 `secp256k1n/2` 的交易签名现在都被认为是无效的。 ECDSA 恢复预编译合约保持不变，并将继续接受高 s 值； 例如，如果合约恢复旧的比特币签名，这将非常有用。
3. 如果合约创建没有足够的 gas 来支付将合约代码添加到状态的最终 gas 费用，则合约创建将失败（即，耗尽 gas ），而不是留下一个空合约。
4. 将难度调整算法从当前公式更改为：`block_diff = parent_diff + parent_diff // 2048 * (1 if block_timestamp - parent_timestamp < 13 else -1) + int(2**((block.number // 100000) - 2))`（其中 `int(2**((block.number // 100000) - 2))` 表示指数难度调整分量）更改为 `block_diff = parent_diff + parent_diff // 2048 * max(1 - (block_timestamp - parent_timestamp) // 10, -99) + int(2**((block.number // 100000) - 2))`，其中 `//` 是整数除法运算符，例如 `6 // 2 = 3`，`7 // 2 = 3`，`8 // 2 = 4`。`minDifficulty` 仍然定义允许的最小难度，并且任何调整都不能使其低于此值。

# 理由

目前，通过交易创建合约存在过度的激励，其成本为 21,000，而不是合约创建，其成本为 32,000。 此外，在自杀退款的帮助下，目前仅使用 11,664 gas 即可进行简单的以太币价值转移。 执行此操作的代码如下：

```python
from ethereum import tester as t
> from ethereum import utils
> s = t.state()
> c = s.abi_contract('def init():\n suicide(0x47e25df8822538a8596b28c637896b4d143c351e)', endowment=10**15)
> s.block.get_receipts()[-1].gas_used
11664
> s.block.get_balance(utils.normalize_address(0x47e25df8822538a8596b28c637896b4d143c351e))
1000000000000000
```
这不是一个特别严重的问题，但可以说是一个 bug。

允许任何 s 值的交易 `0 < s < secp256k1n`，就像目前的情况一样，会引发交易可延展性问题，因为可以将任何交易的 s 值从 `s` 翻转到 `secp256k1n - s`，翻转 v 值（`27 -> 28`，`28 -> 27`），并且生成的签名仍然有效。 这不是一个严重的安全缺陷，特别是由于 Ethereum 使用地址而不是交易哈希作为以太币价值转移或其他交易的输入，但这仍然会造成 UI 不便，因为攻击者可能会导致在区块中确认的交易的哈希值与任何用户发送的交易的哈希值不同，从而干扰使用交易哈希作为跟踪 ID 的用户界面。 阻止高 s 值可以消除此问题。

如果 gas 不足以支付最终 gas 费用，则使合约创建耗尽 gas 具有以下好处：
- (i) 它在合约创建过程的结果中创建了一个更直观的“成功或失败”的区别，而不是当前的“成功、失败或空合约”三歧；
- (ii) 使故障更容易检测，因为除非合约创建完全成功，否则根本不会创建合约帐户；以及
- (iii) 在存在捐赠的情况下，使合约创建更安全，因为可以保证整个启动过程发生或交易失败并且捐赠被退还。

难度调整更改最终解决了以太坊协议两个月前遇到的问题，当时过多的矿工挖掘包含时间戳等于 `parent_timestamp + 1` 的区块； 这扭曲了区块时间分布，因此当前区块时间算法以 13 秒的*中位数*为目标，继续以相同的中位数为目标，但平均值开始增加。 如果 51% 的矿工开始以这种方式挖掘区块，那么平均值将增加到无穷大。 拟议的新公式大致基于以平均值为目标； 可以证明，在使用中的公式下，从长远来看，平均区块时间长于 24 秒在数学上是不可能的。

使用 `(block_timestamp - parent_timestamp) // 10` 作为主要输入变量（而不是直接的时间差）有助于保持算法的粗粒度性质，防止过度激励将时间戳差设置为正好为 1，以便创建一个难度略高的区块，从而保证击败任何可能的分叉。 -99 的上限只是为了确保如果由于客户端安全错误或其他黑天鹅问题导致两个区块在时间上相距太远，难度不会急剧下降。

# 实现

这在 Python 中实现如下：

1. https://github.com/ethereum/pyethereum/blob/d117c8f3fd93359fc641fd850fa799436f7c43b5/ethereum/processblock.py#L130
2. https://github.com/ethereum/pyethereum/blob/d117c8f3fd93359fc641fd850fa799436f7c43b5/ethereum/processblock.py#L129
3. https://github.com/ethereum/pyethereum/blob/d117c8f3fd93359fc641fd850fa799436f7c43b5/ethereum/processblock.py#L304
4. https://github.com/ethereum/pyethereum/blob/d117c8f3fd93359fc641fd850fa799436f7c43b5/ethereum/blocks.py#L42