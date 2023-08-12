#!/usr/bin/env bash


apt update && apt upgrade -y
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt install python3.10
apt-get install python3-distutils -y
apt-get install python3-apt -y
apt install python3-pip -y
apt install python3.10-distutils -y
pip3 install -r requirements.txt
pip3 install -q trl
pip3 install deepspeed
pip3 install scipy

CUDA_VISIBLE_DEVICES=0 python3.10 llama_peft.py --max_seq_len 200 --bf16 --group_by_length