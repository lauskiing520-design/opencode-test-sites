#!/bin/bash
# 啟動 Seedance 工作台（postStartCommand 執行，每次啟動都跑）
set -x

# 確保 Flask 已裝
pip3 list 2>/dev/null | grep -q flask || pip3 install flask requests --break-system-packages 2>/dev/null || pip3 install flask requests

mkdir -p /workspaces/www

# 停掉舊的 Flask（精確匹配 python 進程，避免殺到自己）
pkill -f "python3.*seedance_workbench" 2>/dev/null || true
pkill -f "http.server 8080" 2>/dev/null || true

# 啟動 Seedance 工作台（key 從環境變數 ARK_API_KEY 讀取）
cd /workspaces/opencode-test-sites
echo "=== 啟動 Seedance 工作台 (port 8080) ==="
setsid nohup python3 seedance_workbench/app.py > /tmp/seedance.log 2>&1 < /dev/null &

sleep 3
echo "=== PS ==="
ps aux | grep "app.py" | grep -v grep || echo "NOT RUNNING"
echo "=== LOG ==="
cat /tmp/seedance.log 2>/dev/null || echo "NO LOG"
echo "=== DONE ==="
