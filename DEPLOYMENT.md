# Audio PsyChat - AWS Deployment Guide

## 🚀 Quick Deployment Steps

### 1. Prerequisites
- AWS Account with EC2 access
- EC2 Key Pair created
- Model files downloaded from HuggingFace

### 2. Request GPU Quota (if needed)
```
AWS Console → Service Quotas → EC2 → "Running On-Demand G and VT instances"
Request: 4 vCPUs (usually approved in 15-30 minutes)
```

### 3. Deploy Infrastructure
**Option A: CloudFormation (Automated)**
- Upload `aws_cloudformation.yaml` to AWS CloudFormation
- Provide Key Pair name
- Deploy

**Option B: Manual EC2 Launch**
- Instance: g4dn.xlarge
- AMI: ami-0ec4ab14b1c5a10f2 (Deep Learning AMI Ubuntu 22.04)
- Storage: 85GB gp3
- Security Group: Ports 22, 8086, 80, 443

### 4. Deploy Application
```bash
# 1. Update deployment scripts with your EC2 IP and key path
# Edit deploy_to_aws.sh and upload_models.sh

# 2. Deploy code
./deploy_to_aws.sh

# 3. Upload model files
./upload_models.sh

# 4. SSH and start
ssh -i your-key.pem ubuntu@your-ec2-ip
cd AudioPsyChat
./start_server.sh
```

### 5. Access Application
- **Web Interface**: `http://your-ec2-ip:8086/static`
- **Health Check**: `http://your-ec2-ip:8086/health`

## 💰 Cost Optimization
- **Stop instance when not in use**: Saves ~90%
- **Use Spot Instances**: Save up to 70%
- **Estimated daily cost**: $4-13 depending on usage

## 🔧 Essential Files
- `aws_cloudformation.yaml` - Infrastructure automation
- `deploy_to_aws.sh` - Code deployment
- `upload_models.sh` - Model file upload
- `init_env.sh` - Environment setup
- `start_server.sh` - Application startup
- `requirements.txt` - Python dependencies

## 🆘 Troubleshooting
- **GPU Quota Error**: Request increase in Service Quotas
- **Connection Issues**: Check security group port 8086
- **Model Loading**: Ensure all .bin files are uploaded
- **Performance**: Verify GPU is detected with `nvidia-smi`
