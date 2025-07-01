---
eip: 6
title: 重命名 SUICIDE 操作码
author: Hudson Jameson <hudson@hudsonjameson.com>
status: Final
type: Standards Track
category: Interface
created: 2015-11-22
---

### 摘要
本 EIP 中提出的解决方案是将 Ethereum 编程语言中的 `SUICIDE` 操作码的名称更改为 `SELFDESTRUCT`。

### 动机
对于许多人来说，心理健康是一个非常现实的问题，而小的想法可以带来改变。那些正在应对失落或抑郁的人会因为在我们的编程语言中看不到“suicide（自杀）”这个词而受益。据估计，全球有 3.5 亿人患有抑郁症。如果我们希望将我们的生态系统发展到所有类型的开发者，就需要经常审查 Ethereum 编程语言的语义。

由 DEVolution, GmbH 委托并由 [Least Authority 执行](https://github.com/LeastAuthority/ethereum-analyses/blob/master/README.md) 的 Ethereum 安全审计提出了以下建议：
> 将指令名称“suicide（自杀）”替换为不带感情色彩的词，如“self-destruct（自毁）”、“destroy（销毁）”、“terminate（终止）”或“close（关闭）”，尤其是因为这是一个描述合约自然结论的术语。

我们更改术语 suicide 的主要原因是表明人比代码更重要，并且 Ethereum 是一个足够成熟的项目，可以认识到需要进行更改。自杀是一个沉重的话题，我们应该尽一切可能不影响我们开发社区中那些患有抑郁症或最近因自杀而失去亲人的人。Ethereum 是一个年轻的平台，如果在其发展的早期阶段实施此更改，将会减少很多麻烦。

### 实现
`SELFDESTRUCT` 被添加为 `SUICIDE` 操作码的别名（而不是替换它）。
https://github.com/ethereum/solidity/commit/a8736b7b271dac117f15164cf4d2dfabcdd2c6fd
https://github.com/ethereum/serpent/commit/1106c3bdc8f1bd9ded58a452681788ff2e03ee7c
