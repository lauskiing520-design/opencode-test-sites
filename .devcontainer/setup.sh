#!/bin/bash
set -e

echo "=== 临时测试站初始化 ==="

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

# 用 python3 啟動 HTTP server（codespace 一定內建）
echo "=== 啟動 web server (port 8080) ==="
# 用 setsid 徹底分離，避免被 hook 結束時殺掉
setsid nohup python3 -m http.server 8080 --directory /workspaces/www --bind 0.0.0.0 > /tmp/webserver.log 2>&1 < /dev/null &

sleep 2
echo "=== server status ==="
ps aux | grep "http.server" | grep -v grep || echo "SERVER-NOT-RUNNING"
echo "=== log ==="
cat /tmp/webserver.log 2>/dev/null || true
echo "=== 完成！==="
echo "網頁根目錄: /workspaces/www"
