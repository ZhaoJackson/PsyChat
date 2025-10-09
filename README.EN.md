# Audio PsyChat: Web-based Voice Psychological Counseling System

This is a web-based voice psychological counseling system that runs locally on a server. The counseling system core uses [PsyChat](https://github.com/qiuhuachuan/PsyChat), for which we have created a Web frontend and integrated ASR and TTS components, allowing users within the local network to interact purely through voice. The ASR and TTS components use [PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech) API.

## System Architecture

The backend is comprised of 3 main components:
- **ASR (Automatic Speech Recognition)**: Converts user voice input to text
- **LLM (Large Language Model)**: PsyChat model for psychological counseling responses
- **TTS (Text-to-Speech)**: Converts counselor responses back to audio

## Features

- 🎤 **Voice Interaction**: Pure voice-based communication with the psychological counseling system
- 🌐 **Web Interface**: Accessible through any modern web browser
- 🏠 **Local Deployment**: Runs entirely on local server for privacy
- 🧠 **Professional Counseling**: Uses specialized PsyChat model trained for psychological counseling
- 💬 **Chat History**: Maintains conversation context throughout sessions
- 🔊 **Audio Playback**: Text-to-speech for counselor responses

## Quick Start

### 1. Download Model Files
```bash
# Automated download (recommended)
./download_models.sh

# Manual download from HuggingFace if needed
# Visit: https://huggingface.co/qiuhuachuan/PsyChat/tree/main
```

### 2. AWS Cloud Deployment (Recommended)

**Quick Setup:**
```bash
# 1. Request AWS GPU quota (if needed)
# 2. Deploy infrastructure using aws_cloudformation.yaml
# 3. Deploy application
./deploy_to_aws.sh
./upload_models.sh
# 4. SSH and start: ./start_server.sh
```

**Access:** `http://your-ec2-ip:8086/static`

## System Requirements

- **GPU**: NVIDIA GPU with >16GB VRAM (for optimal performance)
- **CPU**: Multi-core processor (CPU-only mode available but slower)
- **Memory**: 16GB+ RAM recommended
- **Storage**: 10GB+ for model files and dependencies

## File Structure

```
PsyChat/
├── 🔧 Core Application
│   ├── main.py                    # FastAPI server
│   ├── api/                       # API modules
│   ├── web/                       # Web frontend
│   └── chatglm2-6b/              # ChatGLM components
├── 📦 Model Files (download required)
│   └── PsyChat/                   # Model directory
├── 🚀 Deployment
│   ├── aws_cloudformation.yaml    # AWS infrastructure
│   ├── deploy_to_aws.sh          # Code deployment
│   ├── upload_models.sh          # Model upload
│   ├── download_models.sh        # Model download
│   └── start_server.sh           # Application startup
└── 📚 Documentation
    ├── README.md                  # Chinese documentation
    ├── README.EN.md              # English documentation
    └── DEPLOYMENT.md             # Deployment guide
```

## API Endpoints

- `GET /static` - Web interface
- `GET /health` - Health check
- `POST /api/audio_to_audio` - Voice interaction
- `POST /api/text_to_audio` - Text interaction

## Performance

- **Hardware**: Single RTX 3090 GPU recommended
- **Response Time**: ~1 second per conversation turn
- **VRAM Usage**: ~16GB
- **Concurrent Users**: Multiple users supported

## Cost Estimates (AWS)

- **On-demand g4dn.xlarge**: ~$0.53/hour
- **Spot instances**: ~$0.20/hour (up to 70% savings)
- **Daily usage (8 hours)**: $1.60-4.20
- **Stop when not in use**: Save ~90% of costs

## Browser Configuration

For voice input, enable HTTP data transmission:
1. Go to: `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
2. Add your server IP/domain
3. Select "Enabled"
4. Restart browser

## Troubleshooting

- **GPU Issues**: Verify CUDA installation and GPU memory
- **Model Loading**: Ensure all model files are downloaded
- **Connection Issues**: Check security group port 8086
- **Performance**: Monitor GPU usage with `nvidia-smi`

## Disclaimer

⚠️ **Important Notice**: This program is for educational and research purposes only. This system is not a healthcare professional and cannot replace the opinions, diagnoses, advice, or treatment of doctors, psychologists, or other medical professionals. The authors take no responsibility for any consequences resulting from applying this program to healthcare scenarios.

## Demo

Watch the system in action: [Audio PsyChat Demo](https://www.bilibili.com/video/BV13M4m1679N/)

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

Please refer to the original PsyChat repository for licensing information.
