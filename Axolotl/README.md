# Axolotl

---

This is a guide on how to reproduce the Falcon 7b & 40B qlora (double quantization) results on the DSTC8 Schema Guided Dialogue dataset.

---

## 1. General Setup:
Initially, the general setup is done by following the instructions in the [README.md](README.md) file in the following the [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) repository.

A HPC server is needed to run the experiments with an equipped A100-80GB GPU. If the available server environment is compatible with docker images then please 
follow the supplied Axolotl setup. 

In our case, we used a server that uses enroot images instead of docker images. Therefore, we had to adjust the setup accordingly.
we started with a **nvidia_cuda_11_8_ubuntu22_04_devlev** docker image from the Docker Hub. Then, we converted it into the correct format for enroot images using the following command:
```bash
srun \
  enroot import \
  -o /netscratch/$USER/nvidia_cuda_11_8_ubuntu22_04_devlev.sqsh \
  docker://nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04
```
This will create a squashfs image in the specified directory. At this point the following command can be used to run the image:

```bash
srun -K --ntasks=1 --gpus-per-task=1 --cpus-per-gpu=6 --mem=128G -p A100-80GB --container-mounts=/netscratch/$USER:/netscratch/$USER,/home/$USER:/home/$USER,/ds:/ds:ro,`pwd`:`pwd`   --container-image=/netscratch/$USER/nvidia_cuda_11_8_ubuntu22_04_devlev.sqsh  --container-workdir=`pwd`   --export="NCCL_SOCKET_IFNAME=bond,NCCL_IB_HCA=mlx5" ./run_qlora.sh
```

The **run_qlora.sh** script will setup the needed dependencies and run the experiments. However, it is important to copy the [config-7b-qlora_amr.yml](config-7b-qlora_amr.yml) and [config-40b-qlora_amr.yml](config-40b-qlora_amr.yml) files into the cloned [examples](https://github.com/OpenAccess-AI-Collective/axolotl/tree/main/examples/falcon) axolotl directory and specify which one is needed in the main starting script.


--- 
