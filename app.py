"""
PsyChat - AI Psychological Counseling Chatbot + Real-time Benchmark Evaluation
Integrated Streamlit Interface

Unified mode:
- Chat with AI counselor
- Real-time evaluation metrics for each response
- Compare against human reference responses
- Session summary with overall metrics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from benchmark.data_loader import *
from benchmark.azure_client import AzureOpenAIClient
from benchmark.multi_turn_evaluator import MultiTurnEvaluator
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="PsyChat - AI Counseling & Real-time Evaluation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .user-message {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .ai-message {
        background-color: #f1f8e9;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
    }
    .metrics-box {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 10px 0;
    }
    .metric-item {
        display: inline-block;
        margin: 5px 10px 5px 0;
        padding: 5px 10px;
        background-color: #e9ecef;
        border-radius: 15px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# Helper functions
def get_few_shot_examples(num_examples=3):
    """Get example conversations from dataset for few-shot learning"""
    try:
        scenarios = get_all_scenarios(limit=10)
        # Select diverse examples
        examples = []
        seen_conditions = set()
        
        for scenario in scenarios:
            condition = scenario.get('condition')
            if condition not in seen_conditions and len(examples) < num_examples:
                examples.append(scenario)
                seen_conditions.add(condition)
        
        return examples
    except:
        return []

def build_few_shot_prompt(examples):
    """Build system prompt with few-shot examples"""
    base_prompt = """You are a professional psychological counselor with expertise in mental health.
You provide empathetic, supportive, and evidence-based counseling using techniques like CBT, 
motivational interviewing, and solution-focused brief therapy.

Here are some examples of good therapeutic responses:

"""
    
    for i, example in enumerate(examples, 1):
        if example['turns']:
            first_turn = example['turns'][0]
            base_prompt += f"""
Example {i} ({example['condition']}):
Patient: {first_turn['patient']}
Counselor: {first_turn['doctor']}

"""
    
    base_prompt += """
