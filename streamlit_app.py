import streamlit as st
import joblib
import numpy as np
import os


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
try:
    model = load_model()
except Exception as e:
    st.warning(f"模型載入失敗或不存在：{e}\n請先執行 `python src/train_model.py` 來訓練並產生 `models/ai_detector.joblib`。")


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
