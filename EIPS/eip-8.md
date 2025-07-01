---
eip: 8
title: Homestead 中 devp2p 的向前兼容性要求
author: Felix Lange <felix@ethdev.com>
status: Final
type: Standards Track
category: Networking
created: 2015-12-18
---

### 摘要

本 EIP 为 devp2p Wire Protocol、RLPx Discovery Protocol 和 RLPx TCP Transport Protocol 的实现引入了新的向前兼容性要求。实现 EIP-8 的客户端应遵循波斯特尔定律：

> 做事要保守，接受他人要开明。

### 规范

**devp2p Wire Protocol** 的实现应忽略 hello 数据包的版本号。发送 hello 数据包时，version 元素应设置为支持的最高 devp2p 版本。实现还应忽略 hello 数据包末尾的任何其他列表元素。

同样，**RLPx Discovery Protocol** 的实现不应验证 ping 数据包的版本号，应忽略任何数据包中的任何其他列表元素，并忽略任何数据包中第一个 RLP 值之后的任何数据。具有未知数据包类型的 Discovery 数据包应被静默丢弃。任何 discovery 数据包的最大大小仍然是 1280 字节。

最后，**RLPx TCP Transport protocol** 的实现应接受加密密钥建立握手数据包的新编码。如果收到 EIP-8 样式的 RLPx `auth-packet`，则应使用以下规则发送相应的 `ack-packet`。

解码 `auth-body` 和 `ack-body` 中的 RLP 数据应忽略 `auth-vsn` 和 `ack-vsn` 的不匹配、任何其他列表元素以及列表之后的任何尾随数据。在过渡期间（即，直到旧格式停用为止），实现应使用至少 100 字节的垃圾数据填充 `auth-body`。建议添加 [100, 300] 范围内的随机量，以改变数据包的大小。

```text
auth-vsn         = 4
auth-size        = enc-auth-body 的大小，编码为大端 16 位整数
auth-body        = rlp.list(sig, initiator-pubk, initiator-nonce, auth-vsn)
enc-auth-body    = ecies.encrypt(recipient-pubk, auth-body, auth-size)
auth-packet      = auth-size || enc-auth-body

ack-vsn          = 4
ack-size         = enc-ack-body 的大小，编码为大端 16 位整数
ack-body         = rlp.list(recipient-ephemeral-pubk, recipient-nonce, ack-vsn)
enc-ack-body     = ecies.encrypt(initiator-pubk, ack-body, ack-size)
ack-packet       = ack-size || enc-ack-body

where

X || Y
    表示 X 和 Y 的连接。
X[:N]
    表示 X 的 N 字节前缀。
rlp.list(X, Y, Z, ...)
    表示 [X, Y, Z, ...] 作为 RLP 列表的递归编码。
sha3(MESSAGE)
    是 Ethereum 使用的 Keccak256 哈希函数。
ecies.encrypt(PUBKEY, MESSAGE, AUTHDATA)
    是 RLPx 使用的非对称身份验证加密函数。
    AUTHDATA 是经过身份验证的数据，它不是结果密文的一部分，
    而是在生成消息标记之前写入 HMAC-256。
```

### 动机

devp2p 协议的更改很难部署，因为如果 hello（discovery ping、RLPx 握手）数据包的版本号或结构与本地预期不符，则运行旧版本的客户端将拒绝通信。

将向前兼容性要求作为 Homestead 共识升级的一部分引入，将确保 Ethereum 网络上使用的所有客户端软件都能应对未来的网络协议升级（只要保持向后兼容性）。

### 基本原理

