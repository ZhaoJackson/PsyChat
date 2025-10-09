# Audio PsyChat: Web-based Voice Psychological Counseling System

This is a web-based voice psychological counseling system that runs locally on a server. The counseling system core uses [PsyChat](https://github.com/qiuhuachuan/PsyChat), for which we have created a Web frontend and integrated ASR and TTS components, allowing users within the local network to interact purely through voice. The ASR and TTS components use [PaddleSpeech](https://github.com/PaddlePaddle/PaddleSpeech) API.

## Usage

We recommend using Ubuntu 20.04.6 LTS system with CUDA-supported graphics card (VRAM greater than 16G). The system CUDA driver version should not be lower than 11.7, with 12.0 recommended. For python, pytorch, paddle and other version details, see init_env.sh.

### Environment Setup

First download the following model files from [PsyChat directory on HuggingFace](https://huggingface.co/qiuhuachuan/PsyChat/tree/main):

- https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00001-of-00007.bin
- https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00002-of-00007.bin
- https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00003-of-00007.bin
- https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00004-of-00007.bin
- https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00005-of-00007.bin
- https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00006-of-00007.bin
- https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00007-of-00007.bin

to the `AudioPsyChat/PsyChat/` directory

## Running

```bash
# Extract files and enter project directory
cd AudioPsyChat/
# Run environment creation/initialization script (requires pre-installed anaconda/miniconda)
bash init_env.sh
# Run backend program and web server
python main.py
# Access server_ip:8086/static page for interaction
```



### Important Notes

To use voice input, you should allow the browser to transmit http data. Enter the following in your browser:

`chrome://flags/#unsafely-treat-insecure-origin-as-secure`

Fill in the domain name or IP and select Enabled, then click allow recording when entering the service page for recording.

## Disclaimer
Please note that this program is for learning and communication purposes only. This system is not a healthcare professional and cannot replace the opinions, diagnoses, advice, or treatment of doctors, psychologists, or other professionals. The author takes no responsibility for any consequences resulting from applying this program to healthcare.

## DEMO
Using a single RTX 3090 can ensure conversation interaction time of about 1 second per turn (VRAM usage around 16G)
[Audio PsyChat Demo](https://www.bilibili.com/video/BV13M4m1679N/)