Now, respond to the patient with the same level of empathy, professionalism, and therapeutic skill.
"""
    
    return base_prompt

def evaluate_single_response(ai_response, reference_response=None):
    """Evaluate a single AI response against reference"""
    try:
        evaluator = MultiTurnEvaluator()
        
        # Create mock turn data for evaluation
        turn_data = {
            'patient': "User message",  # Placeholder
            'doctor': reference_response if reference_response else "No reference available",
            'turn': 1
        }
        
        ai_turn_data = {
            'patient': "User message",
            'doctor': ai_response,
            'turn': 1
        }
        
        # Evaluate single turn
        results = evaluator.evaluate_conversation([turn_data], [ai_turn_data])
        
        if results and 'turn_scores' in results and len(results['turn_scores']) > 0:
            return results['turn_scores'][0]
        else:
            # Return default scores if evaluation fails
            return {
                'rouge_score': 0.0,
                'meteor_score': 0.0,
                'ethical_alignment': 0.5,
                'sentiment_distribution': 0.5,
                'inclusivity_score': 0.5,
                'complexity_score': 0.5
            }
    except Exception as e:
        st.error(f"Evaluation error: {e}")
        return {
            'rouge_score': 0.0,
            'meteor_score': 0.0,
            'ethical_alignment': 0.5,
            'sentiment_distribution': 0.5,
            'inclusivity_score': 0.5,
            'complexity_score': 0.5
        }

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'azure_client' not in st.session_state:
    st.session_state.azure_client = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = "GPT-4o"
if 'session_metrics' not in st.session_state:
    st.session_state.session_metrics = []
if 'reference_scenario' not in st.session_state:
    st.session_state.reference_scenario = None

# Sidebar
st.sidebar.title("🧠 PsyChat")
st.sidebar.markdown("---")

# Model selection
model_choice = st.sidebar.selectbox(
    "AI Model",
    ["GPT-4o", "O1"],
    help="Select Azure OpenAI model"
)

# Initialize or update client if model changed
if st.session_state.current_model != model_choice or st.session_state.azure_client is None:
    try:
        if model_choice == "GPT-4o":
            config = st.secrets["azure_openai_4o"]
        else:
            config = st.secrets["azure_openai_o1"]
        
        st.session_state.azure_client = AzureOpenAIClient(
            model_name=model_choice,
            api_key=config["api_key"],
            endpoint=config["endpoint"],
            api_version=config["api_version"],
            deployment=config["deployment"]
        )
        st.session_state.current_model = model_choice
        st.sidebar.success(f"✅ {model_choice} loaded")
    except Exception as e:
        st.sidebar.error(f"❌ Error loading model: {e}")

# Reference scenario selection
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Benchmark Reference")

@st.cache_data
def load_reference_scenarios():
    try:
        scenarios = get_all_scenarios(limit=50)
        return scenarios
    except Exception as e:
        st.error(f"Error loading scenarios: {e}")
        return []

reference_scenarios = load_reference_scenarios()

if reference_scenarios:
    scenario_options = [
        f"{s['patient_id']} - {s['condition']} (Session {s['session_id']}, {len(s['turns'])} turns)"
        for s in reference_scenarios
    ]
    
    selected_idx = st.sidebar.selectbox(
        "Select Reference Scenario",
        range(len(scenario_options)),
        format_func=lambda x: scenario_options[x],
        help="Choose a reference scenario for comparison"
    )
    
    if st.sidebar.button("🔄 Load Reference"):
        st.session_state.reference_scenario = reference_scenarios[selected_idx]
        st.session_state.chat_history = []
        st.session_state.session_metrics = []
        st.rerun()

# Display current reference
if st.session_state.reference_scenario:
    st.sidebar.success(f"📋 Reference: {st.session_state.reference_scenario['patient_id']}")
    st.sidebar.metric("Turns", len(st.session_state.reference_scenario['turns']))
    st.sidebar.metric("Condition", st.session_state.reference_scenario['condition'].title())
else:
    st.sidebar.info("Select a reference scenario to start")

st.sidebar.markdown("---")

# Main interface
st.title("💬 AI Counseling with Real-time Evaluation")
st.markdown("Chat with AI counselor and get instant quality metrics for each response")

# System prompt configuration
with st.expander("⚙️ System Prompt Configuration"):
    use_default_prompt = st.checkbox("Use default counseling prompt", value=True)
    
    if not use_default_prompt:
        custom_prompt = st.text_area(
            "Custom System Prompt",
            value="""You are a professional psychological counselor with expertise in mental health...""",
            height=150
        )
    else:
        use_few_shot = st.checkbox("Use few-shot examples from dataset", value=True)
        
        if use_few_shot:
            st.info("💡 AI will be prompted with example therapeutic conversations from the dataset")

# Chat controls
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    st.markdown("### 💭 Conversation with Real-time Evaluation")
with col2:
    if st.button("🔄 New Session"):
        st.session_state.chat_history = []
        st.session_state.session_metrics = []
        if st.session_state.azure_client:
            st.session_state.azure_client.reset_conversation()
        st.rerun()
with col3:
    if len(st.session_state.chat_history) > 0:
        if st.button("📊 Session Summary"):
            st.session_state.show_summary = True
            st.rerun()

# Display chat history with metrics
chat_container = st.container()
with chat_container:
    for i, msg in enumerate(st.session_state.chat_history):
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <strong>👤 You:</strong><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <strong>🤖 AI Counselor ({st.session_state.current_model}):</strong><br>
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
            
            # Show metrics for AI response
            if 'metrics' in msg:
                metrics = msg['metrics']
                st.markdown(f"""
                <div class="metrics-box">
                    <strong>📊 Real-time Metrics:</strong><br>
                    <span class="metric-item">ROUGE: {metrics['rouge_score']:.3f}</span>
                    <span class="metric-item">METEOR: {metrics['meteor_score']:.3f}</span>
                    <span class="metric-item">Ethical: {metrics['ethical_alignment']:.3f}</span>
                    <span class="metric-item">Sentiment: {metrics['sentiment_distribution']:.3f}</span>
                    <span class="metric-item">Inclusive: {metrics['inclusivity_score']:.3f}</span>
                    <span class="metric-item">Complexity: {metrics['complexity_score']:.3f}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Show comparison with reference if available
                if 'reference_comparison' in msg and msg['reference_comparison']:
                    ref = msg['reference_comparison']
                    st.markdown(f"""
                    <div style="background-color: #fff3cd; padding: 10px; border-radius: 8px; margin: 5px 0;">
                        <strong>👨‍⚕️ Reference Response:</strong><br>
                        {ref}
                    </div>
                    """, unsafe_allow_html=True)

# Chat input
st.markdown("---")
user_input = st.text_area(
    "💬 Your message:",
    placeholder="Type your message here...",
    height=100,
    key="chat_input"
)

col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    send_button = st.button("📤 Send", type="primary", use_container_width=True)

