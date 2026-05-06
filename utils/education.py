import random
from typing import Dict, Any, List, Optional

# -------------------- CATEGORIES --------------------
CATEGORIES = [
    "Gastroenterology", "Pulmonology", "Dermatology",
    "Cardiology", "Neurology", "Endocrinology",
    "Hepatology", "Pediatrics", "General Medicine"
]

# -------------------- CASE STUDIES --------------------
case_studies: List[Dict[str, Any]] = [
    {
        "title": "Abdominal Pain in Young Adult",
        "description": "A 26-year-old female presents with sudden sharp abdominal pain in the lower right quadrant, nausea, and mild fever.",
        "options": ["Kidney Stone", "Appendicitis", "Ulcer", "Food Poisoning"],
        "answer": "Appendicitis",
        "explanation": "The location and symptoms are classic signs of acute appendicitis.",
        "difficulty": "Intermediate",
        "category": "Gastroenterology"
    },
    {
        "title": "Chronic Breathlessness in Elderly Smoker",
        "description": "A 65-year-old male with a long history of smoking reports shortness of breath and fatigue on minimal exertion.",
        "options": ["Asthma", "COPD", "Heart Failure", "Bronchitis"],
        "answer": "COPD",
        "explanation": "COPD is common in smokers and causes progressive breathlessness.",
        "difficulty": "Easy",
        "category": "Pulmonology"
    },
    {
        "title": "Teen with Persistent Rash",
        "description": "A 17-year-old has itchy red patches behind the knees that worsen in winter.",
        "options": ["Eczema", "Psoriasis", "Fungal Infection", "Heat Rash"],
        "answer": "Eczema",
        "explanation": "Eczema is common in teens, especially in cold dry weather.",
        "difficulty": "Easy",
        "category": "Dermatology"
    },
    {
        "title": "Chest Pain on Exertion",
        "description": "A 55-year-old male experiences squeezing chest pain during exercise, relieved by rest.",
        "options": ["Angina", "Heart Attack", "GERD", "Panic Attack"],
        "answer": "Angina",
        "explanation": "Exertional chest pain relieved by rest is typical of stable angina.",
        "difficulty": "Intermediate",
        "category": "Cardiology"
    },
    {
        "title": "Sudden Severe Headache",
        "description": "A 40-year-old female complains of sudden, worst-ever headache accompanied by nausea and neck stiffness.",
        "options": ["Migraine", "Tension Headache", "Subarachnoid Hemorrhage", "Sinusitis"],
        "answer": "Subarachnoid Hemorrhage",
        "explanation": "Thunderclap headache and neck stiffness indicate possible subarachnoid hemorrhage.",
        "difficulty": "Advanced",
        "category": "Neurology"
    },
    {
        "title": "Frequent Urination and Thirst",
        "description": "A 30-year-old male reports excessive thirst and frequent urination for the past month.",
        "options": ["Diabetes Mellitus", "Diabetes Insipidus", "UTI", "Hyperthyroidism"],
        "answer": "Diabetes Mellitus",
        "explanation": "Polydipsia and polyuria are classic signs of diabetes mellitus.",
        "difficulty": "Easy",
        "category": "Endocrinology"
    },
    {
        "title": "Yellow Eyes and Fatigue",
        "description": "A 35-year-old female presents with jaundice, fatigue, and mild abdominal discomfort.",
        "options": ["Hepatitis A", "Gallstones", "Anemia", "Appendicitis"],
        "answer": "Hepatitis A",
        "explanation": "Jaundice with fatigue and mild abdominal discomfort points to viral hepatitis.",
        "difficulty": "Intermediate",
        "category": "Hepatology"
    },
    {
        "title": "Infant with Fever and Cough",
        "description": "A 1-year-old infant presents with fever, cough, and difficulty breathing.",
        "options": ["Bronchiolitis", "Pneumonia", "Asthma", "Croup"],
        "answer": "Pneumonia",
        "explanation": "Fever, cough, and breathing difficulty suggest lower respiratory infection in infants.",
        "difficulty": "Easy",
        "category": "Pediatrics"
    },
    {
        "title": "General Fatigue and Weakness",
        "description": "A 28-year-old female complains of persistent fatigue, hair loss, and cold intolerance.",
        "options": ["Hypothyroidism", "Anemia", "Depression", "Diabetes"],
        "answer": "Hypothyroidism",
        "explanation": "Fatigue, hair loss, and cold intolerance are classic hypothyroidism symptoms.",
        "difficulty": "Easy",
        "category": "Endocrinology"
    },
    {
        "title": "Persistent Cough and Night Sweats",
        "description": "A 45-year-old male reports chronic cough, night sweats, and weight loss.",
        "options": ["Tuberculosis", "Pneumonia", "Lung Cancer", "Bronchitis"],
        "answer": "Tuberculosis",
        "explanation": "Chronic cough with night sweats and weight loss suggests TB.",
        "difficulty": "Intermediate",
        "category": "Pulmonology"
    },
    {
        "title": "Severe Migraine Attack",
        "description": "A 32-year-old female experiences unilateral headache with nausea, photophobia, and visual aura.",
        "options": ["Migraine", "Cluster Headache", "Tension Headache", "Sinusitis"],
        "answer": "Migraine",
        "explanation": "Classic migraine features with aura, nausea, and photophobia.",
        "difficulty": "Intermediate",
        "category": "Neurology"
    },
    {
        "title": "Child with Abdominal Pain",
        "description": "A 7-year-old child presents with diffuse abdominal pain and vomiting after eating.",
        "options": ["Food Poisoning", "Appendicitis", "Intestinal Obstruction", "Gastroenteritis"],
        "answer": "Gastroenteritis",
        "explanation": "Acute diffuse pain and vomiting indicate gastroenteritis in children.",
        "difficulty": "Easy",
        "category": "Pediatrics"
    }
]

