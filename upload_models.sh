#!/bin/bash
# Upload PsyChat model files to AWS EC2

# Configuration - UPDATE THESE VALUES
EC2_IP="YOUR_EC2_PUBLIC_IP"  # You'll get this after launching
KEY_PATH="$HOME/.ssh/PsyChat.pem"  # Update this path to your key file
LOCAL_MODEL_DIR="/Users/jacksonzhao/Desktop/PsyChat/PsyChat"

echo "📤 Uploading PsyChat model files to AWS EC2..."

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

# Check if model directory exists
if [ ! -d "$LOCAL_MODEL_DIR" ]; then
    echo "❌ Model directory not found: $LOCAL_MODEL_DIR"
    exit 1
fi

# Upload model files
echo "📦 Uploading model files (this may take a while)..."
scp -i "$KEY_PATH" -r "$LOCAL_MODEL_DIR"/* ubuntu@$EC2_IP:/home/ubuntu/AudioPsyChat/PsyChat/

echo "✅ Model files uploaded successfully!"
echo "🚀 You can now start the application on EC2:"
echo "   ssh -i $KEY_PATH ubuntu@$EC2_IP"
echo "   cd AudioPsyChat"
echo "   python main.py"
