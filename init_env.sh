#!/bin/bash
# Check if conda environment exists
ENVIRONMENT_NAME="AuPC38"
source .bashrc
if ! conda env list | grep -q "^$ENVIRONMENT_NAME "; then
    echo "Environment $ENVIRONMENT_NAME does not exist, creating..."
    conda create --name $ENVIRONMENT_NAME python=3.8.10
    echo "Environment $ENVIRONMENT_NAME created successfully."
else
    echo "Environment $ENVIRONMENT_NAME already exists."
fi
conda activate AuPC38
conda install paddlepaddle-gpu==2.4.2 cudatoolkit=11.7 -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/ -c conda-forge
pip install -r requirements.txt