# Airline Reviews Sentiment Analysis

This project performs sentiment analysis on airline reviews by classifying them as Positive or Negative. The model is trained using TF-IDF vectorization and an XGBoost classifier. The dataset includes airline reviews with an overall score, which is used to determine sentiment.

---

## **Project Overview**
1. **Preprocessing**: The dataset is cleaned, tokenized, and vectorized using TF-IDF.
2. **Handling Imbalance**: SMOTE is applied to balance the dataset.
3. **Model Training**: An XGBoost classifier is trained on the processed data.
4. **Saving Model**: The trained model and vectorizer are saved for future predictions.
5. **Prediction**: The model predicts sentiment based on user-input reviews.

install python 3.9 or later 
#instruction to run

 Run Prediction Script

To test the model with a new airline review:

python ml_classifier.py

Enter a review when prompted.

The model will output whether the sentiment is Positive or Negative.