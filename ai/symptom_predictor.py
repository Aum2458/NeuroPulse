import joblib
from typing import List, Tuple

class SymptomPredictor:
    def __init__(self):
        self.model = joblib.load('ai/disease_model.pkl')
        self.vectorizer = joblib.load('ai/vectorizer.pkl')

    def predict(self, symptoms_list: List[str]) -> Tuple[str, float]:
        symptoms_str = ", ".join(symptoms_list)
        vec = self.vectorizer.transform([symptoms_str])
        prediction = self.model.predict(vec)[0]
        proba = max(self.model.predict_proba(vec)[0]) * 100
        return prediction, round(proba, 2)
