#!/bin/bash
# Deploy Audio PsyChat to AWS EC2

# Configuration - UPDATE THESE VALUES
EC2_IP="YOUR_EC2_PUBLIC_IP"  # You'll get this after launching
KEY_PATH="$HOME/.ssh/PsyChat.pem"  # Update this path to your key file
PROJECT_DIR="/Users/jacksonzhao/Desktop/PsyChat"

echo "🚀 Deploying Audio PsyChat to AWS EC2..."

# Check if EC2_IP is set
if [ "$EC2_IP" = "YOUR_EC2_PUBLIC_IP" ]; then
    echo "❌ Please update EC2_IP in this script with your actual EC2 public IP"
    exit 1
fi

# Check if key file exists
if [ ! -f "$KEY_PATH" ]; then
    echo "❌ Please update KEY_PATH in this script with your actual key file path"
    exit 1
fi

# Create deployment package (excluding large files)
echo "📦 Creating deployment package..."
cd "$PROJECT_DIR"
tar -czf psychat_deploy.tar.gz \
    --exclude='PsyChat/*.bin' \
    --exclude='web/wavs/*.wav' \
    --exclude='web/wavs/*.webm' \
    --exclude='test/input_audio.*' \
    --exclude='test/output.wav' \
    --exclude='test/exp/' \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    .

# Upload to EC2
echo "📤 Uploading to EC2..."
scp -i "$KEY_PATH" psychat_deploy.tar.gz ubuntu@$EC2_IP:/home/ubuntu/

# Connect and setup
echo "🔧 Setting up on EC2..."
ssh -i "$KEY_PATH" ubuntu@$EC2_IP << 'ENDSSH'
    # Extract project
    cd /home/ubuntu
    tar -xzf psychat_deploy.tar.gz -C AudioPsyChat/
    cd AudioPsyChat
    
    # Setup conda environment
    source ~/.bashrc
    bash init_env.sh
    
    # Create model directory and required directories
    mkdir -p PsyChat test web/wavs
    
    # Make scripts executable
    chmod +x start_server.sh
    
    # Test GPU availability
    if command -v nvidia-smi &> /dev/null; then
        echo "🎮 GPU detected:"
        nvidia-smi --query-gpu=name --format=csv,noheader
    else
        echo "⚠️  No GPU detected"
    fi
    
    echo "✅ Project uploaded and configured successfully!"
    echo "📋 Next steps:"
    echo "1. Upload model files: ./upload_models.sh"
    echo "2. Start server: ./start_server.sh"
    echo "3. Access at: http://$EC2_IP:8086/static"
    echo "4. Health check: http://$EC2_IP:8086/health"
ENDSSH

# Cleanup
rm psychat_deploy.tar.gz

echo "🎉 Deployment complete!"
echo "🌐 Your app will be available at: http://$EC2_IP:8086/static"
