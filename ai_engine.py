# ai_engine.py - Clean AI logic separated from UI

import google.generativeai as genai
import json
import time
import os
from config import GEMINI_MODEL, MAX_RETRIES, API_TIMEOUT
from dotenv import load_dotenv


load_dotenv()  # This loads .env file


class MedicalAuthorizationAI:
    """
    Simple AI engine for medical procedure authorization
    Separated from UI for clarity and reusability
    """
    
    def __init__(self):
        """Initialize the AI with error handling"""
        self.is_initialized = False
        self.error_message = ""
        
        try:
            # Get API key from environment or Streamlit secrets
            api_key = self._get_api_key()
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment or secrets")
            
            # Configure the AI model
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                GEMINI_MODEL,
                generation_config={
                    "response_mime_type": "application/json",
                    "temperature": 0.1,  # Low temperature for consistent medical decisions
                    "max_output_tokens": 4000
                }
            )
            
            self.is_initialized = True
            
        except Exception as e:
            self.error_message = str(e)
    
    def _get_api_key(self):
        """Get API key from environment or Streamlit secrets"""
        # Try environment first
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            return api_key
        
        # Try Streamlit secrets
        try:
            import streamlit as st
            return st.secrets.get("GEMINI_API_KEY")
        except:
            return None
    
    def analyze_case(self, patient_data):
        """
        Main analysis function - improved with better error handling
        Returns structured medical decision
        """
        if not self.is_initialized:
            return self._error_response(f"AI system not initialized: {self.error_message}")
        
        # Create the analysis prompt
        prompt = self._create_analysis_prompt(patient_data)
        
        # Try analysis with retries
        for attempt in range(MAX_RETRIES):
            try:
                response = self.model.generate_content(prompt)
                result = json.loads(response.text)
                
                # Validate the response structure
                if self._is_valid_response(result):
                    return self._enhance_response(result)
                else:
                    raise ValueError("Invalid response structure from AI")
                    
            except json.JSONDecodeError as e:
                if attempt == MAX_RETRIES - 1:
                    return self._error_response("Unable to process request - please try again")
                    
            except Exception as e:
                # Handle rate limiting
                if "429" in str(e):
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(10 * (attempt + 1))  # Exponential backoff
                        continue
                
                if attempt == MAX_RETRIES - 1:
                    return self._error_response(f"Analysis failed: {str(e)[:100]}")
                
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return self._error_response("Maximum retries exceeded - please try again later")
    
    def justify_case(self, original_case, decision_info, justification_text):
        """Simple justification for individual procedures only"""
        
        if not self.is_initialized:
            return self._error_response("AI system not initialized")
        
        # Simple prompt - no related procedure logic
        prompt = f"""
        Review this medical authorization that was {decision_info.get('decision', 'DENIED')}.

        ORIGINAL CASE: {original_case}
        ORIGINAL DECISION: {decision_info.get('decision')}
        ORIGINAL REASONING: {decision_info.get('reasoning', 'None provided')}

        NEW JUSTIFICATION FROM PROVIDER: {justification_text}

        Based on this additional information, provide JSON response:
        {{
            "new_decision": "APPROVED/DENIED/PENDING_ADDITIONAL_INFO",
            "confidence": 85,
            "justification_assessment": "Assessment of the new justification",
            "reasoning": "Updated reasoning based on new information",
            "still_needed": ["what else needed if still pending/denied"],
            "decision_changed": true
        }}

        Consider if the additional justification provides sufficient medical evidence to change THIS SPECIFIC PROCEDURE'S decision.
        Be reasonable - if good additional evidence is provided, consider approval.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            return {
                "new_decision": decision_info.get('decision', 'DENIED'),
                "confidence": 0,
                "justification_assessment": f"Error processing justification: {str(e)[:50]}",
                "reasoning": "Unable to process additional information",
                "decision_changed": False
            }
        
    def _create_analysis_prompt(self, patient_data):
        """Create the main analysis prompt"""
        return f"""