with col2:
    if len(st.session_state.chat_history) > 0:
        if st.button("💾 Save Session", use_container_width=True):
            session_export = {
                'timestamp': datetime.now().isoformat(),
                'model': st.session_state.current_model,
                'reference_scenario': st.session_state.reference_scenario['patient_id'] if st.session_state.reference_scenario else None,
                'messages': st.session_state.chat_history,
                'session_metrics': st.session_state.session_metrics
            }
            st.download_button(
                label="Download Session",
                data=json.dumps(session_export, indent=2),
                file_name=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Process message
if send_button and user_input.strip():
    if st.session_state.azure_client:
        with st.spinner("🤔 AI is thinking..."):
            try:
                # Build system prompt with few-shot examples if enabled
                system_prompt = None
                if not use_default_prompt:
                    system_prompt = custom_prompt
                elif use_few_shot:
                    # Load example conversations from dataset
                    examples = get_few_shot_examples(num_examples=3)
                    system_prompt = build_few_shot_prompt(examples)
                
                # Generate response
                response = st.session_state.azure_client.generate_counselor_response(
                    user_input,
                    system_prompt=system_prompt
                )
                
                # Evaluate the response
                with st.spinner("📊 Evaluating response..."):
                    # Get reference response if available
                    reference_response = None
                    if st.session_state.reference_scenario:
                        turn_num = len(st.session_state.chat_history) // 2 + 1
                        if turn_num <= len(st.session_state.reference_scenario['turns']):
                            reference_response = st.session_state.reference_scenario['turns'][turn_num-1]['doctor']
                    
                    # Evaluate AI response
                    metrics = evaluate_single_response(response, reference_response)
                    
                    # Store metrics
                    st.session_state.session_metrics.append(metrics)
                
                # Add to chat history with metrics
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input
                })
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response,
                    'metrics': metrics,
                    'reference_comparison': reference_response
                })
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
    else:
        st.error("Please configure API keys in .streamlit/secrets.toml")

# Session Summary
if hasattr(st.session_state, 'show_summary') and st.session_state.show_summary:
    st.markdown("---")
    st.markdown("### 📊 Session Summary")
    
    if st.session_state.session_metrics:
        # Calculate aggregate metrics
        metrics_df = pd.DataFrame(st.session_state.session_metrics)
        agg_metrics = {
            'avg_rouge_score': metrics_df['rouge_score'].mean(),
            'avg_meteor_score': metrics_df['meteor_score'].mean(),
            'avg_ethical_alignment': metrics_df['ethical_alignment'].mean(),
            'avg_sentiment_distribution': metrics_df['sentiment_distribution'].mean(),
            'avg_inclusivity_score': metrics_df['inclusivity_score'].mean(),
            'avg_complexity_score': metrics_df['complexity_score'].mean()
        }
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        
        with col1:
            st.metric("ROUGE", f"{agg_metrics['avg_rouge_score']:.3f}")
        with col2:
            st.metric("METEOR", f"{agg_metrics['avg_meteor_score']:.3f}")
        with col3:
            st.metric("Ethical", f"{agg_metrics['avg_ethical_alignment']:.3f}")
        with col4:
            st.metric("Sentiment", f"{agg_metrics['avg_sentiment_distribution']:.3f}")
        with col5:
            st.metric("Inclusivity", f"{agg_metrics['avg_inclusivity_score']:.3f}")
        with col6:
            st.metric("Complexity", f"{agg_metrics['avg_complexity_score']:.3f}")
        
        # Visualization
        fig = px.bar(
            x=['ROUGE', 'METEOR', 'Ethical', 'Sentiment', 'Inclusivity', 'Complexity'],
            y=[agg_metrics['avg_rouge_score'], agg_metrics['avg_meteor_score'], agg_metrics['avg_ethical_alignment'],
               agg_metrics['avg_sentiment_distribution'], agg_metrics['avg_inclusivity_score'], agg_metrics['avg_complexity_score']],
            title=f'Session Summary - {st.session_state.current_model}',
            labels={'x': 'Metric', 'y': 'Score'},
            color_discrete_sequence=['#1f77b4']
        )
        fig.update_layout(yaxis_range=[0, 1], showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Export session data
        st.markdown("### 💾 Export Session Data")
        session_data = {
            'session_info': {
                'timestamp': datetime.now().isoformat(),
                'model': st.session_state.current_model,
                'reference_scenario': st.session_state.reference_scenario['patient_id'] if st.session_state.reference_scenario else None,
                'total_turns': len(st.session_state.session_metrics)
            },
            'aggregate_metrics': agg_metrics,
            'turn_metrics': st.session_state.session_metrics,
            'conversation': st.session_state.chat_history
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            json_str = json.dumps(session_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download Session JSON",
                data=json_str,
                file_name=f"session_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            metrics_df_export = pd.DataFrame(st.session_state.session_metrics)
            csv = metrics_df_export.to_csv(index=False)
            st.download_button(
                label="📥 Download Metrics CSV",
                data=csv,
                file_name=f"session_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    if st.button("❌ Close Summary"):
        st.session_state.show_summary = False
        st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
### ℹ️ About

**PsyChat System**

**Real-time Evaluation:**
- Chat with AI counselor
- Instant metrics for each response
- Compare against human reference
- Session summary with overall scores

**Metrics:**
- ROUGE (overlap)
- METEOR (semantic)
- Ethical (professional)
- Sentiment (emotional)
- Inclusivity (LGBTQ+)
- Complexity (readability)

**Dataset:** 542 therapy sessions
""")