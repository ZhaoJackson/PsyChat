# 🎤 Audio PsyChat - Multi-Turn Benchmark Evaluation System

**Evaluate AI chatbots for psychological counseling using multi-turn conversation benchmarks.**

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_benchmark.txt
```

### 2. Configure API Keys
The API keys are already set in `.streamlit/secrets.toml`

### 3. Run Streamlit App
```bash
streamlit run app.py
```

### 4. Use the Interface
1. **Select AI Model** (GPT-4o or O1) in sidebar
2. **Choose a scenario** from the dataset
3. **Click "Run Evaluation"** to generate AI responses
4. **View results** with turn-by-turn comparison and aggregate scores

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  STREAMLIT INTERFACE                     │
│  - Scenario selection                                    │
│  - Model configuration                                   │
│  - Results visualization                                 │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│              DATA LOADING & PARSING                      │
│  - Load JSONL dataset                                    │
│  - Parse multi-turn conversations                        │
│  - Extract patient/doctor turns                          │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│           AI RESPONSE GENERATION                         │
│  - Azure OpenAI API (GPT-4o / O1)                       │
│  - Maintain conversation context                         │
│  - Generate turn-by-turn responses                       │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│           MULTI-TURN EVALUATION                          │
│  Per Turn:                                               │
│    - ROUGE (surface overlap)                             │
│    - METEOR (semantic similarity)                        │
│    - Ethical Alignment (professional quality)            │
│    - Sentiment Distribution (emotional tone)             │
│    - Inclusivity (LGBTQ+ affirming language)            │
│    - Complexity (readability balance)                    │
│                                                          │
│  Aggregate:                                              │
│    - Average scores across turns                         │
│    - Min/max scores                                      │
│    - Overall conversation quality                        │
└─────────────────────────────────────────────────────────┘
                         │
                         ↓
┌─────────────────────────────────────────────────────────┐
│              RESULTS & VISUALIZATION                     │
│  - Turn-by-turn comparison                               │
│  - Aggregate score charts                                │
│  - Export to CSV/JSON                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
PsyChat/
├── app.py                           ← Streamlit interface (RUN THIS)
│
├── benchmark/                       ← Evaluation system
│   ├── __init__.py
│   ├── config.py                   ← Constants and configuration
│   ├── evaluation.py               ← Evaluation algorithms
│   ├── azure_client.py             ← Azure OpenAI API wrapper
│   ├── data_loader.py              ← Dataset loading & parsing
│   └── multi_turn_evaluator.py     ← Multi-turn evaluation logic
│
├── data/
│   ├── synthetic_mental_health_dataset.jsonl  ← Reference data (543 sessions)
│   └── outputs/                    ← Evaluation results
│       ├── scores.csv
│       ├── detailed_results.json
│       └── plots/
│
├── .streamlit/
│   └── secrets.toml                ← API keys (DO NOT COMMIT!)
│
├── requirements_benchmark.txt      ← Python dependencies
└── BENCHMARK_README.md             ← This file
```

---

## 📋 Evaluation Metrics

### 1. **ROUGE Score** (Surface-Level Overlap)
- Measures token overlap between reference and AI response
- Weighted combination of ROUGE-1, ROUGE-2, and ROUGE-L
- Range: 0.0 - 1.0 (higher = better overlap)

### 2. **METEOR Score** (Semantic Similarity)
- Considers synonyms and word order
- Better for evaluating meaning vs exact words
- Range: 0.0 - 1.0 (higher = better semantic match)

### 3. **Ethical Alignment** (Professional Quality)
- Evaluates presence of:
  - LGBTQ+ affirming language (25% weight)
  - Social work professional terms (20% weight)
  - Crisis assessment competency (20% weight)
  - Supportive language (15% weight)
  - Question quality (10% weight)
  - Comprehensiveness (10% weight)
- Penalties for judgmental or harmful language
- Range: 0.0 - 1.0

### 4. **Sentiment Distribution** (Emotional Tone)
- Compares emotional tone between reference and AI
- Uses cosine similarity of weighted emotion vectors
- Considers therapeutic value of emotions
- Range: 0.0 - 1.0 (higher = better emotional alignment)

### 5. **Inclusivity Score** (Affirming Language)
- Rewards LGBTQ+ affirming and inclusive terms
- Penalizes stigmatizing language
- Range: 0.0 - 1.0

### 6. **Complexity Score** (Readability)
- Balances readability with nuanced language
- Uses Flesch-Kincaid + sentence complexity
- Appropriate for mental health communication

---

## 🎯 Usage Examples

### Basic Evaluation
```bash
# Run Streamlit app
streamlit run app.py

# In the interface:
1. Select model: GPT-4o
2. Choose scenario: DEP-b7a05b9f
3. Click "Run Evaluation"
4. View results in Results tab
```

