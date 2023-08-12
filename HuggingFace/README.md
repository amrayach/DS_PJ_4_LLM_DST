# LLaMa PEFT Fine-Tuning

---

Similar to the environment setup in [README.md](..%2FAxolotl%2FREADME.md), the steps should be followed to get the right enroot/docker image and prepare the dependencies.

After that please add your API tokens or comment out the lines (136 & 138) for weights & biases and huggingface hub. 

Finally, run the following command to start the fine-tuning process:

```bash
srun -K --ntasks=1 --gpus-per-task=1 --cpus-per-gpu=6 --mem=128G -p A100-80GB --container-mounts=/netscratch/$USER:/netscratch/$USER,/home/$USER:/home/$USER,/ds:/ds:ro,`pwd`:`pwd`   --container-image=/netscratch/$USER/nvidia_cuda_11_8_ubuntu22_04_devlev.sqsh  --container-workdir=`pwd`   --export="NCCL_SOCKET_IFNAME=bond,NCCL_IB_HCA=mlx5" ./amr_setup.sh
```

This should take the image, install python / pip, and install the needed requirements. After that, the fine-tuning process will start.

---

