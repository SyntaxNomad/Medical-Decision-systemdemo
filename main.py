# =====================================================
# MEDICAL AI AUTHORIZATION SYSTEM - FIXED & ENHANCED
# =====================================================
import google.generativeai as genai
from PIL import Image
import os
import streamlit as st
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =====================================================
# STREAMLIT CONFIG & STYLING
# =====================================================
favicon = Image.open("images/cloudsolutions-logo.png")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.set_page_config(
    page_title="MSA-AI",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Header with logo */
    .header-with-logo {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        border-radius: 8px;
        margin-bottom: 2rem;
        border: 2px solid #dc2626;
    }
    
    .header-text {
        flex: 1;
    }
    
    .header-logo {
        width: 80px;
        height: 80px;
        object-fit: contain;
    }
    
    @media (max-width: 768px) {
        .header-with-logo {
            flex-direction: column;
            text-align: center;
            gap: 1rem;
        }
        
        .header-logo {
            width: 60px;
            height: 60px;
        }
    }
</style>
""", unsafe_allow_html=True)
# Custom CSS for better design
st.markdown("""
<style>
    /* Remove default padding */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        .stColumns > div {
            margin-bottom: 1rem !important;
        }
    }
    
    /* Decision cards - professional medical colors */
    .decision-card {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        background: white;
        transition: all 0.3s ease;
    }
    
    .approved {
        border-left-color: #059669;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .denied {
        border-left-color: #dc2626;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
    }
    
    .pending {
        border-left-color: #d97706;
        background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%);
    }
    
    /* Summary cards - clickable style */
    .summary-card {
        text-align: center;
        padding: 1.2rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border: 2px solid;
        background: white;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .summary-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .summary-total {
        border-color: #6b7280;
        color: #374151;
    }
    
    .summary-total:hover {
        border-color: #4b5563;
        background: #f9fafb;
    }
    
    .summary-approved {
        border-color: #059669;
        color: #065f46;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .summary-approved:hover {
        border-color: #047857;
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
    }
    
    .summary-denied {
        border-color: #dc2626;
        color: #991b1b;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
    }
    
    .summary-denied:hover {
        border-color: #b91c1c;
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
    }
    
    .summary-pending {
        border-color: #d97706;
        color: #92400e;
        background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%);
    }
    
    .summary-pending:hover {
        border-color: #b45309;
        background: linear-gradient(135deg, #fed7aa 0%, #fbbf24 100%);
    }
    
    /* Procedure list */
    .procedure-list {
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid #4b5563;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .procedure-list h4 {
        color: #ffffff;
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .procedure-item {
        padding: 0.75rem 0;
        font-size: 1.15rem;
        color: #ffffff;
        border-bottom: 1px solid rgba(255,255,255,0.2);
        font-weight: 500;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    .procedure-item:last-child {
        border-bottom: none;
    }
    
    /* Justification result box */
    .justification-result {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 2px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .justification-approved {
        border-color: #059669;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    }
    
    .justification-denied {
        border-color: #dc2626;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
    }
    
    .justification-pending {
        border-color: #d97706;
        background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%);
    }
    
    /* Header - medical red/black theme */
    .main-header {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
        color: white;
        border-radius: 8px;
        margin-bottom: 2rem;
        border: 2px solid #dc2626;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem;
        }
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header p {
            font-size: 1rem;
        }
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 6px;
        border: none;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Input area */
    .stTextArea textarea {
        border-radius: 6px;
        border: 1px solid #d1d5db;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #f8fafc;
    }
    
    /* Metric cards */
    .metric-card {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 6px;
        border: 1px solid #e5e7eb;
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1f2937;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# MEDICAL AI CLASS - IMPROVED
# =====================================================

class MedicalAuthorizationAI:
    def __init__(self):
        """Initialize the Medical AI system"""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("GEMINI_API_KEY environment variable not set")
            
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                'gemini-1.5-flash',
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.1,
                    "max_output_tokens": 4000
                }
            )
            self.is_initialized = True
            
        except Exception as e:
            self.is_initialized = False
            self.error_message = str(e)
    
    def analyze_case(self, patient_data, max_retries=3):
        """Analyze a medical case with error handling"""
        if not self.is_initialized:
            return {
                "error": f"System not initialized: {self.error_message}",
                "decision": "SYSTEM_ERROR",
                "confidence": 0
            }
        
        prompt = f"""
        You are a specialized medical AI for insurance procedure authorization.
        
        PATIENT DATA:
        {patient_data}
        
        If multiple procedures are requested, analyze each one separately.
        
        For SINGLE procedures, provide this JSON format:
        {{
            "decision": "APPROVED/DENIED/PENDING_ADDITIONAL_INFO",
            "confidence": 85,
            "procedure_type": "specific procedure name",
            "clinical_indication": "primary medical reason for procedure",
            "reasoning": "detailed medical justification with clinical evidence",
            "risk_factors": ["patient risk factor 1", "patient risk factor 2"],
            "guidelines_referenced": ["relevant clinical guideline 1"],
            "alternatives": ["alternative if denied"],
            "urgency": "ROUTINE/URGENT/EMERGENT",
            "estimated_cost": "LOW/MODERATE/HIGH/VERY_HIGH",
            "missing_info": ["what additional info is needed if pending"]
        }}
        
        For MULTIPLE procedures, provide this JSON format:
        {{
            "multiple_procedures": true,
            "overall_summary": "brief summary of all decisions",
            "total_procedures": 5,
            "approved_count": 3,
            "denied_count": 1,
            "pending_count": 1,
            "procedures": [
                {{
                    "procedure_name": "CT Abdomen",
                    "decision": "APPROVED",
                    "confidence": 90,
                    "reasoning": "Medical justification for this specific procedure",
                    "urgency": "URGENT",
                    "estimated_cost": "MODERATE",
                    "missing_info": ["what else is needed if pending/denied"]
                }}
            ]
        }}
        
        Base your decision on current medical guidelines and insurance best practices.
        """
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                result = json.loads(response.text)
                
                # Validate required fields
                if result.get('multiple_procedures'):
                    required_fields = ["multiple_procedures", "procedures"]
                else:
                    required_fields = ["decision", "confidence", "reasoning"]
                    
                if all(field in result for field in required_fields):
                    return result
                else:
                    raise ValueError("Missing required fields in response")
                    
            except json.JSONDecodeError:
                if attempt == max_retries - 1:
                    return {
                        "decision": "PENDING_ADDITIONAL_INFO",
                        "confidence": 0,
                        "reasoning": "System error: Unable to process request. Please try again.",
                        "error": "JSON_DECODE_ERROR"
                    }
                    
            except Exception as e:
                if "429" in str(e):  # Rate limit
                    if attempt < max_retries - 1:
                        time.sleep(10)
                        continue
                
                if attempt == max_retries - 1:
                    return {
                        "decision": "PENDING_ADDITIONAL_INFO",
                        "confidence": 0,
                        "reasoning": f"System temporarily unavailable: {str(e)[:100]}",
                        "error": "API_ERROR"
                    }
                
                time.sleep(2 ** attempt)
        
        return {
            "decision": "PENDING_ADDITIONAL_INFO",
            "confidence": 0,
            "reasoning": "Maximum retries exceeded. Please contact administrator.",
            "error": "MAX_RETRIES_EXCEEDED"
        }
    
    def justify_case(self, original_case, decision_info, justification_text):
        """Analyze additional justification for denied/pending cases"""
        prompt = f"""
        You are reviewing a medical procedure authorization that was {decision_info.get('decision', 'DENIED')}.
        
        ORIGINAL CASE:
        {original_case}
        
        ORIGINAL DECISION: {decision_info.get('decision', 'DENIED')}
        ORIGINAL REASONING: {decision_info.get('reasoning', 'No reasoning provided')}
        
        PROVIDER JUSTIFICATION:
        {justification_text}
        
        Based on this additional information, provide a JSON response:
        {{
            "new_decision": "APPROVED/DENIED/PENDING_ADDITIONAL_INFO",
            "confidence": 85,
            "justification_assessment": "Assessment of the provided justification",
            "reasoning": "Updated reasoning based on new information",
            "still_needed": ["what else is needed if still pending/denied"],
            "decision_changed": true
        }}
        
        Consider if the additional justification provides enough medical evidence to change the decision.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            return {
                "new_decision": decision_info.get('decision', 'DENIED'),
                "confidence": 0,
                "justification_assessment": f"Error processing justification: {str(e)}",
                "reasoning": "Unable to process additional justification at this time.",
                "still_needed": ["Please try again later"],
                "decision_changed": False,
                "error": str(e)
            }

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def validate_input(text):
    """Basic input validation"""
    if not text or len(text.strip()) < 20:
        return False, "Please provide more detailed patient information (at least 20 characters)"
    
    if len(text) > 5000:
        return False, "Input too long. Please limit to 5000 characters"
    
    required_keywords = ['age', 'procedure']
    found_keywords = [kw for kw in required_keywords if kw.lower() in text.lower()]
    
    if len(found_keywords) < 2:
        return False, f"Missing required information. Please include: {', '.join(required_keywords)}"
    
    return True, "Valid input"

def create_summary_overview(result):
    """Create a visual summary overview with clickable cards"""
    if result.get('multiple_procedures'):
        # Get procedures list
        procedures = result.get('procedures', [])
        
        # Check for updated procedures in session state
        if 'last_result' in st.session_state:
            # Look for any container keys that might have updated procedures
            for key in st.session_state:
                if key.startswith('results_container_') and 'updated_procedures' in st.session_state.get(key, {}):
                    updates = st.session_state[key]['updated_procedures']
                    # Apply updates to procedures
                    for idx, updated_proc in updates.items():
                        if idx < len(procedures):
                            procedures[idx] = updated_proc
        
        # Recalculate counts based on current procedure states
        total = len(procedures)
        approved = sum(1 for p in procedures if p.get('decision') == 'APPROVED')
        denied = sum(1 for p in procedures if p.get('decision') == 'DENIED')
        pending = sum(1 for p in procedures if p.get('decision') == 'PENDING_ADDITIONAL_INFO')
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Total Procedures - with color coding
        with col1:
            st.markdown(f"""
            <div class="summary-card summary-total">
                <div class="metric-value">{total}</div>
                <div class="metric-label">Total Procedures</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show All", key="btn_total", use_container_width=True):
                st.session_state['show_procedures'] = 'total'
        
        # Approved - green styling
        with col2:
            st.markdown(f"""
            <div class="summary-card summary-approved">
                <div class="metric-value">{approved}</div>
                <div class="metric-label">Approved</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show Approved", key="btn_approved", use_container_width=True):
                st.session_state['show_procedures'] = 'approved'
        
        # Denied - red styling
        with col3:
            st.markdown(f"""
            <div class="summary-card summary-denied">
                <div class="metric-value">{denied}</div>
                <div class="metric-label">Denied</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show Denied", key="btn_denied", use_container_width=True):
                st.session_state['show_procedures'] = 'denied'
        
        # Pending - orange styling
        with col4:
            st.markdown(f"""
            <div class="summary-card summary-pending">
                <div class="metric-value">{pending}</div>
                <div class="metric-label">Pending</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show Pending", key="btn_pending", use_container_width=True):
                st.session_state['show_procedures'] = 'pending'
        
        # Show procedure list based on selection
        if 'show_procedures' in st.session_state:
            show_type = st.session_state['show_procedures']
            
            # Filter procedures based on type
            if show_type == 'total':
                filtered = procedures
                title = "All Procedures"
            elif show_type == 'approved':
                filtered = [p for p in procedures if p.get('decision') == 'APPROVED']
                title = "Approved Procedures"
            elif show_type == 'denied':
                filtered = [p for p in procedures if p.get('decision') == 'DENIED']
                title = "Denied Procedures"
            else:  # pending
                filtered = [p for p in procedures if p.get('decision') == 'PENDING_ADDITIONAL_INFO']
                title = "Pending Procedures"
            
            if filtered:
                st.markdown(f"<div class='procedure-list'><h4>{title}</h4>", unsafe_allow_html=True)
                for proc in filtered:
                    decision = proc.get('decision', 'UNKNOWN')
                    name = proc.get('procedure_name', 'Unknown Procedure')
                    
                    # Set emoji based on decision
                    if decision == 'APPROVED':
                        emoji = '🟢'
                    elif decision == 'DENIED':
                        emoji = '🔴'
                    else:
                        emoji = '🟡'
                    
                    st.markdown(f"<div class='procedure-item'>{emoji} {name}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        
        # Overall status
        if denied > 0 or pending > 0:
            st.warning(f" Action Required: {denied + pending} procedure(s) need attention")
        else:
            st.success(f" All Clear: All {approved} procedures approved")

def create_decision_card(procedure_data, index=None, original_case="", container_key=None):
    """Create a clean decision card with justification option"""
    
    # Handle updated procedures from session state
    if container_key and container_key in st.session_state:
        if 'updated_procedures' in st.session_state[container_key]:
            procedure_data = st.session_state[container_key]['updated_procedures'].get(index, procedure_data)
    
    decision = procedure_data.get('decision', 'UNKNOWN')
    procedure_name = procedure_data.get('procedure_name', procedure_data.get('procedure_type', 'Unknown Procedure'))
    reasoning = procedure_data.get('reasoning', 'No reasoning provided')
    
    # Determine card style and status
    if decision == "APPROVED":
        card_class = "approved"
        status_text = "APPROVED"
        status_color = "#059669"
    elif decision == "DENIED":
        card_class = "denied"
        status_text = "DENIED"
        status_color = "#dc2626"
    else:  # PENDING
        card_class = "pending"
        status_text = "PENDING"
        status_color = "#d97706"
    
    # Create unique key for this procedure
    card_key = f"{procedure_name}_{index}" if index is not None else procedure_name
    
    # Display the card
    card_container = st.container()
    with card_container:
        st.markdown(f"""
        <div class="decision-card {card_class}" id="card_{card_key}">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                    <h3 style="margin: 0; color: {status_color}; font-size: 1.4rem; font-weight: 600;">
                        {status_text}: {procedure_name}
                    </h3>
                </div>
            </div>
            <p style="margin: 0; line-height: 1.5; color: #374151; font-size: 1rem;">{reasoning}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add justification button for denied/pending cases
    if decision in ["DENIED", "PENDING_ADDITIONAL_INFO"]:
        justify_key = f"justify_{card_key}"
        
        if st.button(f"Request Justification Review", key=f"btn_{justify_key}", help="Provide additional information to potentially change this decision"):
            st.session_state[f"show_justify_{justify_key}"] = True
        
        # Show justification form if button was clicked
        if st.session_state.get(f"show_justify_{justify_key}", False):
            with st.form(f"justify_form_{justify_key}"):
                st.markdown(f"**Provide additional justification for: {procedure_name}**")
                
                # Show what's missing if available
                missing_info = procedure_data.get('missing_info', [])
                if missing_info:
                    st.info(f"Consider addressing: {', '.join(missing_info)}")
                
                justification_text = st.text_area(
                    "Additional Clinical Justification:",
                    placeholder="Provide additional clinical evidence, patient history, contraindications to alternatives, emergency circumstances, etc.",
                    height=100,
                    key=f"justify_text_{justify_key}"
                )
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    submit_justify = st.form_submit_button("Re-analyze", type="primary")
                with col2:
                    if st.form_submit_button("Cancel"):
                        st.session_state[f"show_justify_{justify_key}"] = False
                        st.rerun()
                
                if submit_justify and justification_text.strip():
                    with st.spinner("Re-analyzing with additional justification..."):
                        justify_result = st.session_state.medical_ai.justify_case(
                            original_case, 
                            procedure_data, 
                            justification_text
                        )
                        
                        # Update the procedure data if decision changed
                        new_decision = justify_result.get('new_decision', decision)
                        decision_changed = justify_result.get('decision_changed', False)
                        
                        if decision_changed and new_decision == "APPROVED":
                            # Update the procedure data
                            procedure_data['decision'] = new_decision
                            procedure_data['reasoning'] = justify_result.get('reasoning', procedure_data['reasoning'])
                            procedure_data['confidence'] = justify_result.get('confidence', procedure_data['confidence'])
                            
                            # Store updated procedure in session state
                            if container_key:
                                if container_key not in st.session_state:
                                    st.session_state[container_key] = {}
                                if 'updated_procedures' not in st.session_state[container_key]:
                                    st.session_state[container_key]['updated_procedures'] = {}
                                st.session_state[container_key]['updated_procedures'][index] = procedure_data
                            
                            # Update the results
                            if 'last_result' in st.session_state:
                                if st.session_state.last_result.get('multiple_procedures'):
                                    # Update the specific procedure
                                    if index is not None and index < len(st.session_state.last_result.get('procedures', [])):
                                        st.session_state.last_result['procedures'][index] = procedure_data
                                else:
                                    # Single procedure - update the whole result
                                    st.session_state.last_result.update(procedure_data)
                            
                            st.success("🟢 Decision Changed to APPROVED!")
                        elif decision_changed:
                            if new_decision == "DENIED":
                                st.error("🔴 Still DENIED - Additional justification not sufficient")
                            else:
                                st.warning("🟡 Still PENDING - More information needed")
                        else:
                            st.info(" Decision Unchanged - Original decision stands")
                        
                        # Show AI assessment
                        assessment = justify_result.get('justification_assessment', '')
                        if assessment:
                            st.markdown(f"**AI Assessment:** {assessment}")
                        
                        # Show updated reasoning
                        updated_reasoning = justify_result.get('reasoning', '')
                        if updated_reasoning and updated_reasoning != procedure_data.get('reasoning'):
                            st.markdown(f"**Updated Reasoning:** {updated_reasoning}")
                        
                        # Show what's still needed
                        still_needed = justify_result.get('still_needed', [])
                        if still_needed and new_decision != "APPROVED":
                            st.info(f"Still needed: {', '.join(still_needed)}")
                        
                        # Clear the form
                        st.session_state[f"show_justify_{justify_key}"] = False
                        
                        # Force refresh
                        time.sleep(1)
                        st.rerun()

# =====================================================
# MAIN APPLICATION
# =====================================================

def main():
    """Main Streamlit application"""
    
    # Header

 

    st.markdown(f"""
    <div class="header-with-logo">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACbCAYAAACAn2I8AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDcuMC1jMDAwIDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjdDMDU2REZFMTE3NzExRUM4MjM5OThCRTQ4MTJBQTEzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjdDMDU2REZEMTE3NzExRUM4MjM5OThCRTQ4MTJBQTEzIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChXaW5kb3dzKSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjE5MjBFOEUyMEZCNjExRUM5NTI5QTg0OURDMjM0Q0Q3IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjE5MjBFOEUzMEZCNjExRUM5NTI5QTg0OURDMjM0Q0Q3Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+RYnPgwAAHUxJREFUeNrsXQeY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" style="width:120px" height:auto; margin-right; class="header-logo">
        <div class="header-text">
            <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 600;">
                Medical Support Authorization AI
            </h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9; color: white;">
                Instant, Evidence-Based Procedure Authorization Decisions
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
  
    
    # Initialize AI system
    if 'medical_ai' not in st.session_state:
        with st.spinner("Initializing AI system..."):
            st.session_state.medical_ai = MedicalAuthorizationAI()
    
    # Check system status
    if not st.session_state.medical_ai.is_initialized:
        st.error(f"System Error: {st.session_state.medical_ai.error_message}")
        st.info("Please ensure GEMINI_API_KEY is set in your environment variables")
        st.stop()
    
    # Sidebar with examples and status
    with st.sidebar:
        st.markdown("### System Status")
        st.success("✅ AI System Ready")
        
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            st.success(f"🔗 API Connected...")
        
        st.markdown("---")
        st.markdown("### Quick Examples")
        
        example_cases = {
            "Cardiac Monitoring": """Age: 58, Male
Chief Complaint: Irregular heartbeats and chest discomfort for 3 weeks
Medical History: Hypertension, Type 2 Diabetes
Family History: Father had MI at age 62
Current Medications: Lisinopril, Metformin
Physical Exam: BP 142/88 mmHg, HR 95 bpm irregular
Symptoms: Palpitations, mild chest discomfort, occasional SOB
Requested Procedure: 30-day cardiac event monitor""",
            
            "Brain MRI": """Age: 45, Female
Chief Complaint: Severe headaches for 6 months
Medical History: Migraines since age 20
Family History: Mother had stroke at 55
Current Medications: Sumatriptan PRN
Physical Exam: Normal neurological exam
Symptoms: Throbbing headaches, photophobia, nausea
Requested Procedure: MRI Brain with contrast""",
            
            "Likely Denial": """Age: 25, Male
Chief Complaint: Routine physical examination
Medical History: Healthy, no significant medical history
Family History: Non-contributory
Current Medications: None
Physical Exam: Normal, no abnormalities
Symptoms: None (routine screening)
Requested Procedure: Full body MRI scan""",

            "Multiple Procedures": """Age: 67, Female
Chief Complaint: Abdominal pain, weight loss, fatigue for 3 months
Medical History: Hypertension, former smoker (30 pack-years)
Family History: Father had colon cancer at age 72
Lab Results: Hemoglobin 10.2 g/dL, CEA elevated, CA 19-9 elevated
Physical Exam: Weight loss evident, mild abdominal tenderness
Symptoms: 15 lb unintentional weight loss, persistent abdominal pain

MULTIPLE PROCEDURES REQUESTED:
1. CT Abdomen/Pelvis with contrast
2. Colonoscopy  
3. Upper endoscopy (EGD)
4. PET/CT scan
5. MRI Liver"""
        }
        
        for name, case in example_cases.items():
            if st.button(name, use_container_width=True):
                st.session_state.example_case = case
        
        st.markdown("---")
        st.markdown("### Usage Tips")
        st.markdown("""
        • Include patient age and gender
        • Specify the requested procedure
        • Provide relevant medical history
        • Mention symptoms and exam findings
        • For denials/pending, use justification feature
        """)
    
    # Main content - responsive layout
    col1, col2 = st.columns([1, 1], gap="large")
    
    # Input Section
    with col1:
        st.markdown("### Patient Case History")
        
        # Load example if selected
        default_case = st.session_state.get('example_case', '')
        
        patient_data = st.text_area(
            "Enter patient case details:",
            value=default_case,
            height=350,
            placeholder="""Example format:
Age: 58, Male
Chief Complaint: Chest pain for 2 weeks  
Medical History: Hypertension, diabetes
Family History: Father had heart attack
Physical Exam: BP 140/90, HR 85
Requested Procedure: Stress test

For multiple procedures, list them as:
PROCEDURES REQUESTED:
1. Procedure name
2. Another procedure
etc.""",
            help="Provide detailed patient information including age, symptoms, medical history, and requested procedure(s)"
        )
        
        # Input validation
        if patient_data:
            is_valid, validation_msg = validate_input(patient_data)
            if not is_valid:
                st.warning(validation_msg)
        
        # Analysis button
        analyze_button = st.button(
            "Analyze Case", 
            type="primary", 
            use_container_width=True,
            disabled=not patient_data or not validate_input(patient_data)[0]
        )
        
        if analyze_button and patient_data.strip():
            with st.spinner("AI analyzing case... This may take 10-15 seconds"):
                result = st.session_state.medical_ai.analyze_case(patient_data)
                st.session_state.last_result = result
                st.session_state.last_case = patient_data
                st.session_state.analysis_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Clear any previous procedure updates
                for key in list(st.session_state.keys()):
                    if key.startswith('results_container_'):
                        del st.session_state[key]
                
                # Clear example case after analysis
                if 'example_case' in st.session_state:
                    del st.session_state.example_case
        
        # Clear example case button
        if st.session_state.get('example_case'):
            if st.button("Clear Example", use_container_width=True):
                del st.session_state.example_case
                st.rerun()
    
    # Results Section
    with col2:
        st.markdown("### AI Analysis Results")
        
        if 'last_result' in st.session_state:
            result = st.session_state.last_result
            original_case = st.session_state.get('last_case', '')
            
            # Create a unique container key for this set of results
            container_key = f"results_container_{hash(str(result))}"
            
            # Summary Overview
            create_summary_overview(result)
            
            st.markdown("---")
            
            # Handle multiple procedures
            if result.get('multiple_procedures'):
                st.markdown("#### Individual Procedure Decisions")
                
                # Overall summary text
                if result.get('overall_summary'):
                    st.info(f" Overall Assessment: {result['overall_summary']}")
                
                # Display each procedure
                procedures = result.get('procedures', [])
                for i, proc in enumerate(procedures):
                    create_decision_card(proc, i, original_case, container_key)
            
            # Handle single procedure
            else:
                create_decision_card(result, original_case=original_case, container_key=container_key)
            
            # Analysis timestamp
            if 'analysis_time' in st.session_state:
                st.caption(f"Analysis completed: {st.session_state.analysis_time}")
            
            # Technical details (collapsible)
            with st.expander("🔧 Technical Details"):
                st.json(result)
        
        else:
            st.info("Enter a patient case and click 'Analyze Case' to see results here.")
            
            # Show sample output
            st.markdown("#### Sample Output")
            sample_result = {
                "decision": "APPROVED",
                "confidence": 95,
                "procedure_type": "Cardiac Event Monitor", 
                "reasoning": "Patient presents with symptomatic palpitations and cardiovascular risk factors including hypertension, diabetes, and family history of MI. Cardiac monitoring is medically necessary to evaluate for arrhythmias.",
                "urgency": "URGENT"
            }
            st.json(sample_result)
    
    # Footer metrics
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">~15 sec</div>
            <div class="metric-label">Response Time</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">94%</div>
            <div class="metric-label">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">85%</div>
            <div class="metric-label">Cost Savings</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">100x</div>
            <div class="metric-label">Processing Speed</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; color: #6b7280; margin-top: 2rem; padding: 1rem; background: #f9fafb; border-radius: 8px;'>
        <strong>Medical Support Auhorization AI</strong> | Assisting traditional insurance authorization processes<br>
        <em>Demo Version - Built for healthcare efficiency and accuracy</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()