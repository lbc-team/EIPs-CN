---
eip: 20
title: Token 标准
author: Fabian Vogelsteller <fabian@ethereum.org>, Vitalik Buterin <vitalik.buterin@ethereum.org>
type: Standards Track
category: ERC
status: Final
created: 2015-11-19
---

## 简单总结

Token 的标准接口。

## 摘要

以下标准允许在智能合约中实现 token 的标准 API。
此标准提供传输 token 的基本功能，并允许 token 被批准，以便链上的另一第三方可以使用它们。

## 动机

标准接口允许以太坊上的任何 token 被其他应用程序重用：从钱包到去中心化交易所。

## 规范

## Token
### 方法

**注意**:
 - 以下规范使用 Solidity `0.4.17`（或更高版本）的语法
 - 调用者必须处理 `returns (bool success)` 返回的 `false`。调用者绝不能假设永远不会返回 `false`！

#### name

返回 Token 的名称 - 例如 `"MyToken"`。

可选 - 此方法可用于提高可用性，
但接口和其他合约不应该期望这些值的存在。

``` js
function name() public view returns (string)
```

#### symbol

返回 Token 的符号。例如 "HIX"。

可选 - 此方法可用于提高可用性，
但接口和其他合约不应该期望这些值的存在。

``` js
function symbol() public view returns (string)
```

#### decimals

返回 Token 使用的小数位数 - 例如 `8`，表示将 Token 数量除以 `100000000` 以获得其用户表示。

可选 - 此方法可用于提高可用性，
但接口和其他合约不应该期望这些值的存在。

``` js
function decimals() public view returns (uint8)
```

#### totalSupply

返回 Token 的总供应量。

``` js
function totalSupply() public view returns (uint256)
```

#### balanceOf

返回地址为 `_owner` 的另一个账户的账户余额。

``` js
function balanceOf(address _owner) public view returns (uint256 balance)
```

#### transfer

将 `_value` 数量的 Token 转移到地址 `_to`，并且必须触发 `Transfer` 事件。
如果消息调用者的账户余额没有足够的 Token 可供花费，则该函数应该 `throw`。

*注意* 0 值的转移必须被视为正常转移并触发 `Transfer` 事件。

``` js
function transfer(address _to, uint256 _value) public returns (bool success)
```

#### transferFrom

将 `_value` 数量的 Token 从地址 `_from` 转移到地址 `_to`，并且必须触发 `Transfer` 事件。

`transferFrom` 方法用于提款工作流程，允许合约代表您转移 Token。
例如，这可用于允许合约代表您转移 Token 和/或以子货币收取费用。
除非 `_from` 账户已通过某种机制故意授权消息的发送者，否则该函数应该 `throw`。

*注意* 0 值的转移必须被视为正常转移并触发 `Transfer` 事件。

``` js
function transferFrom(address _from, address _to, uint256 _value) public returns (bool success)
```

#### approve

允许 `_spender` 从您的账户中多次提取，最高可达 `_value` 数量。如果再次调用此函数，它将使用 `_value` 覆盖当前的授权额度。

**注意**：为了防止像[此处描述](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/)和[此处讨论](https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729)的攻击向量，
客户端应该确保创建用户界面，以便在将授权额度设置为同一 spender 的另一个值之前，首先将其设置为 `0`。
虽然合约本身不应该强制执行此操作，以允许与之前部署的合约向后兼容

``` js
function approve(address _spender, uint256 _value) public returns (bool success)
```

#### allowance

返回 `_spender` 仍然可以从 `_owner` 提取的数量。

``` js
function allowance(address _owner, address _spender) public view returns (uint256 remaining)
```

### 事件

#### Transfer

当 Token 被转移时必须触发，包括零值转移。

创建新 Token 的 Token 合约应该在创建 Token 时触发一个 `_from` 地址设置为 `0x0` 的 Transfer 事件。

``` js
event Transfer(address indexed _from, address indexed _to, uint256 _value)
```

#### Approval

必须在任何成功调用 `approve(address _spender, uint256 _value)` 时触发。

``` js
event Approval(address indexed _owner, address indexed _spender, uint256 _value)
```

## 实现

以太坊网络上已经部署了大量符合 ERC20 标准的 Token。
不同的团队编写了不同的实现，这些实现具有不同的权衡：从节省 gas 到提高安全性。

#### 示例实现可在以下位置找到
- [OpenZeppelin 实现](../assets/eip-20/OpenZeppelin-ERC20.sol)
- [ConsenSys 实现](../assets/eip-20/Consensys-EIP20.sol)

## 历史

与此标准相关的历史链接：

- Vitalik Buterin 的原始提案：https://github.com/ethereum/wiki/wiki/Standardized_Contract_APIs/499c882f3ec123537fc2fccd57eaa29e6032fe4a
- Reddit 讨论：https://www.reddit.com/r/ethereum/comments/3n8fkn/lets_talk_about_the_coin_standard/
- 原始 Issue #20：https://github.com/ethereum/EIPs/issues/20

## 版权
版权及相关权利通过 [CC0](../LICENSE.md) 放弃。