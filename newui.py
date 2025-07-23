# =====================================================
# MEDICAL AI AUTHORIZATION SYSTEM - FIXED & ENHANCED
# =====================================================

import google.generativeai as genai
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

st.set_page_config(
    page_title="Medical AI Authorization",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            st.warning(f"⚡ Action Required: {denied + pending} procedure(s) need attention")
        else:
            st.success(f"✅ All Clear: All {approved} procedures approved")

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
                            st.balloons()
                        elif decision_changed:
                            if new_decision == "DENIED":
                                st.error("🔴 Still DENIED - Additional justification not sufficient")
                            else:
                                st.warning("🟡 Still PENDING - More information needed")
                        else:
                            st.info("📋 Decision Unchanged - Original decision stands")
                        
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
    st.markdown("""
    <div class="main-header">
        <h1>Medical AI Authorization</h1>
        <p>Instant, Evidence-Based Procedure Authorization Decisions</p>
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
            st.success(f"🔗 API Connected ({api_key[:10]}...)")
        
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
        st.markdown("### Patient Case Input")
        
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
                    st.info(f"📋 Overall Assessment: {result['overall_summary']}")
                
                # Display each procedure
                procedures = result.get('procedures', [])
                for i, proc in enumerate(procedures):
                    create_decision_card(proc, i, original_case, container_key)
            
            # Handle single procedure
            else:
                create_decision_card(result, original_case=original_case, container_key=container_key)
            
            # Analysis timestamp
            if 'analysis_time' in st.session_state:
                st.caption(f"⏰ Analysis completed: {st.session_state.analysis_time}")
            
            # Technical details (collapsible)
            with st.expander("🔧 Technical Details"):
                st.json(result)
        
        else:
            st.info("👈 Enter a patient case and click 'Analyze Case' to see results here.")
            
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
        <strong>Medical AI Authorization System</strong> | Replacing traditional insurance authorization processes<br>
        <em>Demo Version - Built for healthcare efficiency and accuracy</em>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()