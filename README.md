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

## 🚀 Quick Start (Google Colab - 100% FREE!)

### Easiest Way (No Setup Required):

1. **Upload** `AudioPsyChat_Colab.ipynb` to [Google Colab](https://colab.research.google.com)
2. **Enable GPU**: Runtime → Change runtime type → GPU → Save
3. **Run all cells**: Runtime → Run all
4. **Wait 10 minutes** for models to download
5. **Access** the public URL shown

**✅ 完全免费 ✅ 无需配置 ✅ 无需AWS ✅ 免费GPU！**

详细的英文说明请查看 `README.EN.md`



### Important Notes

To use voice input, you should allow the browser to transmit http data. Enter the following in your browser:

`chrome://flags/#unsafely-treat-insecure-origin-as-secure`

Fill in the domain name or IP and select Enabled, then click allow recording when entering the service page for recording.

## Disclaimer
Please note that this program is for learning and communication purposes only. This system is not a healthcare professional and cannot replace the opinions, diagnoses, advice, or treatment of doctors, psychologists, or other professionals. The author takes no responsibility for any consequences resulting from applying this program to healthcare.

## DEMO
Using a single RTX 3090 can ensure conversation interaction time of about 1 second per turn (VRAM usage around 16G)
[Audio PsyChat Demo](https://www.bilibili.com/video/BV13M4m1679N/)
