#!/bin/bash
set -e

echo "=== 临时测试站初始化 ==="

# 建立測試站根目錄（指向工作區根，方便直接把 HTML 放這裡）
mkdir -p /workspaces/www

# 放一個預設 index.html 當佔位
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

# 啟動 PHP 內建伺服器（支援 PHP + 靜態檔）
echo "=== 啟動 web server (port 8080) ==="
nohup php -S 0.0.0.0:8080 -t /workspaces/www > /tmp/phpserver.log 2>&1 &

echo "=== 完成！==="
echo "網頁根目錄: /workspaces/www"
echo "訪問網址: 看 VS Code 底部的 Ports 面板，點 8080 端口的鏈接"
