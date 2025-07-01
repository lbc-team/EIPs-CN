---
eip: 7
title: DELEGATECALL
author: Vitalik Buterin (@vbuterin)
status: Final
type: Standards Track
category: Core
created: 2015-11-15
---

### Hard Fork
[Homestead](./eip-606.md)

### 参数
- 激活:
  - 区块 >= 1,150,000 在主网上
  - 区块 >= 494,000 在 Morden 上
  - 区块 >= 0 在未来的测试网上

### 概述

添加一个新的操作码，`DELEGATECALL`，地址为 `0xf4`，其思路与 `CALLCODE` 类似，不同之处在于它将发送者和值从父作用域传播到子作用域，即，创建的调用与原始调用具有相同的发送者和值。

### 规范

`DELEGATECALL`：`0xf4`，接受 6 个操作数：
- `gas`：代码可以使用的 gas 量，以便执行；
- `to`：要执行的代码的目标地址；
- `in_offset`：输入在内存中的偏移量；
- `in_size`：输入的字节大小；
- `out_offset`：输出在内存中的偏移量；
- `out_size`：输出的暂存区大小。

#### 关于 gas 的注意事项
- 不提供基本津贴；`gas` 是被调用者收到的总金额。
- 与 `CALLCODE` 类似，账户创建永远不会发生，因此预付 gas 成本始终为 `schedule.callGas` + `gas`。
- 未使用的 gas 会正常退还。

#### 关于发送者的注意事项
- `CALLER` 和 `VALUE` 在被调用者的环境中的行为与在调用者的环境中的行为完全相同。

#### 其他注意事项
- 1024 的深度限制仍然正常保留。

### 理由

将发送者和值从父作用域传播到子作用域，使得合约更容易将另一个地址存储为可变代码源，并“传递”对其的调用，因为子代码将在与父代码基本相同的环境（除了减少 gas 和增加调用堆栈深度）中执行。

用例 1：拆分代码以绕过 3m gas 障碍

```python
~calldatacopy(0, 0, ~calldatasize())
if ~calldataload(0) < 2**253:
    ~delegate_call(msg.gas - 10000, $ADDR1, 0, ~calldatasize(), ~calldatasize(), 10000)
    ~return(~calldatasize(), 10000)
elif ~calldataload(0) < 2**253 * 2:
    ~delegate_call(msg.gas - 10000, $ADDR2, 0, ~calldatasize(), ~calldatasize(), 10000)
    ~return(~calldatasize(), 10000)
...
```

用例 2：用于存储合约代码的可变地址：

```python
if ~calldataload(0) / 2**224 == 0x12345678 and self.owner == msg.sender:
    self.delegate = ~calldataload(4)
else:
    ~delegate_call(msg.gas - 10000, self.delegate, 0, ~calldatasize(), ~calldatasize(), 10000)
    ~return(~calldatasize(), 10000)
```
这些方法调用的子函数现在可以自由引用 `msg.sender` 和 `msg.value`。

### 可能的反驳意见

* 你可以通过将发送者放入调用数据的前 20 个字节来复制此功能。但是，这将意味着需要为委托合约专门编译代码，并且不能同时在委托和原始上下文中使用。