You are a medical AI for insurance procedure authorization. Analyze this case and provide a JSON response.

PATIENT DATA:
{patient_data}

RESPONSE FORMAT:
For single procedures:
{{
    "decision": "APPROVED/DENIED/PENDING_ADDITIONAL_INFO",
    "confidence": 85,
    "procedure_type": "specific procedure name",
    "clinical_indication": "primary medical reason",
    "reasoning": "detailed medical justification with evidence",
    "risk_factors": ["risk1", "risk2"],
    "guidelines_referenced": ["guideline1"],
    "alternatives": ["alternative if denied"],
    "urgency": "ROUTINE/URGENT/EMERGENT",
    "estimated_cost": "LOW/MODERATE/HIGH/VERY_HIGH", 
    "missing_info": ["what's needed if pending"],
    "differential_diagnosis": [
        {{"diagnosis": "Condition 1", "icd10": "ICD10-CODE", "confidence": 85}},
        {{"diagnosis": "Condition 2", "icd10": "ICD10-CODE", "confidence": 70}}
    ]
}}

For multiple procedures:
{{
    "multiple_procedures": true,
    "overall_summary": "brief summary",
    "total_procedures": 3,
    "approved_count": 2,
    "denied_count": 1,
    "pending_count": 0,
    "procedures": [
        {{
            "procedure_name": "CT Abdomen",
            "decision": "APPROVED",
            "confidence": 90,
            "reasoning": "Medical justification",
            "urgency": "URGENT",
            "estimated_cost": "MODERATE",
            "missing_info": []d
        }}
    ],
    "differential_diagnosis": [
        {{"diagnosis": "Condition", "icd10": "CODE", "confidence": 85}}
    ]
}}

Base decisions on medical necessity, clinical guidelines, and insurance best practices.
Be thorough but practical in your analysis.
"""
    
    def _create_justification_prompt(self, original_case, decision_info, justification_text):
        """Create prompt for justification re-analysis"""
        return f"""
Review this medical authorization that was {decision_info.get('decision', 'DENIED')}.

ORIGINAL CASE: {original_case}
ORIGINAL DECISION: {decision_info.get('decision')}
ORIGINAL REASONING: {decision_info.get('reasoning', 'None provided')}

NEW JUSTIFICATION FROM PROVIDER: {justification_text}

Based on this additional information, provide JSON response:
{{
    "new_decision": "APPROVED/DENIED/PENDING_ADDITIONAL_INFO",
    "confidence": 85,
    "justification_assessment": "Assessment of the new justification",
    "reasoning": "Updated reasoning based on new information",
    "still_needed": ["what else needed if still pending/denied"],
    "decision_changed": true
}}

Consider if the additional justification provides sufficient medical evidence to change the decision.
Be reasonable - if good additional evidence is provided, consider approval.
"""
    
    def _is_valid_response(self, result):
        """Validate AI response structure"""
        if result.get('multiple_procedures'):
            required_fields = ["multiple_procedures", "procedures"]
        else:
            required_fields = ["decision", "confidence", "reasoning"]
        
        return all(field in result for field in required_fields)
    
    def _enhance_response(self, result):
        """Add helpful enhancements to the response"""
        # Add timestamp
        result['analyzed_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Ensure confidence is reasonable
        if 'confidence' in result:
            result['confidence'] = max(0, min(100, result['confidence']))
        
        # Clean up procedure names
        if result.get('multiple_procedures') and 'procedures' in result:
            for proc in result['procedures']:
                if 'confidence' in proc:
                    proc['confidence'] = max(0, min(100, proc['confidence']))
        
        return result
    
    def _error_response(self, error_message):
        """Create standardized error response"""
        return {
            "decision": "PENDING_ADDITIONAL_INFO",
            "confidence": 0,
            "reasoning": error_message,
            "error": True,
            "analyzed_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_status(self):
        """Get current AI system status"""
        return {
            "initialized": self.is_initialized,
            "model": GEMINI_MODEL if self.is_initialized else None,
            "error": self.error_message if not self.is_initialized else None
        }