# -*- coding: utf-8 -*-
"""Seedance 影片生成工作台 - Flask 網頁介面"""
import os
import time
import requests
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

ARK_API_KEY = os.environ.get("ARK_API_KEY", "")
BASE_URL = "https://ark.ap-southeast.bytepluses.com"
MODEL = "dreamina-seedance-2-0-fast-260128"
HEADERS = {
    "Authorization": f"Bearer {ARK_API_KEY}",
    "Content-Type": "application/json",
}

if not ARK_API_KEY:
    print("WARNING: ARK_API_KEY 未設定，請在 Codespaces 環境變數設定")

PAGE = """
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>影片生成工作台</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, "Microsoft JhengHei", sans-serif; background: linear-gradient(135deg,#1a1a2e,#16213e); min-height:100vh; color:#eee; display:flex; align-items:center; justify-content:center; padding:20px; }
  .card { background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.12); border-radius:16px; padding:32px; width:100%; max-width:560px; box-shadow:0 20px 60px rgba(0,0,0,.4); }
  h1 { font-size:22px; margin-bottom:6px; }
  .sub { color:#9aa; font-size:13px; margin-bottom:20px; }
  textarea { width:100%; min-height:110px; background:rgba(0,0,0,.3); border:1px solid rgba(255,255,255,.15); border-radius:10px; color:#fff; padding:14px; font-size:14px; resize:vertical; font-family:inherit; }
  .row { display:flex; gap:10px; margin-top:12px; align-items:center; flex-wrap:wrap; }
  select { background:rgba(0,0,0,.3); border:1px solid rgba(255,255,255,.15); color:#fff; padding:10px; border-radius:8px; font-size:14px; }
  button { background:#4f7cff; color:#fff; border:none; padding:12px 26px; border-radius:10px; font-size:15px; font-weight:600; cursor:pointer; margin-left:auto; }
  button:hover { background:#3d67e0; }
  button:disabled { background:#555; cursor:not-allowed; }
  #status { margin-top:16px; font-size:14px; color:#8cf; min-height:20px; white-space:pre-line; }
  #result { margin-top:16px; text-align:center; }
  video { width:100%; max-width:360px; border-radius:12px; margin-top:10px; }
  .hint { margin-top:18px; font-size:12px; color:#667; line-height:1.6; border-top:1px solid rgba(255,255,255,.08); padding-top:14px; }
</style>
</head>
<body>
<div class="card">
  <h1>🎬 Seedance 影片生成</h1>
  <div class="sub">輸入畫面描述，生成 5/10 秒短影片（無聲音）</div>

  <textarea id="prompt" placeholder="描述你想生成的畫面，例：一位中醫師將草藥茶倒入陶杯，蒸氣升起，暖黃窗光"></textarea>

  <div class="row">
    <select id="duration">
      <option value="5">5 秒</option>
      <option value="10">10 秒</option>
    </select>
    <select id="ratio">
      <option value="9:16">9:16 直式</option>
      <option value="16:9">16:9 橫式</option>
      <option value="1:1">1:1 方形</option>
    </select>
    <select id="res">
      <option value="480p">480p</option>
      <option value="720p" selected>720p</option>
      <option value="1080p">1080p</option>
    </select>
    <button id="btn" onclick="generate()">生成影片</button>
  </div>

  <div id="status"></div>
  <div id="result"></div>

  <div class="hint">
    提示：描述越像「分鏡」效果越好——主題動作 + 運鏡 + 光線 + 風格。<br>
    每次生成都需約 1-3 分鐘渲染，費用依解析度與秒數計算。
  </div>
</div>

<script>
async function generate() {
  const btn = document.getElementById('btn');
  const prompt = document.getElementById('prompt').value.trim();
  if (!prompt) { alert('請先輸入描述'); return; }
  btn.disabled = true;
  document.getElementById('result').innerHTML = '';
  setStatus('📤 提交任務中...');

  try {
    const r = await fetch('/api/generate', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        prompt: prompt,
        duration: document.getElementById('duration').value,
        ratio: document.getElementById('ratio').value,
        res: document.getElementById('res').value
      })
    });
    const data = await r.json();
    if (!r.ok) { throw new Error(data.error || '提交失敗'); }
    setStatus('✅ 任務已提交，渲染中（約 1-3 分鐘）...');

    // 輪詢
    const taskId = data.task_id;
    const start = Date.now();
    while (Date.now() - start < 600000) {
      await sleep(8000);
      const q = await fetch('/api/status/' + taskId);
      const st = await q.json();
      if (st.status === 'succeeded' && st.video_url) {
        showVideo(st.video_url, taskId);
        return;
      } else if (st.status === 'failed') {
        throw new Error('生成失敗：' + (st.error || '未知原因'));
      }
    }
    throw new Error('超過 10 分鐘未完成，任務可能仍在伺服器渲染中');
  } catch (e) {
    setStatus('❌ ' + e.message);
  } finally {
    btn.disabled = false;
  }
}

function showVideo(url, taskId) {
  const el = document.getElementById('result');
  el.innerHTML = `<p style="color:#8c8">✅ 生成完成</p>
    <video controls src="${url}"></video>
    <p style="margin-top:10px"><a href="${url}" download style="color:#8cf">⬇️ 下載影片</a></p>
    <p style="font-size:11px;color:#667">（影片連結約 24 小時內有效，請盡快下載）</p>`;
  setStatus('');
}

function setStatus(t) { document.getElementById('status').textContent = t; }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(PAGE)


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = (data.get("prompt") or "").strip()
    if not prompt:
        return jsonify({"error": "描述不能為空"}), 400
    duration = data.get("duration", "5")
    ratio = data.get("ratio", "9:16")
    res = data.get("res", "720p")
    # ModelArk 用 --flags 附在 prompt 字串
    full_prompt = f"{prompt} --duration {duration} --ratio {ratio} --resolution {res}"
    payload = {
        "model": MODEL,
        "content": [{"type": "text", "text": full_prompt}],
    }
    try:
        r = requests.post(f"{BASE_URL}/api/v3/contents/generations/tasks",
                          json=payload, headers=HEADERS, timeout=30)
        body = r.json()
        if "id" not in body:
            return jsonify({"error": f"API 錯誤: {body}"}), 500
        return jsonify({"task_id": body["id"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status/<task_id>")
def status(task_id):
    try:
        r = requests.get(f"{BASE_URL}/api/v3/contents/generations/tasks/{task_id}",
                         headers=HEADERS, timeout=30)
        body = r.json()
        status = body.get("status")
        if status == "succeeded":
            content = body.get("content") or {}
            video_url = content.get("video_url")
            return jsonify({"status": "succeeded", "video_url": video_url})
        elif status == "failed":
            return jsonify({"status": "failed",
                            "error": (body.get("error") or {}).get("message", "unknown")})
        return jsonify({"status": status})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