# -------------------- QUIZZES --------------------
quizzes: List[Dict[str, Any]] = [
    {
        "question": "Which vitamin is essential for blood clotting?",
        "options": ["Vitamin A", "Vitamin C", "Vitamin K", "Vitamin D"],
        "answer": "Vitamin K",
        "explanation": "Vitamin K is required for synthesizing clotting factors in the liver.",
        "difficulty": "Easy",
        "category": "Biochemistry"
    },
    {
        "question": "What is the normal adult resting heart rate range?",
        "options": ["40-60 bpm", "60-100 bpm", "100-120 bpm", "120-150 bpm"],
        "answer": "60-100 bpm",
        "explanation": "A resting heart rate between 60–100 bpm is considered normal for adults.",
        "difficulty": "Easy",
        "category": "Cardiology"
    },
    {
        "question": "Which organ detoxifies drugs and alcohol in the body?",
        "options": ["Kidneys", "Heart", "Liver", "Lungs"],
        "answer": "Liver",
        "explanation": "The liver is the primary organ for detoxification and drug metabolism.",
        "difficulty": "Easy",
        "category": "Hepatology"
    },
    {
        "question": "Which hormone regulates blood sugar levels?",
        "options": ["Insulin", "Glucagon", "Cortisol", "Thyroxine"],
        "answer": "Insulin",
        "explanation": "Insulin lowers blood glucose, while glucagon raises it.",
        "difficulty": "Easy",
        "category": "Endocrinology"
    },
    {
        "question": "Which type of blood cells fight infection?",
        "options": ["Red blood cells", "White blood cells", "Platelets", "Plasma"],
        "answer": "White blood cells",
        "explanation": "White blood cells are responsible for immunity.",
        "difficulty": "Easy",
        "category": "Immunology"
    },
    {
        "question": "What is the average human body temperature?",
        "options": ["35°C", "36.5-37.5°C", "38°C", "39°C"],
        "answer": "36.5-37.5°C",
        "explanation": "Normal body temperature is approximately 37°C.",
        "difficulty": "Easy",
        "category": "Physiology"
    },
    {
        "question": "Which cranial nerve controls facial movements?",
        "options": ["Trigeminal", "Facial", "Vagus", "Hypoglossal"],
        "answer": "Facial",
        "explanation": "The facial nerve (VII) controls facial expressions.",
        "difficulty": "Intermediate",
        "category": "Neurology"
    },
    {
        "question": "What is the main function of hemoglobin?",
        "options": ["Transport oxygen", "Fight infection", "Clot blood", "Store iron"],
        "answer": "Transport oxygen",
        "explanation": "Hemoglobin in red blood cells carries oxygen throughout the body.",
        "difficulty": "Easy",
        "category": "Physiology"
    },
    {
        "question": "Which vitamin is necessary for calcium absorption?",
        "options": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E"],
        "answer": "Vitamin D",
        "explanation": "Vitamin D facilitates calcium absorption in the gut.",
        "difficulty": "Easy",
        "category": "Nutrition"
    },
    {
        "question": "Normal adult respiratory rate is?",
        "options": ["12-20 breaths/min", "20-30 breaths/min", "8-12 breaths/min", "25-35 breaths/min"],
        "answer": "12-20 breaths/min",
        "explanation": "Normal adult respiratory rate ranges from 12 to 20 breaths per minute.",
        "difficulty": "Easy",
        "category": "Physiology"
    },
    {
        "question": "Which organ is primarily responsible for detoxification?",
        "options": ["Kidneys", "Liver", "Spleen", "Pancreas"],
        "answer": "Liver",
        "explanation": "The liver metabolizes and detoxifies substances from the blood.",
        "difficulty": "Easy",
        "category": "Hepatology"
    },
    {
        "question": "Which type of diabetes is autoimmune in nature?",
        "options": ["Type 1", "Type 2", "Gestational", "MODY"],
        "answer": "Type 1",
        "explanation": "Type 1 diabetes results from autoimmune destruction of insulin-producing cells.",
        "difficulty": "Intermediate",
        "category": "Endocrinology"
    }
]

