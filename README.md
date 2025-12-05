# AI / Human 文章偵測器 — 本地執行與截圖指南

這個目錄為簡化用的範例 repo（`ai-human-detector-clean`），包含訓練腳本與 Streamlit demo。下面的指令能讓你在本地完整執行 demo、產生模型、並截圖放入 repo 以便提交作業。

目錄（重點）
- `src/train_model.py` — 訓練 TF-IDF + LogisticRegression 的腳本
- `streamlit_app.py` — Streamlit 應用，能載入 `models/ai_detector.joblib` 並對輸入文字做 AI/Human 機率判斷
- `requirements.txt` — 執行所需套件
- `data/ai_human_text.csv` — 範例資料（若有）
- `models/` — 訓練後會產生 `ai_detector.joblib`
- `screenshot-placeholder.svg` — 截圖佔位檔（請以實際截圖替換）

快速執行（本機）
1. Clone 或確認你已在本地 repo 資料夾：
```powershell
# 切換到專案資料夾（請改成你本機上 clone 的路徑）
cd <path-to-your-cloned-repo>/ai-human-detector-clean
```

2. 建立並啟動虛擬環境（第一次需要）
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. 安裝相依
```powershell
pip install -r requirements.txt
```

4. 若你已有 `models/ai_detector.joblib`（直接測試）
```powershell
# 確認檔案存在
Test-Path .\models\ai_detector.joblib
streamlit run streamlit_app.py
```

5. 若沒有模型，執行訓練以產生模型（會在 `models/` 生成）：
```powershell
python src\train_model.py
streamlit run streamlit_app.py
```

6. 在瀏覽器開啟 `http://localhost:8501`，貼一段文字後按「開始分析」即可看到 AI% / Human% 與進度條。

如何截圖並放入 repo
1. 在瀏覽器顯示你希望的畫面（例如分析結果），按下 `Win + Shift + S`（Windows）擷取畫面，存成 `screenshot.png`。
2. 把檔案放到本專案根目錄（與 `README.md` 同層）：
```powershell
Move-Item -Path C:\Users\<you>\Desktop\screenshot.png -Destination .\screenshot.png
git add screenshot.png
git commit -m "Add demo screenshot"
git push
```

（已提供）示範佔位圖：`screenshot-placeholder.svg`。請把它替換為你實際的 `screenshot.png`。

上傳模型到 GitHub Release（方便 Streamlit Cloud 下載）
- 若你想讓 Streamlit Cloud 直接下載模型並在部署時使用，先把 `models/ai_detector.joblib` 上傳到 GitHub Release（或其他可直接下載的 host）。
- 我們建議使用 `gh`（GitHub CLI）：
```powershell
# 在本機執行（請先 `cd` 到你的專案資料夾）
# 範例：
# cd C:\Users\<you>\projects\ai-human-detector-clean
gh auth login        # 互動式登入（若尚未登入）
gh release create v1.0 .\models\ai_detector.joblib --repo MINGCHUNSHIH/AIOTHW5 --title "ai_detector v1.0" --notes "Pretrained model for Streamlit demo"
```
- Release 的下載連結通常是：
```
https://github.com/MINGCHUNSHIH/AIOTHW5/releases/download/v1.0/ai_detector.joblib
```

在 Streamlit Cloud 設定 `MODEL_URL`（部署時）
1. 登入 https://share.streamlit.io → 選你的 App → Settings → Secrets。
2. 新增 `MODEL_URL` key，value 設為 Release 的下載連結。
3. 重新部署 App，若 App 在啟動時找不到本地模型，會顯示「下載並載入模型」按鈕，點擊後會把模型下載到 `models/ai_detector.joblib`。

本 README 中的範例指令都已在本地測試過（包含訓練與啟動流程）。



模型上傳與 Streamlit Cloud 的建議處理

- 不建議把訓練好的 `models/ai_detector.joblib` 直接放在公開的 Git repository（檔案較大且非原始碼）。
- 建議把模型檔上傳到 GitHub Release（或其他能取得直鏈的雲端儲存，如 Google Drive / Dropbox），然後在 Streamlit App 啟動時下載模型。

如何建立 GitHub Release（手動）：

1. 到你在 GitHub 的 repo 頁面 → 點選 `Releases` → `Draft a new release`。
2. 填寫 tag（例如 `v1.0`）、標題與描述。
3. 在 `Attach binaries by dropping them here or selecting them.` 區塊上傳 `ai_detector.joblib`。
4. Publish release，複製附件（Release asset）的 `Download` 連結。

在 Streamlit Cloud 設定模型 URL：

1. 到 Streamlit Cloud 的你的 app → Settings → Secrets。新增一個 secret key 叫 `MODEL_URL`，value 填 Release 的下載 URL（或其他可直連檔案的 URL）。
2. 部署的 app 在啟動時若找不到本地模型會顯示下載按鈕，按下後即可下載並儲存到 `models/ai_detector.joblib`。

本地如何測試下載流程（如果你先把模型上傳到某個 URL）：

```powershell
# 在你的專案資料夾執行（請先 `cd` 到專案資料夾）
# 設定環境變數（範例，PowerShell）
$env:MODEL_URL = "https://github.com/<you>/<repo>/releases/download/v1.0/ai_detector.joblib"
streamlit run streamlit_app.py
```

備註：`streamlit_app.py` 已支援從 `st.secrets['MODEL_URL']` 或環境變數 `MODEL_URL` 下載模型，若找不到模型會顯示下載選項。


