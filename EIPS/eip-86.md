---
eip: 86
title: 交易发起者和签名的抽象
author: Vitalik Buterin (@vbuterin)
type: Standards Track
category: Core
status: Stagnant
created: 2017-02-10
---

# 摘要

实现了一系列更改，这些更改共同实现了“抽象出”签名验证和 nonce 检查的目的，允许用户创建“账户合约”，该合约执行任何所需的签名/nonce 检查，而不是使用当前硬编码到交易处理中的机制。

# 参数

* METROPOLIS_FORK_BLKNUM：待定
* CHAIN_ID：与 EIP 155 使用的相同（即，主网为 1，测试网为 3）
* NULL_SENDER：2**160 - 1

# 规范

如果 `block.number >= METROPOLIS_FORK_BLKNUM`，则：
1. 如果交易的签名是 `(CHAIN_ID, 0, 0)`（即 `r = s = 0`，`v = CHAIN_ID`），则将其视为有效，并将发送者地址设置为 `NULL_SENDER`
2. 此形式的交易必须具有 gasprice = 0，nonce = 0，value = 0，并且不增加账户 NULL_SENDER 的 nonce。
3. 在 `0xfb` 处创建一个新的操作码 `CREATE2`，带有 4 个堆栈参数(value, salt, mem_start, mem_size)，它将创建地址设置为 `sha3(sender + salt + sha3(init code)) % 2**160`，其中 `salt` 始终表示为 32 字节的值。
4. 将以下规则添加到_所有_合约创建操作中，包括交易和操作码：如果该地址的合约已存在且具有非空代码或非空 nonce，则该操作将失败并返回 0，就像初始化代码已耗尽 gas 一样。 如果一个账户有空代码和 nonce，但有非空余额，则创建操作仍然可以成功。

# 理由

这些更改的目标是为账户安全抽象奠定基础。 我们不采用协议内机制，将 ECDSA 和默认的 nonce 方案奉为保护帐户的唯一“标准”方式，而是朝着一个长期模型迈出初步步骤，在该模型中，所有帐户都是合约，合约可以支付 gas，并且用户可以自由定义自己的安全模型。

在 EIP 86 下，我们可以期望用户将其以太币存储在合约中，其代码可能如下所示（Serpent 示例）：

```python
# Get signature from tx data
# 从交易数据中获取签名
sig_v = ~calldataload(0)
sig_r = ~calldataload(32)
sig_s = ~calldataload(64)
# Get tx arguments
# 获取交易参数
tx_nonce = ~calldataload(96)
tx_to = ~calldataload(128)
tx_value = ~calldataload(160)
tx_gasprice = ~calldataload(192)
tx_data = string(~calldatasize() - 224)
~calldataload(tx_data, 224, ~calldatasize())
# Get signing hash
# 获取签名哈希
signing_data = string(~calldatasize() - 64)
~mstore(signing_data, tx.startgas)
~calldataload(signing_data + 32, 96, ~calldatasize() - 96)
signing_hash = sha3(signing_data:str)
# Perform usual checks
# 执行通常的检查
prev_nonce = ~sload(-1)
assert tx_nonce == prev_nonce + 1
assert self.balance >= tx_value + tx_gasprice * tx.startgas
assert ~ecrecover(signing_hash, sig_v, sig_r, sig_s) == <pubkey hash here>
# Update nonce
# 更新 nonce
~sstore(-1, prev_nonce + 1)
# Pay for gas
# 支付 gas
~send(MINER_CONTRACT, tx_gasprice * tx.startgas)
# Make the main call
# 进行主要的调用
~call(msg.gas - 50000, tx_to, tx_value, tx_data, len(tx_data), 0, 0)
# Get remaining gas payments back
# 取回剩余的 gas 支付
~call(20000, MINER_CONTRACT, 0, [msg.gas], 32, 0, 0)
```

这可以被认为是一个“转发合约”。 它接受来自“入口点”地址 2**160 - 1（任何人都可以从中发送交易的帐户）的数据，期望数据的格式为 `[sig, nonce, to, value, gasprice, data]`。 转发合约验证签名，如果签名正确，它会设置对矿工的支付，然后使用提供的值和数据向所需地址发送调用。

它提供的优势在于最有趣的情况：

- **多重签名钱包**：目前，从多重签名钱包发送需要每个操作都得到参与者的批准，并且每个批准都是一个交易。 可以通过让一个批准交易包括来自其他参与者的签名来简化此过程，但即便如此，它仍然会引入复杂性，因为参与者的帐户都需要储备 ETH。 通过此 EIP，只需让合约存储 ETH，将包含所有签名的交易直接发送到合约，合约就可以支付费用。
- **环签名混币器**：环签名混币器的工作方式是 N 个人将 1 个币发送到合约中，然后使用可链接的环签名稍后提取 1 个币。 可链接的环签名确保提款交易无法链接到存款，但如果有人试图提取两次，则可以链接这两个签名并阻止第二个签名。 但是，目前存在隐私风险：要提款，您需要有币来支付 gas，如果这些币没有正确混合，则您可能会损害您的隐私。 通过此 EIP，您可以直接用您提取的币支付 gas。
- **自定义密码学**：用户可以升级到 ed25519 签名、Lamport 哈希阶梯签名或他们想要的任何其他方案，他们不需要坚持使用 ECDSA。
- **非密码学修改**：用户可以要求交易具有到期时间（这将成为标准，可以安全地从状态中清除旧的空/灰尘帐户），使用 k-并行化 nonce（一种允许稍微乱序确认交易的方案，从而减少交易间的依赖性），或进行其他修改。

(2) 和 (3) 引入了类似于比特币的 P2SH 的功能，允许用户将资金发送到可证明仅映射到特定代码块的地址。 类似于这样的东西从长远来看至关重要，因为在一个所有帐户都是合约的世界中，我们需要保留在帐户存在于链上之前向其发送资金的能力，因为这是当今所有区块链协议中都存在的基本功能。

# 矿工和交易重放策略

请注意，矿工需要有一种接受这些交易的策略。 这种策略需要非常具有辨别力，否则他们将面临接受不向他们支付任何费用的交易的风险，甚至可能是没有效果的交易（例如，因为该交易已被包括在内，因此 nonce 不再是最新的）。

一种简单的策略是拥有一组正则表达式，将针对帐户的 to 地址进行检查，每个正则表达式对应于已知“安全”（在这种意义上，如果帐户具有该代码，并且涉及帐户余额、帐户存储和交易数据的特定检查通过，则如果该交易包含在区块中，矿工将获得报酬）的“标准帐户类型”，并挖掘和转发通过这些检查的交易。

一个例子是按如下方式检查：

1. 检查 to 地址是否具有作为上述 Serpent 代码编译版本的代码，其中 `<pubkey hash here>` 替换为任何公钥哈希。
2. 检查交易数据中的签名是否与该密钥哈希验证。
3. 检查交易数据中的 gasprice 是否足够高
4. 检查状态中的 nonce 是否与交易数据中的 nonce 匹配
5. 检查帐户中是否有足够的以太币来支付费用

如果所有五个检查都通过，则转发和/或挖掘交易。

一种更宽松但仍然有效的策略是接受任何符合与上述相同通用格式的代码，仅消耗有限数量的 gas 来执行 nonce 和签名检查，并保证交易费用将支付给矿工。 另一种策略是，除了其他方法外，尝试处理任何要求低于 250,000 gas 的交易，并且仅当矿工在执行交易后的余额比执行交易前的余额适当高时才包括该交易。

# 版权

在 CC0 下放弃版权和相关权利。