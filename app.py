# app.py - Clean, simple main application file
import streamlit as st
from datetime import datetime

# Import our clean components
from ai_engine import MedicalAuthorizationAI
from ui_components import (
    render_header, 
    render_sidebar, 
    render_input_section, 
    render_results_section,
    render_footer_metrics,
    render_diagnosis_display  # Add this import
)
from utils import load_css, validate_input_flexible, clean_input, sanitize_medical_input
from config import APP_TITLE

def configure_app():
    """Configure Streamlit app settings"""
    try:
        # Try to load favicon (optional)
        from PIL import Image
        favicon = Image.open("images/cloudsolutions-logo.png")
    except:
        favicon = None
    
    st.set_page_config(
        page_title="MSA-AI",
        page_icon=favicon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_ai():
    """Initialize AI system with proper error handling"""
    if 'medical_ai' not in st.session_state:
        with st.spinner("🔄 Initializing AI system..."):
            st.session_state.medical_ai = MedicalAuthorizationAI()
    
    # Check if initialization failed
    if not st.session_state.medical_ai.is_initialized:
        st.error(f"❌ **System Error:** {st.session_state.medical_ai.error_message}")
        st.info("ℹ️ Please ensure GEMINI_API_KEY is set in your environment variables or Streamlit secrets")
        st.stop()

def handle_analysis(patient_data):
    """Handle case analysis with improved error handling"""
    # Clean and validate input
    cleaned_data = clean_input(sanitize_medical_input(patient_data))
    
    # Validate input
    is_valid, validation_message = validate_input_flexible(cleaned_data)
    if not is_valid:
        st.error(f"❌ **Input Error:** {validation_message}")
        return
    
    # Perform analysis
    with st.spinner("🔬 AI analyzing case... This may take 10-15 seconds"):
        result = st.session_state.medical_ai.analyze_case(cleaned_data)
        
        # Store results
        st.session_state.last_result = result
        st.session_state.last_case = cleaned_data
        st.session_state.analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Clear any previous updates
        keys_to_clear = [key for key in st.session_state.keys() if key.startswith('results_container_')]
        for key in keys_to_clear:
            del st.session_state[key]
        
        # Clear example case after analysis
        # if 'example_case' in st.session_state:
        #     del st.session_state.example_case
        
        # Show success message
        if result.get('error'):
            st.error(f"⚠️ **Analysis Error:** {result.get('reasoning', 'Unknown error')}")
        else:
            st.success("✅ **Analysis Complete!** Results displayed below.")

def main():
    """Main application function - clean and simple"""
    
    # Configure the app
    configure_app()
    
    # Load styling
    load_css()
    
    # Render header
    render_header()
    
    # Initialize AI system
    initialize_ai()
    
    # Create main layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    # Left column: Input, sidebar, and diagnoses
    with col1:
        render_sidebar()
        
        # Input section
        patient_data, analyze_button = render_input_section()
        
        # Handle analysis button click
        if analyze_button and patient_data.strip():
            handle_analysis(patient_data)
        
        # ADD DIAGNOSES HERE - under the input section
        if 'last_result' in st.session_state:
            render_diagnosis_display(st.session_state.last_result)
    
    # Right column: Authorization Results (without diagnoses now)
    with col2:
        render_results_section()
    
    # Footer metrics
    render_footer_metrics()

if __name__ == "__main__":
    main()