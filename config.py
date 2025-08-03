# config.py - All settings and constants in one place

# API Configuration
GEMINI_MODEL = 'gemini-1.5-flash'
MAX_RETRIES = 3
API_TIMEOUT = 30

# Input Validation - Made more flexible based on feedback
MIN_INPUT_LENGTH = 15  # Reduced from 20
MAX_INPUT_LENGTH = 5000

# Age patterns - Accept approximate ages
AGE_PATTERNS = [
    r'\b(\d{1,3})\s*(?:years?\s*old|yo|y\.o\.)\b',  # "58 years old", "58 yo"
    r'\b(\d{1,3})\s*[,-]\s*(?:male|female|m|f)\b',   # "58, male"
    r'\bage\s*:?\s*(\d{1,3})\b',                     # "age: 58"
    r'\b(elderly|senior)\b',                         # "elderly" = 65+
    r'\b(middle.?aged|middle.?age)\b',               # "middle aged" = 45-65
    r'\b(young\s+adult)\b',                          # "young adult" = 18-35
    r'\b(\d{1,2})s\b',                               # "60s" = 60-69
]

# Procedure synonyms - Help with flexible input
PROCEDURE_SYNONYMS = {
    'heart': ['cardiac', 'cardio', 'heart', 'coronary'],
    'brain': ['brain', 'head', 'cerebral', 'cranial', 'neuro'],
    'scan': ['scan', 'imaging', 'test', 'study'],
    'monitor': ['monitor', 'monitoring', 'holter', 'event monitor'],
    'stress test': ['stress test', 'treadmill', 'exercise test', 'cardiac stress'],
    'mri': ['mri', 'magnetic resonance', 'mr imaging'],
    'ct': ['ct', 'cat scan', 'computed tomography'],
    'ultrasound': ['ultrasound', 'echo', 'sonogram', 'doppler']
}

# Example cases for the sidebar
EXAMPLE_CASES = {
    "Heart Monitor": """Age: 60s, Male
Complaint: Irregular heartbeats for 3 weeks
History: High blood pressure, diabetes
Family: Father had heart attack at 62
Symptoms: Palpitations, chest discomfort
Procedure: Heart monitor""",
    
    "Brain MRI": """Age: middle-aged, Female  
Complaint: Severe headaches for 6 months
History: Migraines since 20
Symptoms: Throbbing headaches, light sensitivity
Procedure: Brain MRI with contrast""",
    
    "Likely Denial": """Age: 25, Male
Complaint: Routine checkup
History: Healthy
Symptoms: None
Procedure: Full body MRI scan""",

    "Multiple Tests": """Age: elderly, Female
Complaint: Belly pain, weight loss for 3 months
History: High blood pressure, former smoker
Family: Father had colon cancer
Lab: Low blood count, elevated cancer markers
Symptoms: 15 lb weight loss, persistent pain

PROCEDURES REQUESTED:
1. CT scan of abdomen
2. Colonoscopy  
3. Upper endoscopy
4. PET scan
5. Liver MRI"""
}

# UI Configuration
APP_TITLE = "Medical Support Authorization AI"
APP_SUBTITLE = "Instant, Evidence-Based Procedure Authorization Decisions"

# Color scheme
COLORS = {
    'approved': '#059669',
    'denied': '#dc2626', 
    'pending': '#d97706',
    'primary': '#1f2937',
    'secondary': '#374151'
}

# Required keywords for basic validation (more flexible)
REQUIRED_KEYWORDS = ['age', 'procedure']  # Only need these two basics