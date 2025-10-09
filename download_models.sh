#!/bin/bash
# Download PsyChat model files from HuggingFace

echo "📥 Downloading PsyChat model files from HuggingFace..."
echo "⚠️  This will download ~7GB of model files"
echo ""

# Check if huggingface-hub is installed
if ! python -c "import huggingface_hub" 2>/dev/null; then
    echo "Installing huggingface-hub..."
    pip install huggingface-hub
fi

# Create PsyChat directory if it doesn't exist
mkdir -p PsyChat

# Download all model files
echo "🔄 Starting download..."
huggingface-cli download qiuhuachuan/PsyChat --local-dir ./PsyChat --local-dir-use-symlinks False

echo ""
echo "✅ Download complete!"
echo "📁 Model files saved to: ./PsyChat/"
echo ""
echo "📋 Verifying files..."

# Verify required files exist
REQUIRED_FILES=(
    "PsyChat/config.json"
    "PsyChat/generation_config.json"
    "PsyChat/pytorch_model.bin.index.json"
    "PsyChat/special_tokens_map.json"
    "PsyChat/tokenizer_config.json"
    "PsyChat/tokenizer.model"
)

REQUIRED_DIRS=(
    "PsyChat/pytorch_model-00001-of-00007"
    "PsyChat/pytorch_model-00002-of-00007"
    "PsyChat/pytorch_model-00003-of-00007"
    "PsyChat/pytorch_model-00004-of-00007"
    "PsyChat/pytorch_model-00005-of-00007"
    "PsyChat/pytorch_model-00006-of-00007"
    "PsyChat/pytorch_model-00007-of-00007"
)

ALL_GOOD=true

echo "Checking files..."
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        ALL_GOOD=false
    fi
done

echo "Checking model directories..."
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir"
    else
        echo "❌ $dir (missing)"
        ALL_GOOD=false
    fi
done

echo ""
if [ "$ALL_GOOD" = true ]; then
    echo "🎉 All model files downloaded successfully!"
    echo "🚀 You can now run the application with: python main.py"
else
    echo "⚠️  Some files are missing. Please check the download."
    echo "💡 You can also download manually from: https://huggingface.co/qiuhuachuan/PsyChat"
fi
