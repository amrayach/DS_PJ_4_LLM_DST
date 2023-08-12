#!/usr/bin/env bash

apt update && apt upgrade -y
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt install python3.10
apt-get install python3-distutils -y
apt-get install python3-apt -y
apt install python3-pip -y
apt install python3.10-distutils -y


pip install torch

pip3 install -e .
pip3 install -U git+https://github.com/huggingface/peft.git

accelerate config

accelerate launch scripts/finetune.py examples/falcon/config-7b-qlora_amr.yml 