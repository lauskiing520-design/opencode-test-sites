#!/bin/bash
# 臨時測試站初始化（Codespaces postCreateCommand 執行）
set -x

# 建立測試站根目錄
mkdir -p /workspaces/www

# 預設 index.html
cat > /workspaces/www/index.html <<'EOF'
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>临时测试站</title></head>
<body>
<h1>临时测试站已啟動</h1>
<p>把你的 HTML 檔案放到 <code>/workspaces/www/</code> 即可訪問</p>
</body>
</html>
EOF

# 安裝 python3（base image 沒有，需 sudo）
if ! command -v python3 &>/dev/null; then
  sudo apt-get update
  sudo apt-get install -y python3
fi

# 啟動 HTTP server（setsid 分離避免被終止）
setsid nohup python3 -m http.server 8080 --directory /workspaces/www --bind 0.0.0.0 > /tmp/web.log 2>&1 < /dev/null &
sleep 2

echo "=== PS ==="
ps aux | grep http.server | grep -v grep || echo "NOT RUNNING"
echo "=== LOG ==="
cat /tmp/web.log 2>/dev/null || echo "NO LOG"
echo "=== DONE ==="
