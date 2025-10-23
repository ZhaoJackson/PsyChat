# PsyChat - Clinical Trial Mobile Application

A Streamlit-based chatbot evaluation system designed for **clinical trial mobile application usage** with setting clinical mental health benchmark evaluation of AI response in multi-turn fashion. This application guides users to understand AI responses and learn how to interact with AI while resolving personal mental health issues.

🌐 **Live Demo**: [https://psychatbot.streamlit.app/](https://psychatbot.streamlit.app/)

## 🏥 Clinical Trial Focus

This application is specifically designed for:
- **Clinical Mental Health Research**: Setting benchmarks for AI therapeutic responses
- **Multi-turn Dialogue Evaluation**: Assessing AI performance across conversation turns
- **User Education**: Teaching users how to effectively interact with AI for mental health support
- **Personal Mental Health Resolution**: Guiding users through AI-assisted therapeutic conversations

## 🚀 Quick Start

```bash
# Start the application
./start.sh
```

Or manually:
```bash
source venv_benchmark/bin/activate
streamlit run app.py
```

## 📊 Clinical Features

- **Real-time Therapeutic Evaluation**: ML-based metrics for each AI response in clinical settings
- **Multi-turn Clinical Conversations**: Track AI performance across therapeutic dialogue turns
- **Clinical Benchmark Metrics**: ROUGE, METEOR, Sentiment, Ethical Alignment, Inclusivity, Complexity
- **Azure OpenAI Integration**: GPT-4o and O1 model support for clinical trials
- **Human Therapist Reference Comparison**: Compare AI responses against licensed therapist references
- **User Learning Interface**: Guide users to understand and improve AI interaction patterns
- **Personal Mental Health Support**: Assist users in resolving mental health issues through AI guidance

## 🎯 Clinical Evaluation Metrics

- **ROUGE Score**: Therapeutic text overlap and similarity assessment
- **METEOR Score**: Clinical semantic similarity with therapeutic synonyms
- **Sentiment Distribution**: Emotional alignment analysis for mental health contexts
- **Ethical Alignment**: Clinical safety and therapeutic appropriateness scoring
- **Inclusivity Score**: Bias detection and fairness in mental health support
- **Complexity Score**: Therapeutic readability and accessibility for clinical users

## 📁 Project Structure

```
PsyChat/
├── app.py                    # Main Streamlit application
├── start.sh                  # Quick start script
├── requirements.txt          # All dependencies
├── venv_benchmark/          # Python virtual environment
├── benchmark/               # Evaluation algorithms
│   ├── config.py           # Configuration and constants
│   ├── evaluation.py       # ML evaluation functions
│   ├── azure_client.py    # Azure OpenAI client
│   └── multi_turn_evaluator.py
├── data/                    # Dataset and outputs
│   └── synthetic_mental_health_dataset.jsonl
└── ../outputs/             # Results and plots (outside project)
```

## 🔧 Setup

1. **Install Dependencies**:
   ```bash
   python3.11 -m venv venv_benchmark
   source venv_benchmark/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Azure OpenAI**:
   - Add your API keys to `.streamlit/secrets.toml`
   - Set up your Azure OpenAI endpoints

3. **Run the App**:
   ```bash
   ./start.sh
   ```

## 📈 Clinical Usage

1. **Select AI Model**: Choose between GPT-4o or O1 for clinical trial testing
2. **Load Clinical Scenario**: Pick a reference therapeutic conversation from the clinical dataset
3. **Therapeutic Chat**: Interact with the AI and see real-time clinical evaluation scores
4. **Compare with Therapist**: View licensed therapist reference responses alongside AI responses
5. **Clinical Session Summary**: Get aggregate metrics for the entire therapeutic conversation
6. **User Learning**: Understand how to effectively interact with AI for mental health support
7. **Personal Resolution**: Use AI guidance to work through personal mental health challenges

## 🎯 Clinical Output

Results are saved to `../outputs/` (outside the project directory):
- `evaluation_scores.csv`: Detailed clinical metrics
- `turn_by_turn_scores.csv`: Per-turn therapeutic analysis
- `plots/`: Clinical visualization charts

## 🔄 Clinical Deployment

**Local Development**: Full ML evaluation with all dependencies for clinical research
**Streamlit Cloud**: Simplified fallback algorithms for cloud compatibility - [Live Demo](https://psychatbot.streamlit.app/)

Switch between modes by commenting/uncommenting ML code in `benchmark/evaluation.py` and `benchmark/config.py`.

## 🏥 Clinical Trial Applications

This application is designed for:
- **Mobile Clinical Trials**: Testing AI therapeutic responses in mobile environments
- **Mental Health Research**: Benchmarking AI performance against human therapists
- **User Education**: Teaching effective AI interaction for mental health support
- **Personal Therapy**: Guiding users through AI-assisted mental health resolution