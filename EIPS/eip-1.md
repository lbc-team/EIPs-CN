---
eip: 1
title: EIP 目的和指南
status: Living
type: Meta
author: Martin Becze <mb@ethereum.org>, Hudson Jameson <hudson@ethereum.org>, et al.
created: 2015-10-27
---

## 什么是 EIP？

EIP 代表 Ethereum Improvement Proposal（以太坊改进提案）。EIP 是一份设计文档，旨在向以太坊社区提供信息，或描述以太坊或其流程或环境的新特性。EIP 应该提供该特性的简洁技术规范和理由。EIP 作者负责在社区内建立共识，并记录不同的意见。

## EIP 基本原理

我们希望 EIP 成为提出新特性、收集社区对某个问题的技术意见以及记录以太坊设计决策的主要机制。由于 EIP 作为文本文件保存在版本库中，因此其修订历史记录就是特性提案的历史记录。

对于以太坊的实现者来说，EIP 是一种方便的方式来跟踪其实现的进度。理想情况下，每个实现的维护者都会列出他们已经实现的 EIP。这将为最终用户提供一种方便的方式来了解给定实现或库的当前状态。

## EIP 类型

EIP 有三种类型：

- **标准跟踪 EIP** 描述了影响大多数或所有以太坊实现的任何更改，例如对网络协议的更改、对区块或交易有效性规则的更改、提议的应用程序标准/约定，或影响使用以太坊的应用程序互操作性的任何更改或添加。标准跟踪 EIP 由三个部分组成——设计文档、实现以及（如果需要）[形式规范](https://github.com/ethereum/yellowpaper)的更新。此外，标准跟踪 EIP 可以分为以下几类：
  - **核心 (Core)**：需要共识分叉的改进（例如[EIP-5](./eip-5.md)，[EIP-101](./eip-101.md)），以及不一定对共识至关重要但可能与 ["核心开发" 讨论](https://github.com/ethereum/pm)相关的更改（例如，[EIP-90] 以及 [EIP-86](./eip-86.md) 的矿工/节点策略更改 2、3 和 4）。
  - **网络 (Networking)**：包括围绕 [devp2p](https://github.com/ethereum/devp2p/blob/readme-spec-links/rlpx.md) ([EIP-8](./eip-8.md)) 和 [Light Ethereum Subprotocol](https://ethereum.org/en/developers/docs/nodes-and-clients/#light-node) 的改进，以及对 [whisper](https://github.com/ethereum/go-ethereum/issues/16013#issuecomment-364639309) 和 [swarm](https://github.com/ethereum/go-ethereum/pull/2959) 网络协议规范的拟议改进。
  - **接口 (Interface)**：包括围绕语言级别标准的改进，例如方法名称 ([EIP-6](./eip-6.md)) 和 [合约 ABI](https://docs.soliditylang.org/en/develop/abi-spec.html)。
  - **ERC**：应用程序级别的标准和约定，包括合约标准，例如代币标准 ([ERC-20](./eip-20.md))、名称注册表 ([ERC-137](./eip-137.md))、URI 方案、库/包格式和钱包格式。

- **Meta EIP** 描述了围绕以太坊的流程，或者提出了对流程的更改（或流程中的事件）。流程 EIP 类似于标准跟踪 EIP，但适用于以太坊协议本身以外的领域。他们可能会提出一个实现，但不是针对以太坊的代码库；他们通常需要社区共识；与信息 EIP 不同，它们不仅仅是建议，并且用户通常不能自由地忽略它们。示例包括程序、指南、决策过程的更改以及以太坊开发中使用的工具或环境的更改。任何 Meta EIP 也被认为是流程 EIP。

- **信息 EIP** 描述了一个以太坊设计问题，或者向以太坊社区提供了一般性指南或信息，但没有提出新特性。信息 EIP 不一定代表以太坊社区的共识或建议，因此用户和实现者可以自由地忽略信息 EIP 或遵循他们的建议。

强烈建议单个 EIP 包含单个关键提案或新想法。EIP 越集中，它就越容易成功。对一个客户端的更改不需要 EIP；影响多个客户端或定义多个应用程序使用的标准的更改则需要。

EIP 必须满足某些最低标准。它必须是对拟议增强功能的清晰而完整的描述。增强功能必须代表净改进。如果适用，拟议的实现必须是可靠的，并且不得不适当地使协议复杂化。

### 核心 EIP 的特殊要求

如果**核心 (Core)** EIP 提及或提议更改 EVM (Ethereum Virtual Machine，以太坊虚拟机)，则应按助记符引用指令，并且至少定义一次这些助记符的操作码。首选方式如下：

```
REVERT (0xfe)
```

## EIP 工作流程

### 引导 EIP

流程中的参与方包括你、倡导者或 *EIP 作者*、[*EIP 编辑*](#eip-editors)和 [*以太坊核心开发者*](https://github.com/ethereum/pm)。

在开始编写正式的 EIP 之前，你应该审查你的想法。首先询问以太坊社区一个想法是否是原创的，以避免浪费时间在基于先前研究将被拒绝的事情上。因此，建议在 [Ethereum Magicians 论坛](https://ethereum-magicians.org/)上开设一个讨论主题来做到这一点。

一旦该想法经过审查，你的下一个责任将是通过 EIP 将该想法呈现给审阅者和所有相关方，邀请编辑、开发人员和社区在上述渠道上提供反馈。你应该尝试评估你对 EIP 的兴趣是否与实施该 EIP 所涉及的工作量以及有多少方必须遵守它相称。例如，实施核心 EIP 所需的工作量将远大于 ERC，并且 EIP 需要以太坊客户端团队的足够兴趣。负面的社区反馈将被考虑在内，并可能阻止你的 EIP 超过草案阶段。

### 核心 EIP

对于核心 EIP，鉴于它们需要客户端实现才能被认为是**最终版本**（请参阅下面的“EIP 流程”），你需要为客户端提供实现或说服客户端实施你的 EIP。

让客户端实施者审查你的 EIP 的最佳方式是在 AllCoreDevs 通话中展示它。你可以通过在 [AllCoreDevs 议程 GitHub Issue](https://github.com/ethereum/pm/issues) 上发布评论来要求这样做，并在评论中链接到你的 EIP。

AllCoreDevs 通话是一种让客户端实施者做三件事的方式。首先，讨论 EIP 的技术优点。其次，评估其他客户端将要实施的内容。第三，协调网络升级的 EIP 实施。

这些通话通常会导致围绕应实施哪些 EIP 达成“大致共识”。这种“大致共识”基于以下假设：EIP 没有足够的争议会导致网络分裂，并且它们在技术上是合理的。

:warning: EIP 流程和 AllCoreDevs 通话并非旨在解决有争议的非技术问题，但由于缺乏解决这些问题的其他方法，最终常常会纠缠其中。这给客户端实施者带来了尝试评估社区情绪的负担，这阻碍了 EIP 和 AllCoreDevs 通话的技术协调功能。如果你正在引导 EIP，你可以通过确保你的 EIP 的 [Ethereum Magicians 论坛](https://ethereum-magicians.org/) 线程包含或链接到尽可能多的社区讨论，并且各个利益相关者都有充分的代表性，从而简化建立社社区共识的过程。

*简而言之，你作为倡导者的角色是使用下面描述的风格和格式编写 EIP，引导适当论坛中的讨论，并围绕该想法建立社区共识。*

### EIP 流程

以下是所有跟踪中的所有 EIP 的标准化流程：

![EIP 状态图](../assets/eip-1/EIP-process-update.jpg)

**想法（Idea）** - 草案之前的想法。这不在 EIP 存储库中跟踪。

**草案（Draft）** - EIP 开发中第一个正式跟踪的阶段。当 EIP 格式正确时，由 EIP 编辑将其合并到 EIP 存储库中。

**审查（Review）** - EIP 作者将 EIP 标记为准备好并请求同行评审。

**最后征求意见（Last Call）** - 这是 EIP 进入“最终（Final）”状态之前的最终审查窗口。EIP 编辑将分配“最后征求意见（Last Call）”状态并设置审查结束日期（`last-call-deadline`），通常为 14 天后。

如果在此期间导致必要的规范性更改，它将使 EIP 恢复为“审查（Review）”。

**最终（Final）** - 此 EIP 代表最终标准。“最终（Final）”EIP 存在于最终状态，应仅更新以更正勘误并添加非规范性说明。

将 EIP 从“最后征求意见（Last Call）”移至“最终（Final）”的 PR 不应包含状态更新以外的任何更改。任何内容或编辑提议的更改应与此状态更新 PR 分开，并在其之前提交。

**停滞（Stagnant）** - 在“草案（Draft）”、“审查（Review）”或“最后征求意见（Last Call）”中的任何 EIP，如果闲置 6 个月或更长时间，则会移至“停滞（Stagnant）”。EIP 可以通过作者或 EIP 编辑将其移回“草案（Draft）”或其早期状态来从此状态中恢复。如果未恢复，则提案可能会永久保持此状态。

>*EIP 作者会收到对其 EIP 状态的任何算法更改的通知*

**撤回（Withdrawn）** - EIP 作者已撤回了提出的 EIP。此状态具有最终性，并且不能再使用此 EIP 编号来恢复。如果该想法在稍后日期被采纳，则将其视为新提案。

**活跃（Living）** - EIP 的一种特殊状态，这些 EIP 旨在不断更新，而不会达到最终状态。这尤其包括 EIP-1。

## 成功的 EIP 中包含哪些内容？

每个 EIP 都应具有以下部分：

- 前导码（Preamble）- RFC 822 样式的标头，其中包含有关 EIP 的元数据，包括 EIP 编号、简短的描述性标题（限制为最多 44 个字符）、描述（限制为最多 140 个字符）和作者详细信息。无论类别如何，标题和描述都不应包含 EIP 编号。有关详细信息，请参见[下方](./eip-1.md#eip-header-preamble)。
- 摘要（Abstract）- 摘要是多句（短段落）技术摘要。这应该是规范部分的非常简洁且易于理解的版本。有人应该只阅读摘要，就可以了解该规范的作用。
- 动机（Motivation）*(可选)* - 动机部分对于想要更改以太坊协议的 EIP 至关重要。它应清楚地解释为什么现有协议规范不足以解决 EIP 解决的问题。如果动机很明显，则可以省略此部分。
- 规范（Specification）- 技术规范应描述任何新特性的语法和语义。该规范应足够详细，以便为任何当前的以太坊平台（besu、erigon、ethereumjs、go-ethereum、nethermind 或其他平台）提供竞争性的、可互操作的实现。
- 基本原理（Rationale）- 基本原理通过描述设计动机以及为什么做出特定的设计决策来充实规范。它应描述所考虑的替代设计和相关工作，例如，该特性在其他语言中的支持方式。基本原理应讨论围绕 EIP 的讨论中提出的重要异议或疑虑。
- 向后兼容性（Backwards Compatibility）*(可选)* - 所有引入向后不兼容性的 EIP 必须包含一个描述这些不兼容性及其后果的部分。EIP 必须解释作者建议如何处理这些不兼容性。如果该提案未引入任何向后不兼容性，则可以省略此部分，但是如果存在向后不兼容性，则必须包含此部分。
- 测试用例（Test Cases）*(可选)* - 对于影响共识变更的 EIP，实现测试用例是强制性的。测试应以内联方式包含在 EIP 中作为数据（例如输入/预期输出对），或包含在`../assets/eip-###/<filename>`中。非核心提案可以省略此部分。
- 参考实现（Reference Implementation）*(可选)* - 一个可选部分，其中包含人们可以用来帮助理解或实现此规范的参考/示例实现。所有 EIP 都可以省略此部分。
- 安全考虑（Security Considerations）- 所有 EIP 必须包含一个部分，讨论与拟议变更相关的安全影响/考虑因素。包括可能对安全讨论很重要的信息、表面风险，并可以在提案的整个生命周期中使用。例如，包括与安全相关的设计决策、疑虑、重要讨论、特定于实现的指南和陷阱，以及威胁和风险的概述以及如何解决这些问题。缺少“安全考虑”部分的 EIP 提交将被拒绝。如果没有审阅者认为足够的“安全考虑”讨论，EIP 将无法进入“最终（Final）”状态。
- 版权放弃（Copyright Waiver）- 所有 EIP 必须在公共领域中。版权放弃必须链接到许可文件并使用以下措辞：`版权和相关权利通过 [CC0](../LICENSE.md) 放弃。`

## EIP 格式和模板

EIP 应该以 [markdown](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) 格式编写。有一个 [模板](https://github.com/ethereum/EIPs/blob/master/eip-template.md) 可供遵循。

## EIP 标头前导码

每个 EIP 必须以 [RFC 822](https://www.ietf.org/rfc/rfc822.txt) 样式的标头前导码开头，并在其前后加上三个连字符 (`---`)。此标头也称为 Jekyll 的 ["front matter"](https://jekyllrb.com/docs/front-matter/)。标头必须按以下顺序显示。

`eip`: *EIP number（EIP 编号）*

`title`: *The EIP title is a few words, not a complete sentence（EIP 标题是几个词，而不是一个完整的句子）*

`description`: *Description is one full (short) sentence（描述是一个完整的（简短）句子）*

`author`: *The list of the author's or authors' name(s) and/or username(s), or name(s) and email(s). Details are below（作者或作者的姓名和/或用户名，或姓名和电子邮件的列表。详细信息如下。）*

`discussions-to`: *The url pointing to the official discussion thread（指向官方讨论线程的 URL）*

`status`: *Draft, Review, Last Call, Final, Stagnant, Withdrawn, Living（草案、审查、最后征求意见、最终、停滞、撤回、活跃）*

`last-call-deadline`: *The date last call period ends on（最后征求意见期限结束的日期）* (可选字段，仅当状态为 `Last Call` 时需要)

`type`: *One of `Standards Track`, `Meta`, or `Informational`（`标准跟踪`、`Meta` 或 `信息`之一）*

`category`: *One of `Core`, `Networking`, `Interface`, or `ERC`（`核心`、`网络`、`接口` 或 `ERC` 之一）* (可选字段，仅适用于 `标准跟踪` EIP)

`created`: *Date the EIP was created on（创建 EIP 的日期）*

`requires`: *EIP number(s)（EIP 编号）* (可选字段)

`withdrawal-reason`: *A sentence explaining why the EIP was withdrawn（解释 EIP 为何被撤回的句子）* (可选字段，仅当状态为 `Withdrawn` 时需要)

允许列表的标头必须用逗号分隔元素。

需要日期的标头将始终采用 ISO 8601 (yyyy-mm-dd) 格式。

### `author` 标头

`author` 标头列出了 EIP 的作者/所有者的姓名、电子邮件地址或用户名。那些喜欢匿名的人可以仅使用用户名，也可以使用名字和用户名。`author` 标头值的格式必须为：

> Random J. User &lt;address@dom.ain&gt;

或

> Random J. User (@username)

或

> Random J. User (@username) &lt;address@dom.ain&gt;

如果包含电子邮件地址和/或 GitHub 用户名，并且

> Random J. User

如果未提供电子邮件地址和 GitHub 用户名。

至少一位作者必须使用 GitHub 用户名，以便收到更改请求的通知并具有批准或拒绝更改请求的能力。

### `discussions-to` 标头

当 EIP 为草案时，`discussions-to` 标头将指示正在讨论 EIP 的 URL。

首选的讨论 URL 是 [Ethereum Magicians](https://ethereum-magicians.org/) 上的一个主题。该 URL 不能指向 Github pull request、任何临时 URL 以及任何可能随着时间推移而被锁定的 URL（即 Reddit 主题）。

### `type` 标头

`type` 标头指定 EIP 的类型：标准跟踪、Meta 或信息。如果跟踪是标准，请包括子类别（核心、网络、接口或 ERC）。

### `category` 标头

`category` 标头指定 EIP 的类别。这仅对于标准跟踪 EIP 是必需的。

### `created` 标头

`created` 标头记录分配 EIP 编号的日期。这两个标头都应采用 yyyy-mm-dd 格式，例如 2001-08-14。

### `requires` 标头

EIP 可以具有 `requires` 标头，指示此 EIP 依赖的 EIP 编号。如果存在此类依赖关系，则此字段是必需的。

当没有来自另一个 EIP 的概念或技术要素就无法理解或实现当前 EIP 时，就会创建 `requires` 依赖关系。仅仅提及另一个 EIP 不一定会创建这样的依赖关系。

## 链接到外部资源

除了下面列出的特定例外情况外，**不应**包含指向外部资源的链接。外部资源可能会意外消失、移动或更改。

管理允许的外部资源的流程在 [EIP-5757](./eip-5757.md) 中进行了描述。

### 执行客户端规范

可以使用正常的 markdown 语法包含指向以太坊执行客户端规范的链接，例如：

```markdown
[Ethereum Execution Client Specifications](https://github.com/ethereum/execution-specs/blob/9a1f22311f517401fed6c939a159b55600c454af/README.md)
```

呈现为：

[Ethereum Execution Client Specifications](https://github.com/ethereum/execution-specs/blob/9a1f22311f517401fed6c939a159b55600c454af/README.md)

允许的执行客户端规范 URL 必须锚定到特定的提交，因此必须与此正则表达式匹配：

```regex
^(https://github.com/ethereum/execution-specs/(blob|commit)/[0-9a-f]{40}/.*|https://github.com/ethereum/execution-specs/tree/[0-9a-f]{40}/.*)$
```

### 共识层规范

可以使用正常的 markdown 语法包含指向以太坊共识层规范中特定提交的文件的链接，例如：

```markdown
[Beacon Chain](https://github.com/ethereum/consensus-specs/blob/26695a9fdb747ecbe4f0bb9812fedbc402e5e18c/specs/sharding/beacon-chain.md)
```

呈现为：

[Beacon Chain](https://github.com/ethereum/consensus-specs/blob/26695a9fdb747ecbe4f0bb9812fedbc402e5e18c/specs/sharding/beacon-chain.md)

允许的共识层规范 URL 必须锚定到特定的提交，因此必须与此正则表达式匹配：

```regex
^https://github.com/ethereum/consensus-specs/(blob|commit)/[0-9a-f]{40}/.*$
```

### 网络规范

可以使用正常的 markdown 语法包含指向以太坊网络规范中特定提交的文件的链接，例如：

```markdown
[Ethereum Wire Protocol](https://github.com/ethereum/devp2p/blob/40ab248bf7e017e83cc9812a4e048446709623e8/caps/eth.md)
```

呈现为：

[Ethereum Wire Protocol](https://github.com/ethereum/devp2p/blob/40ab248bf7e017e83cc9812a4e048446709623e8/caps/eth.md)

允许的网络规范 URL 必须锚定到特定的提交，因此必须与此正则表达式匹配：

```regex
^https://github.com/ethereum/devp2p/(blob|commit)/[0-9a-f]{40}/.*$
```

### 万维网联盟 (W3C)

可以使用正常的 markdown 语法包含指向 W3C“推荐”状态规范的链接。例如，允许以下链接：

```markdown
[Secure Contexts](https://www.w3.org/TR/2021/CRD-secure-contexts-20210918/)
```

呈现为：

[Secure Contexts](https://www.w3.org/TR/2021/CRD-secure-contexts-20210918/)

允许的 W3C 推荐 URL 必须锚定到技术报告命名空间中带有日期的规范，因此必须与此正则表达式匹配：

```regex
^https://www\.w3\.org/TR/[0-9][0-9][0-9][0-9]/.*$
```

### Web 超文本应用技术工作组 (WHATWG)

可以使用正常的 markdown 语法包含指向 WHATWG 规范的链接，例如：

```markdown
[HTML](https://html.spec.whatwg.org/commit-snapshots/578def68a9735a1e36610a6789245ddfc13d24e0/)
```

呈现为：

[HTML](https://html.spec.whatwg.org/commit-snapshots/578def68a9735a1e36610a6789245ddfc13d24e0/)

允许的 WHATWG 规范 URL 必须锚定到 `spec` 子域中定义的规范（不允许使用 idea 规范）和提交快照，因此必须与此正则表达式匹配：

```regex
^https:\/\/[a-z]*\.spec\.whatwg\.org/commit-snapshots/[0-9a-f]{40}/$
```

尽管 WHATWG 不建议这样做，但 EIP 必须锚定到特定的提交，以便将来的读者可以参考 EIP 最终确定时存在的实时标准的精确版本。这为读者提供了足够的信息来维护与 EIP 引用的版本和当前实时标准的兼容性（如果他们选择这样做）。

### 互联网工程任务组 (IETF)

可以使用正常的 markdown 语法包含指向 IETF Request For Comment (RFC) 规范的链接，例如：

```markdown
[RFC 8446](https://www.rfc-editor.org/rfc/rfc8446)
```

呈现为：

[RFC 8446](https://www.rfc-editor.org/rfc/rfc8446)

允许的 IETF 规范 URL 必须锚定到具有已分配 RFC 编号的规范（意味着不能引用互联网草案），因此必须与此正则表达式匹配：

```regex
^https:\/\/www.rfc-editor.org\/rfc\/.*$
```

### 比特币改进提案

可以使用正常的 markdown 语法包含指向比特币改进提案的链接，例如：

```markdown
[BIP 38](https://github.com/bitcoin/bips/blob/3db736243cd01389a4dfd98738204df1856dc5b9/bip-0038.mediawiki)
```

呈现为：

[BIP 38](https://github.com/bitcoin/bips/blob/3db736243cd01389a4dfd98738204df1856dc5b9/bip-0038.mediawiki)

允许的比特币改进提案 URL 必须锚定到特定的提交，因此必须与此正则表达式匹配：

```regex
^(https://github.com/bitcoin/bips/blob/[0-9a-f]{40}/bip-[0-9]+\.mediawiki)$
```

### 国家漏洞数据库 (NVD)

可以使用国家标准与技术研究院 (NIST) 发布的通用漏洞披露 (CVE) 系统链接，前提是它们符合最新更改的日期，使用以下语法：

```markdown
[CVE-2023-29638 (2023-10-17T10:14:15)](https://nvd.nist.gov/vuln/detail/CVE-2023-29638)
```

呈现为：

[CVE-2023-29638 (2023-10-17T10:14:15)](https://nvd.nist.gov/vuln/detail/CVE-2023-29638)

### 数字对象标识符系统

可以使用数字对象标识符 (DOI) 限定的链接，使用以下语法：

````markdown
This is a sentence with a footnote.[^1]

[^1]:
    ```csl-json
    {
      "type": "article",
      "id": 1,
      "author": [
        {
          "family": "Jameson",
          "given": "Hudson"
        }
      ],
      "DOI": "00.0000/a00000-000-0000-y",
      "title": "An Interesting Article",
      "original-date": {
        "date-parts": [
          [2022, 12, 31]
        ]
      },
      "URL": "https://sly-hub.invalid/00.0000/a00000-000-0000-y",
      "custom": {
        "additional-urls": [
          "https://example.com/an-interesting-article.pdf"
        ]
      }
    }
    ```
````

呈现为：

<!-- markdownlint-capture -->
<!-- markdownlint-disable code-block-style -->

This is a sentence with a footnote.[^1]

[^1]:
    ```csl-json
    {
      "type": "article",
      "id": 1,
      "author": [
        {
          "family": "Jameson",
          "given": "Hudson"
        }
      ],
      "DOI": "00.0000/a00000-000-0000-y",
      "title": "An Interesting Article",
      "original-date": {
        "date-parts": [
          [2022, 12, 31]
        ]
      },
      "URL": "https://sly-hub.invalid/00.0000/a00000-000-0000-y",
      "custom": {
        "additional-urls": [
          "https://example.com/an-interesting-article.pdf"
        ]
      }
    }
    ```

<!-- markdownlint-restore -->

有关支持的字段，请参阅 [Citation Style Language Schema](https://resource.citationstyles.org/schema/v1.0/input/json/csl-data.json)。除了通过针对该模式的验证外，引用必须包括 DOI 和至少一个 URL。

顶级 URL 字段必须解析为可以零成本查看的引用文档的副本。`additional-urls` 下的值也必须解析为引用文档的副本，但可能会收取费用。

## 链接到其他 EIP

对其他 EIP 的引用应遵循 `EIP-N` 格式，其中 `N` 是您要引用的 EIP 编号。在 EIP 中引用的每个 EIP **必须**在第一次引用时附带一个相对 markdown 链接，并且**可以**在后续引用中附带一个链接。链接**必须**始终通过相对路径完成，以便链接在此 GitHub 存储库、此存储库的分支、主 EIP 站点、主 EIP 站点的镜像等中起作用。例如，您应该将此 EIP 链接为 `./eip-1.md`。

## 辅助文件

图像、图表和辅助文件应包含在该 EIP 的 `assets` 文件夹的子目录中，如下所示：`assets/eip-N`（其中 **N** 将替换为 EIP 编号）。链接到 EIP 中的图像时，请使用相对链接，例如 `../assets/eip-1/image.png`。

## 转移 EIP 所有权

有时有必要将 EIP 的所有权转移给新的倡导者。一般来说，我们希望保留原始作者作为转移的 EIP 的共同作者，但这实际上取决于原始作者。转移所有权的一个好理由是，原始作者不再有时间或兴趣来更新它或完成 EIP 流程，或者已经从互联网上消失了（即无法联系或没有回复电子邮件）。转移所有权的一个坏理由是因为您不同意 EIP 的方向。我们尝试围绕 EIP 建立共识，但如果这不可能，您可以随时提交竞争的 EIP。

如果您有兴趣承担 EIP 的所有权，请发送一条消息，要求接管，发送给原始作者和 EIP 编辑。如果原始作者没有及时回复电子邮件，EIP 编辑将做出单方面决定（并非此类决定无法撤销 :)）。

## EIP 编辑

当前的 EIP 编辑是

- Matt Garnett (@lightclient)
- Sam Wilson (@SamWilsn)
- Zainan Victor Zhou (@xinbenlv)
- Gajinder Singh (@g11tech)

荣誉 EIP 编辑是

- Alex Beregszaszi (@axic)
- Casey Detrio (@cdetrio)
- Gavin John (@Pandapip1)
- Greg Colvin (@gcolvin)
- Hudson Jameson (@Souptacular)
- Martin Becze (@wanderer)
- Micah Zoltu (@MicahZoltu)
- Nick Johnson (@arachnid)
- Nick Savers (@nicksavers)
- Vitalik Buterin (@vbuterin)

如果您想成为 EIP 编辑，请查看 [EIP-5069](./eip-5069.md)。

## EIP 编辑职责

对于每个新的 EIP，编辑执行以下操作：

- 阅读 EIP 以检查它是否已准备好：合理且完整。这些想法必须具有技术意义，即使它们似乎不太可能达到最终状态。
- 标题应准确描述内容。
- 检查 EIP 的语言（拼写、语法、句子结构等）、标记（GitHub flavored Markdown）、代码风格

如果 EIP 未准备好，编辑将将其发回给作者进行修订，并提供具体说明。

一旦 EIP 准备好进入存储库，EIP 编辑将：

- 分配一个 EIP 编号（通常是增量的；如果怀疑有人抢注编号，编辑可以重新分配）
- 合并相应的 [pull request](https://github.com/ethereum/EIPs/pulls)
- 向 EIP 作者发回一条消息，说明下一步。

许多 EIP 由具有以太坊代码库写入权限的开发人员编写和维护。EIP 编辑监控 EIP 更改，并纠正我们看到的任何结构、语法、拼写或标记错误。

编辑不对 EIP 做出判断。我们只是做管理和编辑部分。

## 风格指南

### 标题

前导码中的 `title` 字段：

- 不应包含“标准”或其任何变体；并且
- 不应包含 EIP 的编号。

### 描述

前导码中的 `description` 字段：

- 不应包含“标准”或其任何变体；并且
- 不应包含 EIP 的编号。

### EIP 编号

当引用 `category` 为 `ERC` 的 EIP 时，必须以连字符形式 `ERC-X` 编写，其中 `X` 是该 EIP 的分配编号。当引用任何其他 `category` 的 EIP 时，必须以连字符形式 `EIP-X` 编写，其中 `X` 是该 EIP 的分配编号。

### RFC 2119 和 RFC 8174

鼓励 EIP 遵循 [RFC 2119](https://www.ietf.org/rfc/rfc2119.html) 和 [RFC 8174](https://www.ietf.org/rfc/rfc8174.html) 中的术语，并在规范部分的开头插入以下内容：

> The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 and RFC 8174.

## 历史

本文档很大程度上来源于 Amir Taaki 编写的 [Bitcoin's BIP-0001](https://github.com/bitcoin/bips)，而后者又来源于 [Python's PEP-0001](https://peps.python.org/)。在许多地方，文本只是被复制和修改。尽管 PEP-0001 文本由 Barry Warsaw、Jeremy Hylton 和 David Goodger 编写，但他们不对其在以太坊改进过程中的使用负责，不应因以太坊或 EIP 特有的技术问题而受到打扰。请将所有评论发送给 EIP 编辑。

## 版权

版权和相关权利通过 [CC0](../LICENSE.md) 放弃。