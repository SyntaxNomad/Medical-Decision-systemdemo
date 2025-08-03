# utils.py - Helper functions made simple and flexible

import streamlit as st
import re
from config import *

def load_css():
    """Load CSS styling from external file"""
    try:
        with open("styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found - using basic styling")

def extract_age(text):
    """Extract age from text - now accepts approximate ages!"""
    text_lower = text.lower()
    
    # Handle special age descriptions
    if 'elderly' in text_lower or 'senior' in text_lower:
        return "65+"
    if 'middle' in text_lower and 'age' in text_lower:
        return "45-65"
    if 'young adult' in text_lower:
        return "18-35"
    
    # Handle "60s" format
    sixties_match = re.search(r'\b(\d{1,2})s\b', text_lower)
    if sixties_match:
        decade = int(sixties_match.group(1))
        return f"{decade}0s"
    
    # Handle specific ages
    for pattern in AGE_PATTERNS[:3]:  # First 3 are for specific ages
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1)
    
    return None

def extract_procedures(text):
    """Extract procedures from text - now more flexible!"""
    procedures = []
    text_lower = text.lower()
    
    # Look for explicit procedure lists
    if "procedures requested:" in text_lower or "requested procedures:" in text_lower:
        lines = text.split('\n')
        in_procedure_section = False
        
        for line in lines:
            line_lower = line.lower()
            if "procedure" in line_lower and "requested" in line_lower:
                in_procedure_section = True
                continue
            
            if in_procedure_section and line.strip():
                # Remove numbering and clean up
                clean_line = re.sub(r'^\d+\.?\s*', '', line.strip())
                if clean_line:
                    procedures.append(clean_line)
    
    # Look for single procedure mentions
    if not procedures:
        for keyword, synonyms in PROCEDURE_SYNONYMS.items():
            for synonym in synonyms:
                if synonym in text_lower:
                    # Find the full procedure name around this keyword
                    pattern = rf'\b[^.]*{re.escape(synonym)}[^.]*\b'
                    matches = re.findall(pattern, text_lower)
                    if matches:
                        procedures.extend(matches[:1])  # Take first match
                        break
    
    return procedures if procedures else ["Procedure mentioned in text"]

def validate_input_flexible(text):
    """Flexible input validation - improved based on feedback"""
    if not text or len(text.strip()) < MIN_INPUT_LENGTH:
        return False, f"Please provide more details (at least {MIN_INPUT_LENGTH} characters)"
    
    if len(text) > MAX_INPUT_LENGTH:
        return False, f"Input too long. Please limit to {MAX_INPUT_LENGTH} characters"
    
    # Check for age (more flexible now)
    age = extract_age(text)
    if not age:
        return False, "Please include patient age (can be approximate like '60s', 'elderly', 'middle-aged')"
    
    # Check for procedure mention (more flexible)
    procedures = extract_procedures(text)
    if not procedures:
        return False, "Please mention the requested procedure or test"
    
    return True, f"✓ Found age: {age}, procedure(s): {len(procedures)}"

def clean_input(text):
    """Clean and normalize input text"""
    if not text:
        return text
    
    # Fix common typos in medical terms
    replacements = {
        'abd': 'abdomen',
        'htn': 'hypertension', 
        'dm': 'diabetes mellitus',
        'mi': 'myocardial infarction',
        'sob': 'shortness of breath',
        'cp': 'chest pain',
        'yo': 'years old',
        'y.o.': 'years old'
    }
    
    cleaned = text
    for abbrev, full in replacements.items():
        # Replace abbreviations (case insensitive, word boundaries)
        pattern = rf'\b{re.escape(abbrev)}\b'
        cleaned = re.sub(pattern, full, cleaned, flags=re.IGNORECASE)
    
    return cleaned

def format_age_for_display(age_str):
    """Format age nicely for display"""
    if not age_str:
        return "Age not specified"
    
    age_mappings = {
        "65+": "Elderly (65+)",
        "45-65": "Middle-aged (45-65)", 
        "18-35": "Young adult (18-35)"
    }
    
    return age_mappings.get(age_str, f"{age_str} years old")

def get_validation_feedback(text):
    """Provide helpful feedback on what's missing"""
    feedback = []
    
    if len(text.strip()) < MIN_INPUT_LENGTH:
        feedback.append(f"Need at least {MIN_INPUT_LENGTH} characters")
    
    if not extract_age(text):
        feedback.append("Add patient age (exact or approximate)")
    
    if not extract_procedures(text):
        feedback.append("Mention the requested procedure")
    
    return feedback

def sanitize_medical_input(text):
    """Basic sanitization for medical input"""
    if not text:
        return text
    
    # Remove potential harmful characters but keep medical symbols
    sanitized = re.sub(r'[<>{}[\]\\]', '', text)
    
    # Limit consecutive spaces
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    return sanitized.strip()