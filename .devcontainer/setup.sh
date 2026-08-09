#!/bin/bash
# 臨時測試站初始化（Codespaces postCreateCommand 執行）
set -x
mkdir -p /workspaces/www
cat > /workspaces/www/index.html <<'EOF'
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>临时测试站</title></head>
<body><h1>临时测试站 OK</h1></body></html>
EOF
which python3 || apt-get update && apt-get install -y python3
setsid nohup python3 -m http.server 8080 --directory /workspaces/www --bind 0.0.0.0 > /tmp/web.log 2>&1 < /dev/null &
sleep 2
echo "=== PS ==="
ps aux | grep http.server | grep -v grep || echo "NOT RUNNING"
echo "=== LOG ==="
cat /tmp/web.log 2>/dev/null || echo "NO LOG"
echo "=== DONE ==="
