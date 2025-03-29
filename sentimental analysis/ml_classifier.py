import os
import sys
import subprocess


def install_requirements():
    required_packages = ["nltk", "scikit-learn", "xgboost"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"Installing missing package: {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package])

install_requirements() 

import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("punkt", quiet=True)


try:
    with open("xgb_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)

    with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
except FileNotFoundError:
    print("Error: Model or vectorizer file not found. Ensure 'xgb_model.pkl' and 'tfidf_vectorizer.pkl' are in the same directory.")
    sys.exit(1)


try:
    with open("accuracy.txt", "r") as acc_file:
        accuracy = acc_file.read().strip()
except FileNotFoundError:
    accuracy = "Unknown (accuracy.txt not found)"


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^\w\s]", "", text)  
    text = re.sub(r"\b\d+\b", "", text)  

    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]

    return " ".join(tokens)


while True:
    new_review = input("\nEnter a review (or type 'exit' to quit): ").strip()
    
    if new_review.lower() == "exit":
        print("Exiting program. Goodbye!")
        break  

    cleaned_review = clean_text(new_review)

  
    review_tfidf = vectorizer.transform([cleaned_review])
    prediction = model.predict(review_tfidf)[0]
    sentiment = "Positive" if prediction == 1 else "Negative"

    
    print("\n====== REVIEW PREDICTION ======")
    print(f"Review: {new_review}")
    print(f"Predicted Sentiment: {sentiment}")
    print(f"Model Accuracy: {accuracy}")