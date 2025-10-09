#!/bin/bash
# EC2-optimized startup script for Audio PsyChat

echo "🚀 Starting Audio PsyChat Server..."

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export CUDA_VISIBLE_DEVICES=0

# Check if running on EC2
if curl -s --max-time 3 http://169.254.169.254/latest/meta-data/instance-id > /dev/null 2>&1; then
    echo "✅ Running on EC2 instance"
    INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
    echo "📍 Instance ID: $INSTANCE_ID"
    echo "🌐 Public IP: $PUBLIC_IP"
    echo "🔗 Access URL: http://$PUBLIC_IP:8086/static"
else
    echo "💻 Running locally"
fi

# Check GPU availability
if command -v nvidia-smi &> /dev/null; then
    echo "🎮 GPU Status:"
    nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader,nounits
else
    echo "⚠️  No GPU detected - running on CPU (will be slower)"
fi

# Check disk space
echo "💾 Disk usage:"
df -h . | tail -1

# Check memory
echo "🧠 Memory usage:"
free -h

# Activate conda environment if it exists
if [ -d "$HOME/miniconda3/envs/AuPC38" ]; then
    echo "🐍 Activating conda environment..."
    source $HOME/miniconda3/etc/profile.d/conda.sh
    conda activate AuPC38
fi

# Start the server
echo "🌟 Starting FastAPI server..."
echo "📱 Access the app at: http://localhost:8086/static (or use public IP if on EC2)"
echo "🔍 Health check: http://localhost:8086/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================="

python main.py
