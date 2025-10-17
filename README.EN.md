# 🧠 PsyChat - AI Psychological Counseling Chatbot & Benchmark Evaluation

**Interactive AI counseling chatbot with comprehensive multi-turn evaluation system**

---

## 🚀 Quick Start (2 Minutes)

```bash
cd /Users/jacksonzhao/Desktop/PsyChat
./run_benchmark.sh
```

**Or manual:**
```bash
pip install -r requirements_benchmark.txt
streamlit run app.py
```

**Access:** Opens automatically at `http://localhost:8501`

---

## 🎯 Two Modes in One App

### 💬 **Chat Mode** - Interactive AI Counseling
- Chat with GPT-4o or O1 in real-time
- Trained with 543 therapeutic conversations
- Few-shot learning from reference data
- Save conversation history
- Professional counseling responses

### 📊 **Benchmark Mode** - Evaluate AI Quality
- Test AI responses against reference data
- 542 multi-turn therapy sessions
- 6 comprehensive evaluation metrics
- Turn-by-turn comparison
- Export results (CSV/JSON)
- Visual dashboards

---

## 📋 Features

### Chat Mode:
✅ **Real-time counseling** with Azure OpenAI  
✅ **Model choice** (GPT-4o or O1)  
✅ **Few-shot learning** from 543 real therapy sessions  
✅ **Custom prompts** for experimentation  
✅ **Chat history** with export  
✅ **Professional** therapeutic responses  

### Benchmark Mode:
✅ **542 reference scenarios** (depression, anxiety, PTSD, normal)  
✅ **Multi-turn evaluation** (10-20 turns per session)  
✅ **6 metrics**: ROUGE, METEOR, Ethical, Sentiment, Inclusivity, Complexity  
✅ **Turn-by-turn comparison** with visualizations  
✅ **Export capabilities** (CSV, JSON)  
✅ **Crisis assessment** scoring  
✅ **LGBTQ+ inclusivity** metrics  

---

## 📊 Evaluation Metrics

| Metric | What It Measures | Range |
|--------|------------------|-------|
| **ROUGE** | Surface text overlap with reference | 0-1 |
| **METEOR** | Semantic similarity (considers synonyms) | 0-1 |
| **Ethical** | Professional quality (LGBTQ+, crisis, social work) | 0-1 |
| **Sentiment** | Emotional tone alignment | 0-1 |
| **Inclusivity** | LGBTQ+ affirming language | 0-1 |
| **Complexity** | Readability balance | 0-1 |

---

## 🎨 How to Use

### Chat Mode:
1. Select "💬 Chat Mode" in sidebar
2. Choose model (GPT-4o recommended)
3. Type your message
4. Click "Send"
5. Get professional counseling response
6. Continue conversation
7. Save chat history if needed

### Benchmark Mode:
1. Select "📊 Benchmark Mode" in sidebar
2. Choose model to evaluate
3. Filter by condition (depression, anxiety, etc.)
4. Select a scenario from 542 sessions
5. Click "Run Evaluation"
6. View turn-by-turn comparison
7. See aggregate scores
8. Export results

---

## 📁 Project Structure

```
PsyChat/
├── app.py                          ← Streamlit app (RUN THIS)
├── run_benchmark.sh                ← Quick start script
├── requirements_benchmark.txt      ← Dependencies
│
├── benchmark/                      ← Evaluation engine
│   ├── config.py                   ← Constants & parameters
│   ├── evaluation.py               ← 6 metric algorithms
│   ├── azure_client.py             ← Azure OpenAI API
│   ├── data_loader.py              ← Dataset parser
│   └── multi_turn_evaluator.py     ← Multi-turn logic
│
├── data/
│   ├── synthetic_mental_health_dataset.jsonl  ← 542 sessions
│   └── outputs/                    ← Results storage
│
├── .streamlit/
│   └── secrets.toml                ← API keys (secure)
│
└── README.EN.md                    ← This file
```

---

## 🔧 Configuration