### Evaluate Multiple Scenarios
```python
# In Python script or notebook
from benchmark.data_loader import get_all_scenarios
from benchmark.azure_client import create_client_from_secrets
from benchmark.multi_turn_evaluator import MultiTurnEvaluator

# Load scenarios
scenarios = get_all_scenarios(condition='depression', limit=10)

# Create AI client
client = create_client_from_secrets("GPT-4o", secrets)

# Evaluate all
evaluator = MultiTurnEvaluator()
all_results = []

for scenario in scenarios:
    patient_msgs = [turn['patient'] for turn in scenario['turns']]
    ai_responses = client.generate_multi_turn_conversation(patient_msgs)
    result = evaluator.evaluate_conversation(scenario['turns'], ai_responses)
    all_results.append(result)

# Export results
evaluator.export_results_to_csv(all_results, 'data/outputs/batch_evaluation.csv')
```

---

## 📊 Dataset Information

**Source:** `data/synthetic_mental_health_dataset.jsonl`

**Format:** JSONL (one JSON object per line)

**Structure:**
```json
{
  "patient_id": "DEP-b7a05b9f",
  "condition": "depression",
  "session_id": 1,
  "input": "Patient: ...\nDoctor: ...\nPatient: ...\nDoctor: ...",
  "risk_flag": "yes",
  "session_state": {...}
}
```

**Statistics:**
- Total sessions: 543
- Conditions: Depression, Anxiety, PTSD, etc.
- Average turns per session: 10-20
- Multi-turn therapeutic dialogues

---

## 🔧 Configuration

### API Keys
Edit `.streamlit/secrets.toml` if you need to update credentials:

```toml
[azure_openai_4o]
api_key = "your-key-here"
endpoint = "your-endpoint-here"
api_version = "2024-12-01-preview"
deployment = "gpt-4o"
```

### Evaluation Parameters
Edit `benchmark/config.py` to adjust:
- Emotion weights
- Ethical term lists
- LGBTQ+ affirming terms
- Complexity parameters

---

## 📈 Output Files

### Aggregate Scores CSV
```csv
patient_id,condition,session_id,model,avg_rouge_score,avg_meteor_score,...
DEP-001,depression,1,GPT-4o,0.85,0.78,0.92,...
```

### Turn-by-Turn CSV
```csv
patient_id,turn,patient_message,reference_response,ai_response,rouge_score,meteor_score,...
DEP-001,1,"I feel down...","Thank you for sharing...","I hear that you...",0.82,0.75,...
```

### Detailed JSON
Complete results with full text and all metadata

---

## 🎨 Streamlit Interface Features

### Scenario View Tab
- Display full reference conversation
- Show patient messages and doctor responses
- View session metadata (condition, risk flags, etc.)

### Run Evaluation Tab
- Select AI model (GPT-4o or O1)
- Optional custom system prompt
- Run evaluation with progress indication
- Real-time feedback

### Results Tab
- Aggregate scores summary table
- Visual charts (bar charts, radar plots)
- Turn-by-turn detailed comparison
- Export options (CSV, JSON)

---

## 🔍 How It Works

### 1. Load Scenario
```python
scenario = get_scenario_by_id("DEP-b7a05b9f")
# Parses: Patient: X \n Doctor: Y \n Patient: Z \n Doctor: W
# Into turns: [{patient: X, doctor: Y}, {patient: Z, doctor: W}]
```

### 2. Generate AI Responses
```python
client = AzureOpenAIClient("GPT-4o", ...)
patient_messages = ["I feel down", "It's been a month", ...]

ai_responses = client.generate_multi_turn_conversation(patient_messages)
# Returns: [{turn: 1, ai_response: "..."}, {turn: 2, ai_response: "..."}]
```

### 3. Evaluate Each Turn
```python
evaluator = MultiTurnEvaluator()

for turn in range(num_turns):
    scores = evaluator.evaluate_turn(
        reference_response=scenario['turns'][turn]['doctor'],
        ai_response=ai_responses[turn]['ai_response']
    )
    # scores = {rouge: 0.85, meteor: 0.78, ethical: 0.92, ...}
```

### 4. Aggregate & Display
```python
aggregate_scores = calculate_averages(all_turn_scores)
# Display in Streamlit with charts
```

---

## 🎯 Use Cases

### 1. **Model Comparison**
- Evaluate GPT-4o vs O1
- Compare against reference human responses
- Identify strengths and weaknesses

### 2. **Prompt Engineering**
- Test different system prompts
- Optimize for specific metrics
- Improve ethical alignment

### 3. **Quality Assurance**
- Ensure AI meets professional standards
- Verify crisis assessment capability
- Check LGBTQ+ inclusivity

### 4. **Research**
- Generate evaluation datasets
- Analyze AI counseling patterns
- Publish benchmark results

---

## ⚠️ Important Notes

### Security
- **DO NOT commit `.streamlit/secrets.toml` to Git!**
- It's already in `.gitignore`
- Keep API keys private

### Dataset
- Synthetic mental health conversations
- For research and evaluation only
- Not for actual patient care

### Limitations
- Evaluation is comparative (vs reference)
- Does not replace human judgment
- Metrics are computational approximations

---

## 🚀 Next Steps

1. **Run the app**: `streamlit run app.py`
2. **Explore scenarios**: Browse the 543 therapy sessions
3. **Run evaluations**: Test GPT-4o and O1
4. **Analyze results**: Compare scores and export data
5. **Optimize**: Adjust prompts and parameters

---

**The system is ready to use! Start evaluating AI chatbots for psychological counseling!** 🎉

