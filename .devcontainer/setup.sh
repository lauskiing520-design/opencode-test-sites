#!/bin/bash
# 臨時測試站初始化（Codespaces postCreateCommand 執行）
set -x

# 安裝 python3（base image 沒有，需 sudo）
if ! command -v python3 &>/dev/null; then
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip
fi

# 安裝 Flask
pip3 install flask requests --break-system-packages 2>/dev/null || pip3 install flask requests

# 工作台根目錄
mkdir -p /workspaces/www
cat > /workspaces/www/index.html <<'EOF'
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>臨時測試站</title></head>
<body><h1>臨時測試站</h1><p>Seedance 工作台在 <a href="/seedance">/seedance</a></p></body></html>
EOF

# 啟動 Seedance 工作台（Flask，port 8080）
echo "=== 啟動 Seedance 工作台 (port 8080) ==="
setsid nohup python3 /workspaces/opencode-test-sites/seedance_workbench/app.py > /tmp/seedance.log 2>&1 < /dev/null &

sleep 3
echo "=== PS ==="
ps aux | grep "app.py" | grep -v grep || echo "NOT RUNNING"
echo "=== LOG ==="
cat /tmp/seedance.log 2>/dev/null || echo "NO LOG"
echo "=== DONE ==="
