"""
Azure OpenAI Client for Chatbot Response Generation

Handles API calls to Azure OpenAI (GPT-4o and O1 models)
Generates counselor responses for multi-turn conversations
"""

from openai import AzureOpenAI
from typing import List, Dict
import time


class AzureOpenAIClient:
    """
    Client for Azure OpenAI API
    Supports GPT-4o and O1 deployments
    """
    
    def __init__(self, model_name: str, api_key: str, endpoint: str, api_version: str, deployment: str):
        """
        Initialize Azure OpenAI client
        
        Args:
            model_name: "GPT-4o" or "O1"
            api_key: Azure OpenAI API key
            endpoint: Azure OpenAI endpoint URL
            api_version: API version
            deployment: Deployment name
        """
        self.model_name = model_name
        self.deployment = deployment
        self.conversation_history = []
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version
        )
    
    def reset_conversation(self):
        """Reset conversation history for new session"""
        self.conversation_history = []
    
    def generate_counselor_response(self, patient_message: str, system_prompt: str = None) -> str:
        """
        Generate a counselor response to patient message
        
        Args:
            patient_message: The patient's message
            system_prompt: Optional system prompt (uses default if None)
            
        Returns:
            AI-generated counselor response
        """
        if system_prompt is None:
            system_prompt = self._get_default_system_prompt()
        
        # Build messages for API call
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current patient message
        messages.append({"role": "user", "content": f"Patient: {patient_message}"})
        
        # Call Azure OpenAI
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            counselor_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": f"Patient: {patient_message}"})
            self.conversation_history.append({"role": "assistant", "content": counselor_response})
            
            return counselor_response
            
        except Exception as e:
            raise RuntimeError(f"Azure OpenAI API error: {e}")
    
    def generate_multi_turn_conversation(self, patient_turns: List[str], system_prompt: str = None) -> List[Dict]:
        """
        Generate responses for a complete multi-turn conversation
        
        Args:
            patient_turns: List of patient messages in order
            system_prompt: Optional system prompt
            
        Returns:
            List of dicts with turn, patient, and ai_response
        """
        self.reset_conversation()
        results = []
        
        for turn_num, patient_msg in enumerate(patient_turns, 1):
            try:
                ai_response = self.generate_counselor_response(patient_msg, system_prompt)
                results.append({
                    'turn': turn_num,
                    'patient': patient_msg,
                    'ai_response': ai_response
                })
                # Small delay to avoid rate limiting
                time.sleep(0.5)
            except Exception as e:
                results.append({
                    'turn': turn_num,
                    'patient': patient_msg,
                    'ai_response': f"ERROR: {str(e)}"
                })
        
        return results
    
    def _get_default_system_prompt(self) -> str:
        """
        Default system prompt for psychological counseling
        """
        return """You are a professional psychological counselor with expertise in mental health. 
You provide empathetic, supportive, and evidence-based counseling using techniques like:
- Cognitive Behavioral Therapy (CBT)
- Motivational Interviewing
- Solution-Focused Brief Therapy

Guidelines:
1. Show empathy and understanding
2. Ask appropriate questions for assessment
3. Provide practical, actionable advice
4. Assess for crisis/safety when appropriate
5. Use inclusive, non-judgmental language
6. Maintain professional boundaries
7. Encourage hope and resilience

Respond as a counselor would in a therapy session."""


def create_client_from_secrets(model_name: str, secrets) -> AzureOpenAIClient:
    """
    Create client from Streamlit secrets
    
    Args:
        model_name: "GPT-4o" or "O1"
        secrets: Streamlit secrets object
        
    Returns:
        Configured AzureOpenAIClient
    """
    if model_name == "GPT-4o":
        config = secrets["azure_openai_4o"]
    else:  # O1
        config = secrets["azure_openai_o1"]
    
    return AzureOpenAIClient(
        model_name=model_name,
        api_key=config["api_key"],
        endpoint=config["endpoint"],
        api_version=config["api_version"],
        deployment=config["deployment"]
    )

