"""
PsyChat - AI Psychological Counseling Chatbot + Benchmark Evaluation
Streamlit Interface

Two modes:
1. Chat Mode: Interactive counseling with GPT-4o/O1
2. Benchmark Mode: Evaluate AI responses against reference data
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
    page_title="PsyChat - AI Counseling & Evaluation",
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

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'azure_client' not in st.session_state:
    st.session_state.azure_client = None
if 'current_model' not in st.session_state:
    st.session_state.current_model = "GPT-4o"

# Sidebar
st.sidebar.title("🧠 PsyChat")
st.sidebar.markdown("---")

# Mode selection
mode = st.sidebar.radio(
    "Select Mode",
    ["💬 Chat Mode", "📊 Benchmark Mode"],
    help="Chat: Interactive counseling | Benchmark: Evaluate against reference data"
)

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

st.sidebar.markdown("---")

# ====================
# CHAT MODE
# ====================
if mode == "💬 Chat Mode":
    st.title("💬 AI Psychological Counseling Chat")
    st.markdown("Chat with an AI counselor trained on therapeutic conversations")
    
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
            # Load examples from dataset for few-shot learning
            use_few_shot = st.checkbox("Use few-shot examples from dataset", value=True)
            
            if use_few_shot:
                st.info("💡 AI will be prompted with example therapeutic conversations from the dataset")
    
    # Chat controls
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 💭 Conversation")
    with col2:
        if st.button("🔄 New Chat"):
            st.session_state.chat_history = []
            if st.session_state.azure_client:
                st.session_state.azure_client.reset_conversation()
            st.rerun()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
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
            if st.button("💾 Save Chat", use_container_width=True):
                chat_export = {
                    'timestamp': datetime.now().isoformat(),
                    'model': st.session_state.current_model,
                    'messages': st.session_state.chat_history
                }
                st.download_button(
                    label="Download Chat History",
                    data=json.dumps(chat_export, indent=2),
                    file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
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
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'role': 'user',
                        'content': user_input
                    })
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating response: {e}")
        else:
            st.error("Please configure API keys in .streamlit/secrets.toml")

# ====================
# BENCHMARK MODE
# ====================
else:  # Benchmark Mode
    st.title("📊 Multi-Turn Benchmark Evaluation")
    st.markdown("Evaluate AI chatbot responses against reference therapeutic conversations")
    
    # Load dataset
    @st.cache_data
    def load_data():
        try:
            summary = get_scenario_summary()
            scenarios = get_all_scenarios(limit=100)
            return summary, scenarios
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return None, None
    
    summary_df, scenarios = load_data()
    
    if summary_df is not None and scenarios:
        # Dataset overview
        st.sidebar.subheader("📊 Dataset Info")
        st.sidebar.metric("Total Scenarios", len(scenarios))
        
        # Filter by condition
        conditions = summary_df['condition'].unique().tolist()
        selected_condition = st.sidebar.selectbox(
            "Filter by Condition",
            ["All"] + sorted(conditions)
        )
        
        # Filter scenarios
        if selected_condition != "All":
            filtered_scenarios = [s for s in scenarios if s.get('condition') == selected_condition]
        else:
            filtered_scenarios = scenarios
        
        # Scenario selection
        scenario_options = [
            f"{s['patient_id']} - {s['condition']} (Session {s['session_id']}, {len(s['turns'])} turns)"
            for s in filtered_scenarios
        ]
        
        selected_idx = st.selectbox(
            "📋 Select Scenario to Evaluate",
            range(len(scenario_options)),
            format_func=lambda x: scenario_options[x]
        )
        
        selected_scenario = filtered_scenarios[selected_idx]
        
        # Display scenario details
        st.markdown("### 📝 Scenario Details")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Patient ID", selected_scenario['patient_id'])
        with col2:
            st.metric("Condition", selected_scenario['condition'].title())
        with col3:
            st.metric("Total Turns", len(selected_scenario['turns']))
        with col4:
            risk_color = "🔴" if selected_scenario.get('risk_flag') == 'yes' else "🟢"
            st.metric("Risk Flag", f"{risk_color} {selected_scenario.get('risk_flag', 'N/A')}")
        
        # Show reference conversation
        with st.expander("👀 View Reference Conversation"):
            for turn in selected_scenario['turns']:
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**Turn {turn['turn']} - Patient:**\n\n{turn['patient']}")
                with col2:
                    st.success(f"**Turn {turn['turn']} - Doctor:**\n\n{turn['doctor']}")
        
        st.markdown("---")
        
        # Evaluation controls
        st.markdown("### 🚀 Run Evaluation")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.write(f"**Model:** {model_choice}")
            st.write(f"**Scenario:** {selected_scenario['patient_id']} ({len(selected_scenario['turns'])} turns)")
        
        with col2:
            if st.button("▶️ Run Evaluation", type="primary", use_container_width=True):
                with st.spinner(f"🤖 Generating {model_choice} responses..."):
                    try:
                        # Extract patient messages
                        patient_messages = [turn['patient'] for turn in selected_scenario['turns']]
                        
                        # Generate AI responses
                        if st.session_state.azure_client:
                            ai_conversation = st.session_state.azure_client.generate_multi_turn_conversation(
                                patient_messages
                            )
                            
                            # Add model info
                            for turn in ai_conversation:
                                turn['model'] = model_choice
                            
                            # Evaluate
                            with st.spinner("📊 Evaluating responses..."):
                                try:
                                    evaluator = MultiTurnEvaluator()
                                    results = evaluator.evaluate_conversation(
                                        selected_scenario['turns'],
                                        ai_conversation
                                    )
                                    
                                    results['scenario_metadata'] = {
                                        'patient_id': selected_scenario['patient_id'],
                                        'condition': selected_scenario['condition'],
                                        'session_id': selected_scenario['session_id'],
                                        'risk_flag': selected_scenario['risk_flag']
                                    }
                                    results['model'] = model_choice
                                    
                                    # Display results
                                    st.success("✅ Evaluation complete!")
                                    
                                    # Aggregate scores
                                    st.markdown("### 📈 Aggregate Scores")
                                    
                                    agg = results['aggregate_scores']
                                    
                                    col1, col2, col3 = st.columns(3)
                                    col4, col5, col6 = st.columns(3)
                                    
                                    with col1:
                                        st.metric("ROUGE", f"{agg['avg_rouge_score']:.3f}")
                                    with col2:
                                        st.metric("METEOR", f"{agg['avg_meteor_score']:.3f}")
                                    with col3:
                                        st.metric("Ethical", f"{agg['avg_ethical_alignment']:.3f}")
                                    with col4:
                                        st.metric("Sentiment", f"{agg['avg_sentiment_distribution']:.3f}")
                                    with col5:
                                        st.metric("Inclusivity", f"{agg['avg_inclusivity_score']:.3f}")
                                    with col6:
                                        st.metric("Complexity", f"{agg['avg_complexity_score']:.3f}")
                                    
                                    # Visualization
                                    fig = px.bar(
                                        x=['ROUGE', 'METEOR', 'Ethical', 'Sentiment', 'Inclusivity', 'Complexity'],
                                        y=[agg['avg_rouge_score'], agg['avg_meteor_score'], agg['avg_ethical_alignment'],
                                           agg['avg_sentiment_distribution'], agg['avg_inclusivity_score'], agg['avg_complexity_score']],
                                        title=f'Evaluation Scores - {model_choice}',
                                        labels={'x': 'Metric', 'y': 'Score'},
                                        color_discrete_sequence=['#1f77b4']
                                    )
                                    fig.update_layout(yaxis_range=[0, 1], showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True)
                                    
                                    # Turn-by-turn results
                                    st.markdown("### 🔍 Turn-by-Turn Comparison")
                                    
                                    for turn_score in results['turn_scores']:
                                        with st.expander(f"📝 Turn {turn_score['turn']}"):
                                            col1, col2, col3 = st.columns(3)
                                            
                                            with col1:
                                                st.markdown("**👤 Patient:**")
                                                st.info(turn_score['patient_message'])
                                            
                                            with col2:
                                                st.markdown("**👨‍⚕️ Reference:**")
                                                st.success(turn_score['reference_response'])
                                            
                                            with col3:
                                                st.markdown(f"**🤖 {model_choice}:**")
                                                st.warning(turn_score['ai_response'])
                                            
                                            # Scores
                                            st.markdown("**📊 Scores:**")
                                            score_cols = st.columns(6)
                                            metrics_list = [
                                                ("ROUGE", turn_score['rouge_score']),
                                                ("METEOR", turn_score['meteor_score']),
                                                ("Ethical", turn_score['ethical_alignment']),
                                                ("Sentiment", turn_score['sentiment_distribution']),
                                                ("Inclusivity", turn_score['inclusivity_score']),
                                                ("Complexity", turn_score['complexity_score'])
                                            ]
                                            
                                            for col, (name, score) in zip(score_cols, metrics_list):
                                                col.metric(name, f"{score:.2f}")
                                    
                                    # Export options
                                    st.markdown("---")
                                    st.markdown("### 💾 Export Results")
                                    
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        json_str = json.dumps(results, indent=2, ensure_ascii=False)
                                        st.download_button(
                                            label="📥 Download as JSON",
                                            data=json_str,
                                            file_name=f"evaluation_{selected_scenario['patient_id']}_{model_choice}.json",
                                            mime="application/json"
                                        )
                                    
                                    with col2:
                                        turn_df = pd.DataFrame(results['turn_scores'])
                                        csv = turn_df.to_csv(index=False)
                                        st.download_button(
                                            label="📥 Download as CSV",
                                            data=csv,
                                            file_name=f"evaluation_{selected_scenario['patient_id']}_{model_choice}.csv",
                                            mime="text/csv"
                                        )
                                
                                except Exception as e:
                                    st.error(f"Evaluation error: {e}")
                                    st.exception(e)
                        else:
                            st.error("Azure client not initialized. Check API keys.")
                        
                    except Exception as e:
                        st.error(f"Error generating responses: {e}")
                        st.exception(e)
    else:
        st.error("Dataset not loaded. Check data/synthetic_mental_health_dataset.jsonl")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
### ℹ️ About

**PsyChat System**

**Chat Mode:**  
Interactive AI counseling with GPT-4o or O1

**Benchmark Mode:**  
Evaluate AI quality with 6 metrics:
- ROUGE (overlap)
- METEOR (semantic)
- Ethical (professional)
- Sentiment (emotional)
- Inclusivity (LGBTQ+)
- Complexity (readability)

**Dataset:** 543 therapy sessions
""")
