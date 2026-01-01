#!/bin/bash
set -e

REPO_ROOT=$(git rev-parse --show-toplevel)
MARKETPLACE="$REPO_ROOT/.claude-plugin/marketplace.json"

# 开始生成
cat > "$MARKETPLACE" << 'EOF'
{
  "name": "geraldpeng6-plugins",
  "owner": {
    "name": "geraldpeng6"
  },
  "plugins": [
EOF

first=true
for dir in "$REPO_ROOT"/*/; do
  plugin_json="${dir}.claude-plugin/plugin.json"
  if [ -f "$plugin_json" ]; then
    name=$(basename "$dir")
    desc=$(jq -r '.description // ""' "$plugin_json")
    ver=$(jq -r '.version // "0.1.0"' "$plugin_json")

    if [ "$first" = true ]; then
      first=false
    else
      # 在上一个对象后添加逗号
      sed -i '' '$ s/}$/},/' "$MARKETPLACE"
    fi

    cat >> "$MARKETPLACE" << EOF
    {
      "name": "$name",
      "source": "./$name",
      "description": "$desc",
      "version": "$ver",
      "license": "MIT"
    }
EOF
  fi
done

echo -e "\n  ]\n}" >> "$MARKETPLACE"

# 自动 stage 更新的文件
git add "$MARKETPLACE"
echo "✓ marketplace.json synced"
