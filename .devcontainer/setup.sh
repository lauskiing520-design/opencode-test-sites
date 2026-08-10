#!/bin/bash
# 臨時測試站初始化（Codespaces postCreateCommand 執行，只跑一次）
set -x

# 安裝 python3（base image 沒有，需 sudo）
if ! command -v python3 &>/dev/null; then
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip
fi

# 安裝 Flask
pip3 install flask requests --break-system-packages 2>/dev/null || pip3 install flask requests

# 測試站根目錄
mkdir -p /workspaces/www
cat > /workspaces/www/index.html <<'EOF'
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>臨時測試站</title></head>
<body><h1>臨時測試站</h1><p>Seedance 工作台在根路徑 /</p></body></html>
EOF

echo "=== 初始化完成，工作台由 start.sh 啟動 ==="
