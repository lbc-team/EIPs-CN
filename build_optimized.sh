#!/bin/bash

echo "🚀 开始完整构建和优化流程..."

# 设置Ruby路径
export PATH="/usr/local/opt/ruby@3.1/bin:$PATH"

# 清理旧文件
echo "🧹 清理旧的构建文件..."
rm -rf _site optimized_site final_deployment

# 构建Jekyll站点
echo "🔨 构建Jekyll站点..."
bundle exec jekyll build

if [ $? -ne 0 ]; then
    echo "❌ Jekyll构建失败"
    exit 1
fi

# 运行优化脚本
echo "⚡ 运行优化脚本..."
./optimize_build.sh

# 创建最终部署目录
echo "📦 创建最终部署目录..."
mkdir -p final_deployment
cp -r optimized_site/* final_deployment/

# 显示最终结果
echo "📊 最终构建结果："
echo "最终部署包大小: $(du -sh final_deployment | cut -f1)"
echo "文件数量: $(find final_deployment -type f | wc -l)"

echo "✅ 构建完成！"
echo "📁 部署文件位于: final_deployment/"
echo "🚀 可以直接上传到服务器的 /home/www/tipask/public/docs/eips/ 目录"

# 提供上传命令
echo ""
echo "📤 上传命令："
echo "scp -P 901 -r final_deployment/* lbc:/home/www/tipask/public/docs/eips/" 