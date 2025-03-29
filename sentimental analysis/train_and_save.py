import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score


nltk.download("stopwords")
nltk.download("punkt")


file_path = "AirlineReviews.csv"
df = pd.read_csv(file_path)


if "Review" not in df.columns or "OverallScore" not in df.columns:
    raise KeyError("Required columns ('Review', 'OverallScore') are missing!")


df = df.dropna(subset=["Review", "OverallScore"]).copy()


df["Sentiment"] = df["OverallScore"].apply(lambda x: 1 if x > 5 else 0)


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", "", text)  
    text = re.sub(r"\b\d+\b", "", text)  

    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    return " ".join(tokens)


df["cleaned_text"] = df["Review"].apply(clean_text)


X_train, X_test, y_train, y_test = train_test_split(
    df["cleaned_text"], df["Sentiment"], test_size=0.2, random_state=42
)


vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=10000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


smote = SMOTE(random_state=42)
X_train_tfidf_resampled, y_train_resampled = smote.fit_resample(X_train_tfidf, y_train)


xgb_model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
xgb_model.fit(X_train_tfidf_resampled, y_train_resampled)


y_pred = xgb_model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)


with open("accuracy.txt", "w") as acc_file:
    acc_file.write(f"{accuracy:.4f}")


with open("xgb_model.pkl", "wb") as model_file:
    pickle.dump(xgb_model, model_file)

with open("tfidf_vectorizer.pkl", "wb") as vectorizer_file:
    pickle.dump(vectorizer, vectorizer_file)

print(f"Model training complete! Accuracy: {accuracy:.4f}")
print("Model, vectorizer, and accuracy saved successfully.")
