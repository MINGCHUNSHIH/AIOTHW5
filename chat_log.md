# Chat / Agent Conversation Log

以下為本次專案開發過程中，與 ChatGPT 助手互動的摘要（可作為 HW5 的「ChatGPT / AI Agent 對話過程」附件）。

- 需求：建立 AI vs Human 文章偵測器，使用 TF-IDF + Logistic Regression，並提供 Streamlit UI 與部署說明。
- 我（使用者）收到的協助內容包含：
  - 完整專案架構建議與檔案清單
  - `src/train_model.py` 訓練腳本範例（包含讀取 CSV、切分資料、訓練、輸出 `classification_report` 與 ROC-AUC、儲存模型）
  - `streamlit_app.py` 的範例與完整程式（可顯示 AI% / Human% 與簡單視覺化）
  - `requirements.txt` 的建議內容（`streamlit, pandas, scikit-learn, joblib, numpy`）
  - 部署步驟摘要（推上 GitHub → Streamlit Cloud 部署）

- 開發紀錄（重要互動）
  1. 我請助理把範例程式加入專案，助理在 `新增資料夾/` 中新增 `src/train_model.py`、修改 `streamlit_app.py` 為 AI Detector、更新 `requirements.txt`，並加上 `README.md`。
  2. 助理建立了一個小型示範資料 `data/ai_human_text.csv`（用於本地 demo 與測試）。
  3. 助理協助在本地安裝相依並執行 `src/train_model.py` 進行訓練，訓練成功並產生 `models/ai_detector.joblib`（訓練結果與 Classification Report 已列印）。
  4. 助理啟動 Streamlit 應用以驗證，但在該執行環境中出現 `config.toml` 解析錯誤（與使用者或環境的 Streamlit 設定有關），因此提示使用者自行檢查 `~/.streamlit/config.toml` 或忽略該錯誤以本機執行。

可用來呈交的檔案：
- `README.md`（專案說明與快速操作）
- `src/train_model.py`（訓練腳本）
- `streamlit_app.py`（部署用主程式）
- 本次產生的 `data/ai_human_text.csv`（為 demo 目的，可改為實際 Kaggle 下載的資料）
- `chat_log.md`（本檔，包含對話摘要）

若需要我可以將完整的對話紀錄（包含問答原文）另存為 PDF，或協助你把 repo 推到 GitHub 並部署到 Streamlit Cloud。
