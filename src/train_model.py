import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score
import joblib
import os


def main():
    # 1. 讀取資料 ------------------------------------------------------
    DATA_PATH = os.path.join("data", "ai_human_text.csv")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}\nPlease put your CSV into the `data/` folder and name it `ai_human_text.csv` (or change DATA_PATH).")

    df = pd.read_csv(DATA_PATH)

    # 假設欄位名稱是 text / label，不一樣就改這兩行
    # 如果你的資料欄位不同，請修改下列兩行，或在執行前重新命名 CSV 欄位
    X = df["text"].astype(str)
    y = df["label"].astype(str)   # 例如 "AI" 或 "Human"

    # 若 label 不是 AI/Human，可以在這裡做 mapping，例如:
    # y = df['generated'].map({0: 'Human', 1: 'AI'})

    # 2. 切訓練 / 測試 -------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # 3. 建立 TF-IDF + Logistic Regression pipeline -------------------
    pipeline = Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),   # unigrams + bigrams
                max_df=0.9,
                min_df=5,
                max_features=5000
            )
        ),
        (
            "clf",
            LogisticRegression(
                max_iter=500,
                n_jobs=-1
            )
        )
    ])

    # 4. 訓練模型 ------------------------------------------------------
    print("Training model...")
    pipeline.fit(X_train, y_train)

    # 5. 評估模型 ------------------------------------------------------
    y_pred = pipeline.predict(X_test)

    # 若 label 是 "AI"/"Human"，這裡換成 1/0 來算 ROC-AUC
    try:
        y_test_binary = (y_test == "AI").astype(int)
        # 取得預測 AI 的機率
        proba = pipeline.predict_proba(X_test)
        ai_index = list(pipeline.classes_).index("AI")
        y_proba_ai = proba[:, ai_index]

        print("\n=== Classification Report ===")
        print(classification_report(y_test, y_pred))

        try:
            auc = roc_auc_score(y_test_binary, y_proba_ai)
            print(f"ROC-AUC (AI vs Human): {auc:.4f}")
        except Exception as e:
            print("ROC-AUC 無法計算，可能是資料標籤問題：", e)
    except Exception:
        print("無法計算 classification report / ROC-AUC，請確認標籤包含 'AI' 與 'Human'。")

    # 6. 存模型 --------------------------------------------------------
    os.makedirs("models", exist_ok=True)
    MODEL_PATH = os.path.join("models", "ai_detector.joblib")
    joblib.dump(pipeline, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


if __name__ == "__main__":
    main()