所提出的更改通过在整个协议栈中应用波斯特尔定律（也称为稳健性原则）来解决向前兼容性问题。自最初在 RFC 761 中应用以来，已经反复研究了这种方法的优点和适用性。有关最新的观点，请参阅
[“重新考虑稳健性原则”（Eric Allman，2011）](https://queue.acm.org/detail.cfm?id=1999945)。

#### 对 devp2p Wire Protocol 的更改

所有客户端当前都包含以下语句：

```python
# pydevp2p/p2p_protocol.py
if data['version'] != proto.version:
    log.debug('incompatible network protocols', peer=proto.peer,
        expected=proto.version, received=data['version'])
    return proto.send_disconnect(reason=reasons.incompatibel_p2p_version)
```

这些检查使得不可能更改 hello 数据包的版本或结构。删除它们可以切换到较新的协议版本：实现较新版本的客户端只需发送具有更高版本和可能附加列表元素的数据包。

* 如果具有较低版本的节点收到此类数据包，它将盲目地假定远程端向后兼容，并使用旧握手进行响应。
* 如果具有相同版本的节点收到该数据包，则可以使用该协议的新功能。
* 如果具有更高版本的节点收到该数据包，则可以启用
  向后兼容性逻辑或断开连接。

#### 对 RLPx Discovery Protocol 的更改

放宽 discovery 数据包解码规则在很大程度上规范了当前的实践。大多数现有实现都不关心列表元素的数量（go-ethereum 除外），并且不拒绝具有不匹配版本的节点。但是，规范不能保证此行为。

如果采用，此更改使得可以以与 devp2p hello 更改类似的方式部署协议更改：只需增加版本并发送其他信息。旧客户端将忽略其他元素，即使网络上的大多数客户端已迁移到更新的协议，它们也可以继续运行。

#### 对 RLPx TCP 握手的更改

对 RLPx v5 更改（分块数据包、密钥派生更改）的讨论部分原因在于 v4 握手编码仅提供一种带内方式来添加版本号：缩短 nonce 的随机部分。即使 RLPx v5 握手提案被接受，未来的升级也很困难，因为握手数据包是具有已知布局的固定大小 ECIES 密文。

我建议对握手数据包进行以下更改：

* 将密文的长度添加为纯文本标头。
* 将握手的主体编码为 RLP。
* 用版本号替换两个数据包中的令牌标志（未使用）。
* 删除临时公钥的哈希值（它是多余的）。

这些更改使得可以按照与其他协议描述的方式相同的方式升级 RLPx TCP 传输协议，即通过添加列表元素和增加版本。由于这是对 RLPx 握手数据包的首次更改，因此我们可以抓住机会删除所有当前未使用的字段。

允许（事实上是必需的）在 RLP 列表之后添加其他数据，因为握手数据包需要增长以便与旧格式区分开来。
客户端可以采用以下伪代码之类的逻辑来同时处理两种格式。

```go
packet = read(307, connection)
if decrypt(packet) {
    // process as old format
} else {
    size = unpack_16bit_big_endian(packet)
    packet += read(size - 307 + 2, connection)
    if !decrypt(packet) {
        // error
    }
    // process as new format
}
```

纯文本大小前缀可能是本文档中最具争议的方面。有人认为，前缀有助于那些试图在网络级别过滤和识别 RLPx 连接的对手。

这在很大程度上是对手愿意花费多少精力的问题。如果遵循随机化长度的建议，则纯粹基于模式的数据包识别不太可能成功。

* 对于典型的防火墙运营商来说，阻止所有前两个字节形成 [300,600] 范围内的整数的连接可能过于激进。基于端口的阻止将是过滤大多数 RLPx 流量的更有效措施。
* 对于能够负担得起关联许多标准的攻击者来说，大小前缀将简化识别，因为它会添加到指示器集。但是，也可以预期此类攻击者读取或参与 RLPx Discovery 流量，这足以阻止 RLPx TCP 连接，无论其格式如何。

### 向后兼容性

此 EIP 是向后兼容的，所有有效的版本 4 数据包仍然可以接受。

### 实现

[go-ethereum](https://github.com/ethereum/go-ethereum/pull/2091)
[libweb3core](https://github.com/ethereum/libweb3core/pull/46)
[pydevp2p](https://github.com/ethereum/pydevp2p/pull/32)

### 测试向量

#### devp2p 基本协议

devp2p hello 数据包，宣传版本 22 并包含一些其他列表元素：

```text
f87137916b6e6574682f76302e39312f706c616e39cdc5836574683dc6846d6f726b1682270fb840
fda1cff674c90c9a197539fe3dfb53086ace64f83ed7c6eabec741f7f381cc803e52ab2cd55d5569
bce4347107a310dfd5f88a010cd2ffd1005ca406f1842877c883666f6f836261720304
```

#### RLPx Discovery Protocol

实现应接受以下编码的 discovery 数据包作为有效数据包。
这些数据包使用 secp256k1 节点密钥签名

```text
b71c71a67e1177ad4e901695e1b4b9ee17ae16c6668d313eac2f96dbcda3f291
```

带有版本 4 和其他列表元素的 ping 数据包：

```text
e9614ccfd9fc3e74360018522d30e1419a143407ffcce748de3e22116b7e8dc92ff74788c0b6663a
aa3d67d641936511c8f8d6ad8698b820a7cf9e1be7155e9a241f556658c55428ec0563514365799a
4be2be5a685a80971ddcfa80cb422cdd0101ec04cb847f000001820cfa8215a8d790000000000000
000000000000000000018208ae820d058443b9a3550102
```

带有版本 555、其他列表元素和其他随机数据的 ping 数据包：

```text
577be4349c4dd26768081f58de4c6f375a7a22f3f7adda654d1428637412c3d7fe917cadc56d4e5e
7ffae1dbe3efffb9849feb71b262de37977e7c7a44e677295680e9e38ab26bee2fcbae207fba3ff3
d74069a50b902a82c9903ed37cc993c50001f83e82022bd79020010db83c4d001500000000abcdef
12820cfa8215a8d79020010db885a308d313198a2e037073488208ae82823a8443b9a355c5010203
040531b9019afde696e582a78fa8d95ea13ce3297d4afb8ba6433e4154caa5ac6431af1b80ba7602
3fa4090c408f6b4bc3701562c031041d4702971d102c9ab7fa5eed4cd6bab8f7af956f7d565ee191
7084a95398b6a21eac920fe3dd1345ec0a7ef39367ee69ddf092cbfe5b93e5e568ebc491983c09c7
6d922dc3
```

带有其他列表元素和其他随机数据的 pong 数据包：

```text
09b2428d83348d27cdf7064ad9024f526cebc19e4958f0fdad87c15eb598dd61d08423e0bf66b206
9869e1724125f820d851c136684082774f870e614d95a2855d000f05d1648b2d5945470bc187c2d2
216fbe870f43ed0909009882e176a46b0102f846d79020010db885a308d313198a2e037073488208
ae82823aa0fbc914b16819237dcd8801d7e53f69e9719adecb3cc0e790c57e91ca4461c9548443b9
a355c6010203c2040506a0c969a58f6f9095004c0177a6b47f451530cab38966a25cca5cb58f0555
42124e
```

带有其他列表元素和其他随机数据的 findnode 数据包：

```text
c7c44041b9f7c7e41934417ebac9a8e1a4c6298f74553f2fcfdcae6ed6fe53163eb3d2b52e39fe91
831b8a927bf4fc222c3902202027e5e9eb812195f95d20061ef5cd31d502e47ecb61183f74a504fe
04c51e73df81f25c4d506b26db4517490103f84eb840ca634cae0d49acb401d8a4c6b6fe8c55b70d
115bf400769cc1400f3258cd31387574077f301b421bc84df7266c44e9e6d569fc56be0081290476
7bf5ccd1fc7f8443b9a35582999983999999280dc62cc8255c73471e0a61da0c89acdc0e035e260a
dd7fc0c04ad9ebf3919644c91cb247affc82b69bd2ca235c71eab8e49737c937a2c396
```

带有其他列表元素和其他随机数据的 neighbours 数据包：

```text
c679fc8fe0b8b12f06577f2e802d34f6fa257e6137a995f6f4cbfc9ee50ed3710faf6e66f932c4c8
d81d64343f429651328758b47d3dbc02c4042f0fff6946a50f4a49037a72bb550f3a7872363a83e1
b9ee6469856c24eb4ef80b7535bcf99c0004f9015bf90150f84d846321163782115c82115db84031
55e1427f85f10a5c9a7755877748041af1bcd8d474ec065eb33df57a97babf54bfd2103575fa8291
15d224c523596b401065a97f74010610fce76382c0bf32f84984010203040101b840312c55512422
cf9b8a4097e9a6ad79402e87a15ae909a4bfefa22398f03d20951933beea1e4dfa6f968212385e82
9f04c2d314fc2d4e255e0d3bc08792b069dbf8599020010db83c4d001500000000abcdef12820d05
820d05b84038643200b172dcfef857492156971f0e6aa2c538d8b74010f8e140811d53b98c765dd2
d96126051913f44582e8c199ad7c6d6819e9a56483f637feaac9448aacf8599020010db885a308d3
13198a2e037073488203e78203e8b8408dcab8618c3253b558d459da53bd8fa68935a719aff8b811
197101a4b2b47dd2d47295286fc00cc081bb542d760717d1bdd6bec2c37cd72eca367d6dd3b9df73
8443b9a355010203b525a138aa34383fec3d2719a0
```

#### RLPx 握手

在这些测试向量中，节点 A 发起与节点 B 的连接。
所有数据包中包含的值如下：

```text
静态密钥 A：    49a7b37aa6f6645917e7b807e9d1c00d4fa71f18343b0d4122a4d2df64dd6fee
静态密钥 B：    b71c71a67e1177ad4e901695e1b4b9ee17ae16c6668d313eac2f96dbcda3f291
临时密钥 A： 869d6ecf5211f1cc60418a13b9d870b22959d0c16f02bec714c960dd2298a32d
临时密钥 B： e238eb8e04fee6511ab04c6dd3c89ce097b11f25d584863ac2b6d5b35b1847e4
Nonce A:         7e968bba13b6c50e2c4cd7f241cc0d64d1ac25c7f5952df231ac6a2bda8ee5d6
Nonce B:         559aead08264d5795d3909718cdd05abd49572e84fe55590eef31a88a08fdffd
```

(Auth₁)  RLPx v4 格式（从 A 发送到 B）：
```text
048ca79ad18e4b0659fab4853fe5bc58eb83992980f4c9cc147d2aa31532efd29a3d3dc6a3d89eaf
913150cfc777ce0ce4af2758bf4810235f6e6ceccfee1acc6b22c005e9e3a49d6448610a58e98744
ba3ac0399e82692d67c1f58849050b3024e21a52c9d3b01d871ff5f210817912773e610443a9ef14
2e91cdba0bd77b5fdf0769b05671fc35f83d83e4d3b0b000c6b2a1b1bba89e0fc51bf4e460df3105
c444f14be226458940d6061c296350937ffd5e3acaceeaaefd3c6f74be8e23e0f45163cc7ebd7622
0f0128410fd05250273156d548a414444ae2f7dea4dfca2d43c057adb701a715bf59f6fb66b2d1d2
0f2c703f851cbf5ac47396d9ca65b6260bd141ac4d53e2de585a73d1750780db4c9ee4cd4d225173
a4592ee77e2bd94d0be3691f3b406f9bba9b591fc63facc016bfa8
```

(Auth₂) EIP-8 格式，版本为 4，没有其他列表元素（从 A 发送到 B）：
```text
01b304ab7578555167be8154d5cc456f567d5ba302662433674222360f08d5f1534499d3678b513b
0fca474f3a514b18e75683032eb63fccb16c156dc6eb2c0b1593f0d84ac74f6e475f1b8d56116b84
9634a8c458705bf83a626ea0384d4d7341aae591fae42ce6bd5c850bfe0b999a694a49bbbaf3ef6c
da61110601d3b4c02ab6c30437257a6e0117792631a4b47c1d52fc0f8f89caadeb7d02770bf999cc
147d2df3b62e1ffb2c9d8c125a3984865356266bca11ce7d3a688663a51d82defaa8aad69da39ab6
d5470e81ec5f2a7a47fb865ff7cca21516f9299a07b1bc63ba56c7a1a892112841ca44b6e0034dee
70c9adabc15d76a54f443593fafdc3b27af8059703f88928e199cb122362a4b35f62386da7caad09
c001edaeb5f8a06d2b26fb6cb93c52a9fca51853b68193916982358fe1e5369e249875bb8d0d0ec3
6f917bc5e1eafd5896d46bd61ff23f1a863a8a8dcd54c7b109b771c8e61ec9c8908c733c0263440e
2aa067241aaa433f0bb053c7b31a838504b148f570c0ad62837129e547678c5190341e4f1693956c
3bf7678318e2d5b5340c9e488eefea198576344afbdf66db5f51204a6961a63ce072c8926c
```

(Auth₃) EIP-8 格式，版本为 56，带有 3 个其他列表元素（从 A 发送到 B）：
```text
01b8044c6c312173685d1edd268aa95e1d495474c6959bcdd10067ba4c9013df9e40ff45f5bfd6f7
2471f93a91b493f8e00abc4b80f682973de715d77ba3a005a242eb859f9a211d93a347fa64b597bf
280a6b88e26299cf263b01b8dfdb712278464fd1c25840b995e84d367d743f66c0e54a586725b7bb
f12acca27170ae3283c1073adda4b6d79f27656993aefccf16e0d0409fe07db2dc398a1b7e8ee93b
cd181485fd332f381d6a050fba4c7641a5112ac1b0b61168d20f01b479e19adf7fdbfa0905f63352
bfc7e23cf3357657455119d879c78d3cf8c8c06375f3f7d4861aa02a122467e069acaf513025ff19
6641f6d2810ce493f51bee9c966b15c5043505350392b57645385a18c78f14669cc4d960446c1757
1b7c5d725021babbcd786957f3d17089c084907bda22c2b2675b4378b114c601d858802a55345a15
116bc61da4193996187ed70d16730e9ae6b3bb8787ebcaea1871d850997ddc08b4f4ea668fbf3740
7ac044b55be0908ecb94d4ed172ece66fd31bfdadf2b97a8bc690163ee11f5b575a4b44e36e2bfb2
f0fce91676fd64c7773bac6a003f481fddd0bae0a1f31aa27504e2a533af4cef3b623f4791b2cca6
d490
```

(Ack₁) RLPx v4 格式（从 B 发送到 A）：
```text
049f8abcfa9c0dc65b982e98af921bc0ba6e4243169348a236abe9df5f93aa69d99cadddaa387662
b0ff2c08e9006d5a11a278b1b3331e5aaabf0a32f01281b6f4ede0e09a2d5f585b26513cb794d963
5a57563921c04a9090b4f14ee42be1a5461049af4ea7a7f49bf4c97a352d39c8d02ee4acc416388c
1c66cec761d2bc1c72da6ba143477f049c9d2dde846c252c111b904f630ac98e51609b3b1f58168d
dca6505b7196532e5f85b259a20c45e1979491683fee108e9660edbf38f3add489ae73e3dda2c71b
d1497113d5c755e942d1
```

(Ack₂) EIP-8 格式，版本为 4，没有其他列表元素（从 B 发送到 A）：
```text
01ea0451958701280a56482929d3b0757da8f7fbe5286784beead59d95089c217c9b917788989470
b0e330cc6e4fb383c0340ed85fab836ec9fb8a49672712aeabbdfd1e837c1ff4cace34311cd7f4de
05d59279e3524ab26ef753a0095637ac88f2b499b9914b5f64e143eae548a1066e14cd2f4bd7f814
c4652f11b254f8a2d0191e2f5546fae6055694aed14d906df79ad3b407d94692694