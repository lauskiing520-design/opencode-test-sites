# 臨時測試站模板（GitHub Codespaces）

每個測試站 = 一個獨立 Codespaces 環境，**用完即刪、完全不碰正式伺服器**。

## 怎麼用

### 第一次（建 repo + 開環境）
1. 到 GitHub 網頁建一個**空倉庫**（例如 `test-site-1`）
2. 把本資料夾裡的 `.devcontainer/`（devcontainer.json + setup.sh）**上傳到 repo 根目錄**
3. 在 repo 頁面 → **Code → Codespaces → Create codespace on main**
4. 環境建立中（約 1-2 分鐘），自動裝好 PHP + Node + opencode + web server

### 之後每次（開新測試站）
1. 建立**新 repo**（或複製模板 repo）→ 開 Codespaces
2. 把你的 HTML/PHP 上傳到 `/workspaces/www/`
3. 看 VS Code **底部 Ports 面板** → 點 8080 端口的鏈接（格式 `https://xxxx-8080.app.github.dev`）
4. 瀏覽器就能訪問你的測試站

### 用完
- 直接關閉/刪除該 Codespaces 環境即可，什麼都不殘留
- 對正式伺服器零影響

## 可改的設定
- **`devcontainer.json` 的 `forwardPorts` / `portsAttributes`**：改端口號（PHP 預設 8080）
- **`setup.sh`**：可改成自動跑 Python server（`python3 -m http.server`）或 Node 伺服器

## 注意
- 每個 Codespaces 都有**免費額度**（個人每月 60 小時），用完會收費——測完記得刪
- 如果你有 PHP 以外的需求（例如 MySQL、Python 框架），需要改 devcontainer.json 的 features