### API Keys
Already configured in `.streamlit/secrets.toml`:
- Azure OpenAI GPT-4o
- Azure OpenAI O1

**Security:** File is in `.gitignore` - never committed!

### Dataset
- **Location:** `data/synthetic_mental_health_dataset.jsonl`
- **Format:** JSONL (one session per line)
- **Size:** 542 therapy sessions
- **Conditions:** depression (234), anxiety (152), PTSD (89), normal (67)
- **Turns per session:** 10-20 conversations

---

## 💡 Use Cases

### 1. **Interactive Counseling**
- Test AI counseling capabilities
- Explore therapeutic conversations
- Research AI empathy and responses

### 2. **Model Comparison**
- GPT-4o vs O1 performance
- Different prompt strategies
- Ethical alignment testing

### 3. **Quality Assurance**
- Verify professional standards
- Check crisis assessment
- Ensure LGBTQ+ inclusivity

### 4. **Research & Development**
- Generate evaluation datasets
- Analyze AI counseling patterns
- Publish benchmark results
- Improve prompting strategies

---

## 📈 Example Evaluation Results

```
Scenario: DEP-b7a05b9f (Depression, 17 turns)
Model: GPT-4o

Aggregate Scores:
- ROUGE: 0.847 (high overlap with reference)
- METEOR: 0.792 (good semantic match)
- Ethical: 0.923 (excellent professional quality)
- Sentiment: 0.856 (emotional tone aligned)
- Inclusivity: 0.891 (inclusive language)
- Complexity: 0.778 (appropriate readability)

Overall: Strong performance across all metrics
```

---

## 🎯 Getting Started

### Step 1: Install Dependencies
```bash
pip install -r requirements_benchmark.txt
```

### Step 2: Run the App
```bash
streamlit run app.py
# Opens at http://localhost:8501
```

### Step 3: Choose Your Mode
- **Chat Mode**: Interactive counseling
- **Benchmark Mode**: Evaluation & analysis

---

## 🔍 Technical Details

### AI Models:
- **GPT-4o**: Latest GPT-4 with optimized performance
- **O1**: Reasoning-focused model
- **Azure OpenAI**: Enterprise-grade API

### Training Data:
- 542 synthetic therapy sessions
- Multi-condition (depression, anxiety, PTSD, normal)
- Professional counselor responses
- 10-20 turn conversations

### Evaluation Algorithm:
- Comprehensive 6-metric scoring
- Turn-by-turn and aggregate analysis
- Weighted scoring (ethical emphasis)
- Crisis and inclusivity assessment

---

## ⚠️ Important Notes

### Disclaimer
**For educational and research purposes only.**

This system is **NOT**:
- A replacement for professional therapy
- Medical advice
- Emergency mental health service
- Licensed counseling

**In crisis?**
- Call 911 (Emergency)
- Call 988 (Suicide Prevention)
- Text HOME to 741741 (Crisis Text Line)

### Security
- API keys in `.streamlit/secrets.toml` (protected)
- Never commit secrets to Git
- Dataset is synthetic (not real patient data)

### Limitations
- AI responses are computational
- Evaluation is comparative (not absolute)
- Requires human oversight
- Not for actual patient care

---

## 🆘 Troubleshooting

### "Module not found"
```bash
pip install -r requirements_benchmark.txt
```

### "API key error"
Check `.streamlit/secrets.toml` has correct keys

### "Dataset not found"
Verify `data/synthetic_mental_health_dataset.jsonl` exists

### "Streamlit won't start"
```bash
pip install --upgrade streamlit
streamlit run app.py
```

---

## 🤝 Contributing

Contributions welcome!
- Additional metrics
- More AI models
- UI improvements
- Documentation

---

## 📄 License

Copyright © 2025 Zichen Zhao  
Columbia University School of Social Work  
MIT Academic Research License

---

## 🎉 You're Ready!

```bash
./run_benchmark.sh
```

**Two powerful systems in one:**
1. Chat with AI counselor
2. Evaluate AI quality

**All running locally on your Mac!** 🚀