# -------------------- FUNCTIONS --------------------
def get_case_study(category: Optional[str] = None) -> Dict[str, Any]:
    filtered = [cs for cs in case_studies if category is None or cs['category'] == category]
    return random.choice(filtered) if filtered else {
        "title": "No Case Study Available",
        "description": "No matching case studies found.",
        "options": [],
        "answer": "",
        "explanation": "",
        "difficulty": "Unknown",
        "category": category or "All"
    }

def get_quiz(category: Optional[str] = None) -> Dict[str, Any]:
    filtered = [q for q in quizzes if category is None or q['category'] == category]
    return random.choice(filtered) if filtered else {
        "question": "No quiz available for this category.",
        "options": [],
        "answer": "",
        "explanation": "",
        "difficulty": "Unknown",
        "category": category or "All"
    }

def get_case_studies(limit: int = 3, category: Optional[str] = None) -> List[Dict[str, Any]]:
    filtered = [cs for cs in case_studies if category is None or cs['category'] == category]
    return random.sample(filtered, min(limit, len(filtered)))

def get_quizzes(limit: int = 3, category: Optional[str] = None) -> List[Dict[str, Any]]:
    filtered = [q for q in quizzes if category is None or q['category'] == category]
    return random.sample(filtered, min(limit, len(filtered)))

# -------------------- TEST --------------------
if __name__ == "__main__":
    print("🎓 Random Case Study:\n", get_case_study())
    print("\n🧠 Random Quiz:\n", get_quiz())
    print("\n📚 Multiple Case Studies:\n", get_case_studies(5))
    print("\n🔬 Multiple Quizzes:\n", get_quizzes(5))
