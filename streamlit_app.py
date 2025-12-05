import streamlit as st
import joblib
import numpy as np
import os
import requests


def download_file(url: str, dest_path: str):
    """Download a file from `url` to `dest_path` with a simple progress indicator."""
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    resp = requests.get(url, stream=True, timeout=30)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))
    chunk_size = 8192
    downloaded = 0
    with open(dest_path + ".part", "wb") as f:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            if not chunk:
                continue
            f.write(chunk)
            downloaded += len(chunk)
    os.replace(dest_path + ".part", dest_path)


@st.cache_resource
def load_model():
    model_path = os.path.join("models", "ai_detector.joblib")
    return joblib.load(model_path)


st.set_page_config(
    page_title="AI / Human 文章偵測器",
    page_icon="🤖",
)

st.title("🤖 AI vs Human 文章偵測器")
st.write("輸入一段文字，模型會估計它是 **AI 生成** 還是 **人類撰寫**。")

# Load model if available
model = None
model_path = os.path.join("models", "ai_detector.joblib")
try:
    model = load_model()
except Exception as e:
    st.warning(f"模型載入失敗或不存在：{e}")

    # Provide option to download a pre-trained model from a URL (useful for Streamlit Cloud)
    st.info("若你沒有本地模型，可從遠端下載模型檔。")

    # Determine model URL: prefer Streamlit secrets, then environment variable, then placeholder
    MODEL_URL = None
    try:
        MODEL_URL = st.secrets.get("MODEL_URL")
    except Exception:
        MODEL_URL = None
    if not MODEL_URL:
        MODEL_URL = os.environ.get("MODEL_URL")

    if MODEL_URL:
        st.write("模型下載地址已設定。你可以按下按鈕下載模型並載入。")
        if st.button("下載並載入模型"):
            try:
                with st.spinner("正在下載模型..."):
                    download_file(MODEL_URL, model_path)
                st.success("模型下載完成，已儲存至 models/ai_detector.joblib。請重新整理頁面以載入模型。")
            except Exception as e2:
                st.error(f"下載模型失敗：{e2}")
    else:
        st.write("未設定模型下載地址。請在 Streamlit secrets 或環境變數 `MODEL_URL` 中放入模型檔案的可下載 URL（例如 GitHub Release 連結）。")
        st.write("或是在本地先執行 `python src/train_model.py` 產生 `models/ai_detector.joblib`。")


# User input
default_text = "請在這裡貼上你想檢測的文章內容..."

user_text = st.text_area(
    "輸入或貼上文字：",
    height=220,
    placeholder=default_text
)

if st.button("開始分析"):
    if not user_text.strip():
        st.warning("請先輸入一些文字再按下按鈕。")
    else:
        if model is None:
            st.error("模型尚未載入。請先執行 `python src/train_model.py` 並確認 `models/ai_detector.joblib` 存在。")
        else:
            proba = model.predict_proba([user_text])[0]
            classes = model.classes_

            # 找出 "AI" 這一類的位置，如果找不到就用 index 0 作為 fallback
            try:
                ai_idx = int(np.where(classes == "AI")[0][0])
                ai_prob = float(proba[ai_idx])
            except Exception:
                ai_prob = float(proba[0])

            human_prob = 1.0 - ai_prob

            col1, col2 = st.columns(2)
            with col1:
                st.metric("AI 生成的機率", f"{ai_prob * 100:.1f} %")
            with col2:
                st.metric("Human 撰寫的機率", f"{human_prob * 100:.1f} %")

            st.write("---")
            st.write("🔍 **視覺化：AI 機率條**")
            st.progress(ai_prob)

            with st.expander("顯示模型內部資訊（選用）"):
                st.write("模型使用 TF-IDF + Logistic Regression 進行分類。")
                try:
                    vectorizer = model.named_steps["tfidf"]
                    vocab_size = len(vectorizer.vocabulary_)
                    st.write(f"目前 TF-IDF 詞彙數量：約 **{vocab_size}** 個特徵。")
                except Exception:
                    st.write("無法取得 TF-IDF 特徵資訊。")
