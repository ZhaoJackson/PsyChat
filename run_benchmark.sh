#!/bin/bash
# Quick start script for Audio PsyChat Benchmark Evaluation

echo "🎤 Audio PsyChat - Multi-Turn Benchmark Evaluation"
echo "=================================================="
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the PsyChat directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv_benchmark" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv_benchmark
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv_benchmark/bin/activate

# Install dependencies
if [ ! -f "venv_benchmark/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -q --upgrade pip
    pip install -q -r requirements_benchmark.txt
    touch venv_benchmark/.installed
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

# Download NLTK data (required for evaluation)
echo "📚 Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('cmudict', quiet=True)"

echo ""
echo "🚀 Starting Streamlit app..."
echo "=================================================="
echo ""
echo "📱 The app will open in your browser automatically"
echo "🌐 Or go to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run Streamlit
streamlit run app.py

