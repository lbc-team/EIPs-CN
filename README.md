# Ethereum Improvement Proposals (EIPs)

> **_ATTENTION_**: The EIPs repository has recently [undergone](https://github.com/ethereum/EIPs/pull/7206) a separation of ERCs and EIPs. ERCs are now accessible at [https://github.com/ethereum/ercs](https://github.com/ethereum/ercs). All new ERCs and updates to existing ones must be directed at this new repository. The editors apologize for this inconvenience.

The goal of the EIP project is to standardize and provide high-quality documentation for Ethereum itself and conventions built upon it. This repository tracks past and ongoing improvements to Ethereum in the form of Ethereum Improvement Proposals (EIPs). [EIP-1](https://eips.ethereum.org/EIPS/eip-1) governs how EIPs are published.

The [status page](https://eips.ethereum.org/) tracks and lists EIPs, which can be divided into the following categories:

- [Core EIPs](https://eips.ethereum.org/core) are improvements to the Ethereum consensus protocol.
- [Networking EIPs](https://eips.ethereum.org/networking) specify the peer-to-peer networking layer of Ethereum.
- [Interface EIPs](https://eips.ethereum.org/interface) standardize interfaces to Ethereum, which determine how users and applications interact with the blockchain.
- [ERCs](https://eips.ethereum.org/erc) specify application layer standards, which determine how applications running on Ethereum can interact with each other.
- [Meta EIPs](https://eips.ethereum.org/meta) are miscellaneous improvements that nonetheless require some sort of consensus.
- [Informational EIPs](https://eips.ethereum.org/informational) are non-standard improvements that do not require any form of consensus.

**Before you write an EIP, ideas MUST be thoroughly discussed on [Ethereum Magicians](https://ethereum-magicians.org/) or [Ethereum Research](https://ethresear.ch/t/read-this-before-posting/8). Once consensus is reached, thoroughly read and review [EIP-1](https://eips.ethereum.org/EIPS/eip-1), which describes the EIP process.**

Please note that this repository is for documenting standards and not for help implementing them. These types of inquiries should be directed to the [Ethereum Stack Exchange](https://ethereum.stackexchange.com). For specific questions and concerns regarding EIPs, it's best to comment on the relevant discussion thread of the EIP denoted by the `discussions-to` tag in the EIP's preamble.

If you would like to become an EIP Editor, please read [EIP-5069](./EIPS/eip-5069.md).

## Preferred Citation Format

The canonical URL for an EIP that has achieved draft status at any point is at <https://eips.ethereum.org/>. For example, the canonical URL for EIP-1 is <https://eips.ethereum.org/EIPS/eip-1>.

Consider any document not published at <https://eips.ethereum.org/> as a working paper. Additionally, consider published EIPs with a status of "draft", "review", or "last call" to be incomplete drafts, and note that their specification is likely to be subject to change.

## Validation and Automerging

All pull requests in this repository must pass automated checks before they can be automatically merged:

- [eip-review-bot](https://github.com/ethereum/eip-review-bot/) determines when PRs can be automatically merged [^1]
- EIP-1 rules are enforced using [`eipw`](https://github.com/ethereum/eipw)[^2]
- HTML formatting and broken links are enforced using [HTMLProofer](https://github.com/gjtorikian/html-proofer)[^2]
- Spelling is enforced with [CodeSpell](https://github.com/codespell-project/codespell)[^2]
  - False positives sometimes occur. When this happens, please submit a PR editing [.codespell-whitelist](https://github.com/ethereum/EIPs/blob/master/config/.codespell-whitelist) and **ONLY** .codespell-whitelist
- Markdown best practices are checked using [markdownlint](https://github.com/DavidAnson/markdownlint)[^2]

[^1]: https://github.com/ethereum/EIPs/blob/master/.github/workflows/auto-review-bot.yml
[^2]: https://github.com/ethereum/EIPs/blob/master/.github/workflows/ci.yml

It is possible to run the EIP validator locally:

Make sure to add cargo's `bin` directory to your environment (typically `$HOME/.cargo/bin` in your `PATH` environment variable)

```sh
cargo install eipw
eipw --config ./config/eipw.toml <INPUT FILE / DIRECTORY>
```

## Build the status page locally

### Install prerequisites

1. Open Terminal.

2. Check whether you have Ruby 3.1.4 installed. Later [versions are not supported](https://stackoverflow.com/questions/14351272/undefined-method-exists-for-fileclass-nomethoderror).

   ```sh
   ruby --version
   ```

3. If you don't have Ruby installed, install Ruby 3.1.4.

4. Install Bundler:

   ```sh
   gem install bundler
   ```

5. Install dependencies:

   ```sh
   bundle install
   ```

### Build your local Jekyll site

1. Bundle assets and start the server:

   ```sh
   bundle exec jekyll serve
   ```

2. Preview your local Jekyll site in your web browser at `http://localhost:4000`.

More information on Jekyll and GitHub Pages [here](https://docs.github.com/en/enterprise/2.14/user/articles/setting-up-your-github-pages-site-locally-with-jekyll).


## 合并部署

EIPS：https://github.com/ethereum/EIPs
目前ibc-team下已有eips库，但版本比较久远，需要把新的eips库clone过来，再执行翻译脚本。
● 先在自己的仓库下clone eips，尝试构建。
● 构建完成后尝试执行翻译脚本。
构建eips：
1. 这是一个以太坊改进提案(EIP)的官方网站项目
2. 使用Jekyll静态网站生成器构建
3. 当前Ruby版本是2.6.10，但文档建议使用Ruby 3.1.4
4. 需要安装bundler和依赖包
5. 然后可以用jekyll serve运行
  ● 更新ruby版本 ： 使用rbenv来管理ruby版本。
  ● 安装依赖：无法安装，切换国内镜像源。网络连接问题，无法访问rubygems.org
  https://rubygems.org/ removed from sources
  https://gems.ruby-china.com/ added to sources
  ERC无内容，因为ERC的提案单独放了个仓库，和EIPS同级：http://github.com/ethereum/ERCs。
  需要把ERCs也clone下来，在本地做合并后，作为一个项目构建。

``````
   # 合并ERC内容到EIP仓库
   cp -rp ERCs/ERCS/. EIPS/
   cp -rp ERCs/EIPS/. EIPS/  
   cp -rp ERCs/assets/. assets/
   
   # 重命名文件：erc-*.md -> eip-*.md
   find . -name "erc-*.md" -type f -exec mv {} {重命名为eip-} \;
   
   # 重命名目录：erc-* -> eip-*
   find . -name "erc-*" -type d -exec mv {} {重命名为eip-} \;
``````

合并脚本

``````
#!/bin/bash

echo "🚀 开始按照官方流程合并 ERCs 仓库..."

# 1. 复制ERCs仓库到当前目录
echo "📁 复制 ERCs 仓库..."
cp -rp ../ERCs ./

# 2. 创建必要的目录结构
echo "📂 创建目录结构..."
mkdir -p ./ERCs/ERCS
mkdir -p ./ERCs/EIPS

# 3. 合并内容到EIPS目录
echo "🔄 合并 ERC 内容到 EIPS 目录..."
cp -rp ./ERCs/ERCS/. ./EIPS/
cp -rp ./ERCs/EIPS/. ./EIPS/
cp -rp ./ERCs/assets/. ./assets/

# 4. 重命名 erc-*.md 文件为 eip-*.md
echo "🏷️  重命名 ERC 文件为 EIP 格式..."
cd ./EIPS
find . -name "erc-*.md" -type f | while read file; do
    newname=$(echo "$file" | sed 's/erc-/eip-/')
    echo "重命名: $file -> $newname"
    mv "$file" "$newname"
done

# 5. 重命名 assets 目录中的 erc-* 目录为 eip-*
echo "🗂️  重命名 assets 目录..."
cd ../assets
find . -name "erc-*" -type d | while read dir; do
    newdir=$(echo "$dir" | sed 's/erc-/eip-/')
    echo "重命名目录: $dir -> $newdir"
    mv "$dir" "$newdir"
done

# 6. 回到根目录并清理
cd ..
echo "🧹 清理临时文件..."
rm -rf ERCs

echo "✅ 合并完成！现在 EIP 和 ERC 内容已经合并到一起了。"
echo "📝 您现在可以重新启动 Jekyll 服务器查看完整内容。" 
``````

## 草案统计，截止2025.06.30

### Status统计（总共986个文档）：

- **Final** (239个) - 最终确定的标准
- **Draft** (250个) - 草案阶段
- **St****agnant** (365个) - 停滞状态
- **Review** (77个) - 同行评审阶段
- **Last Call** (17个) - 最终评审阶段
- **Withdrawn** (36个) - 已撤回
- **Living** (2个) - 持续更新状态