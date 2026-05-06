import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
import joblib
import os

# Example training dataset
data = {
    'symptoms': [
        "fever, cough, fatigue",
        "chest pain, shortness of breath",
        "headache, nausea, vomiting",
        "skin rash, itching",
        "joint pain, swelling",
        "bp 180, dizziness, blurred vision",
        "sneezing, runny nose",
        "abdominal pain, diarrhea",
        "anxiety, insomnia",
        "frequent urination, increased thirst"
    ],
    'diagnosis': [
        "Flu",
        "Heart Attack",
        "Migraine",
        "Allergy",
        "Arthritis",
        "Hypertension",
        "Cold",
        "Gastroenteritis",
        "Stress Disorder",
        "Diabetes"
    ]
}

df = pd.DataFrame(data)

# Train pipeline
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

pipeline.fit(df['symptoms'], df['diagnosis'])

# Save model
os.makedirs('ai', exist_ok=True)
joblib.dump(pipeline, 'ai/disease_model.pkl')
print("✅ Model trained and saved to 'ai/disease_model.pkl'")
