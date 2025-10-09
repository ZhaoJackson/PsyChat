# PsyChat Model Directory

This directory contains the PsyChat model files required for the psychological counseling system.

## Required Model Files

Due to their large size (several GB), the model files are not included in the Git repository. You must download them manually from HuggingFace.

### Download Instructions

1. **Visit HuggingFace**: [PsyChat Model Repository](https://huggingface.co/qiuhuachuan/PsyChat/tree/main)

2. **Download these files** and place them in this directory:
   ```
   PsyChat/
   ├── config.json                     ✅ (included in repo)
   ├── generation_config.json          ✅ (included in repo)  
   ├── pytorch_model.bin.index.json    ✅ (included in repo)
   ├── special_tokens_map.json         ✅ (included in repo)
   ├── tokenizer_config.json           ✅ (included in repo)
   ├── tokenizer.model                 ❌ (download required - 1MB)
   ├── pytorch_model-00001-of-00007/   ❌ (download required - ~1GB)
   ├── pytorch_model-00002-of-00007/   ❌ (download required - ~1GB)
   ├── pytorch_model-00003-of-00007/   ❌ (download required - ~1GB)
   ├── pytorch_model-00004-of-00007/   ❌ (download required - ~1GB)
   ├── pytorch_model-00005-of-00007/   ❌ (download required - ~1GB)
   ├── pytorch_model-00006-of-00007/   ❌ (download required - ~1GB)
   └── pytorch_model-00007-of-00007/   ❌ (download required - ~1GB)
   ```

3. **Total download size**: ~7GB

### Direct Download Links

- [tokenizer.model](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/tokenizer.model)
- [pytorch_model-00001-of-00007.bin](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00001-of-00007.bin)
- [pytorch_model-00002-of-00007.bin](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00002-of-00007.bin)
- [pytorch_model-00003-of-00007.bin](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00003-of-00007.bin)
- [pytorch_model-00004-of-00007.bin](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00004-of-00007.bin)
- [pytorch_model-00005-of-00007.bin](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00005-of-00007.bin)
- [pytorch_model-00006-of-00007.bin](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00006-of-00007.bin)
- [pytorch_model-00007-of-00007.bin](https://huggingface.co/qiuhuachuan/PsyChat/blob/main/pytorch_model-00007-of-00007.bin)

### Automated Download (Alternative)

You can also use the HuggingFace CLI to download all files:

```bash
# Install huggingface-hub
pip install huggingface-hub

# Download all model files
huggingface-cli download qiuhuachuan/PsyChat --local-dir ./PsyChat
```

## File Descriptions

- **`config.json`**: Model configuration parameters
- **`generation_config.json`**: Text generation settings
- **`pytorch_model.bin.index.json`**: Index mapping for model shards
- **`special_tokens_map.json`**: Special token definitions
- **`tokenizer_config.json`**: Tokenizer configuration
- **`tokenizer.model`**: SentencePiece tokenizer model (1MB)
- **`pytorch_model-*-of-*.bin`**: Model weight files (sharded into 7 parts)

## Verification

After downloading, verify you have all required files:

```bash
ls -la PsyChat/
# Should show all config files plus the 7 pytorch_model directories and tokenizer.model
```

The application will fail to start if any of these files are missing.

## Note for Deployment

When deploying to AWS EC2, use the `upload_models.sh` script to transfer these files to your instance after the initial code deployment.
