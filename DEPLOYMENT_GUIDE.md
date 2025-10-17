# 🚀 PsyChat Deployment Guide

## 📋 Two Deployment Options

### 🌐 **Streamlit Cloud Deployment** (Public)
- **File**: `requirements.txt` (minimal dependencies)
- **Python**: 3.13 (Streamlit Cloud default)
- **Evaluation**: Simplified (keyword-based sentiment)
- **Dependencies**: Only packages with pre-built wheels

### 💻 **Local Development** (Full Features)
- **File**: `requirements_local.txt` (full dependencies)
- **Python**: 3.11 (recommended)
- **Evaluation**: Complete ML-based evaluation
- **Dependencies**: All packages including transformers, torch, etc.

---

## 🔧 How to Switch Between Versions

### For Streamlit Cloud Deployment:
```bash
# Use requirements.txt (already configured)
git add requirements.txt
git commit -m "Deploy to Streamlit Cloud"
git push
```

### For Local Development:
```bash
# Install full dependencies
pip install -r requirements_local.txt

# Uncomment the ML evaluation code in:
# - benchmark/evaluation.py (lines 31-40, 313-328)
# - benchmark/config.py (lines 72-73)
```

---

## 📊 Evaluation System Comparison

| Feature | Streamlit Cloud | Local Development |
|---------|----------------|-------------------|
| **ROUGE** | ✅ Full | ✅ Full |
| **METEOR** | ✅ Full | ✅ Full |
| **Ethical** | ✅ Full | ✅ Full |
| **Sentiment** | 🔄 Keyword-based | ✅ ML-based |
| **Inclusivity** | ✅ Full | ✅ Full |
| **Complexity** | ✅ Full | ✅ Full |

---

## 🎯 Quick Start

### Local Development (Recommended):
```bash
cd /Users/jacksonzhao/Desktop/PsyChat
pip install -r requirements_local.txt
streamlit run app.py
```

### Streamlit Cloud:
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

---

## 🔄 Switching Between Versions

### To Enable Full Local Evaluation:
1. Uncomment lines 31-40 in `benchmark/evaluation.py`
2. Uncomment lines 313-328 in `benchmark/evaluation.py`
3. Uncomment lines 72-73 in `benchmark/config.py`
4. Install: `pip install -r requirements_local.txt`

### To Deploy to Streamlit Cloud:
1. Comment out the ML evaluation code
2. Use `requirements.txt`
3. Push to GitHub

---

## ✅ Your Evaluation System is Preserved!

- **All algorithms intact**: Just commented out for cloud deployment
- **Easy switching**: Uncomment for local, comment for cloud
- **No data loss**: All your evaluation logic is preserved
- **Both versions work**: Local (full) and Cloud (simplified)
