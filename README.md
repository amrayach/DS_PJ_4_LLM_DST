# DS_PJ_4_LLM_SGD


---

## Setting up Lit-LLaMa

```bash 
git clone https://github.com/Lightning-AI/lit-llama
cd lit-llama
```


### Use same version for reproducibility

```bash 
git checkout 26f33a3b95 
```


### Copy customized implementations

```bash 
cp ../customized/lit-llama/scripts/prepare_dst.py ./scripts/
cp ../customized/lit-llama/finetune/adapter_ckpt.py ./finetune/
cp ../customized/lit-llama/generate/adapter.py ./generate/
cp ../customized/lit-llama/install_requirements.sh ./
./install_requirements.sh
```



### Download and prepare LLaMa weights for Lit-LLaMA
Either download the weights by filling this [form](https://forms.gle/jk851eBVbX1m5TAv5) or follow the next steps:	

```bash 

pip install pyllama -U
pip install transformers
python -m llama.download --model_size 7B
```

**NOTE:** Sometimes the download gets stuck so just ctrl-c and run the command again it will continue from the checkpoint

```bash 
mv pyllama_data llama
mkdir checkpoints
mv llama checkpoints
```

Once downloaded, you should have a folder called **checkpoints/llama** containing the weights.

#### Convert the weights to the Lit-LLaMA format:
```bash 
python scripts/convert_checkpoint.py --model_size 7B
```

#### Preprocess the dataset for Lit-LLama
```bash 
python scripts/prepare_dst.py --destination_path data/dst/train
```

#### Finetune LLaMa using Lora  
```bash 
python finetune/lora.py --data_dir data/dst/ --out_dir out/dst/lora
```

#### Finetune LLaMa using Adapter. If you want to continue training from a checkpoint, the checkpoint needs to be entered in the script (adapter_checkpoint = torch.load())
```bash 
python finetune/adapter.py --data_dir data/dst/ --out_dir out/dst/adapter
```


#### Generate predictions on the test set: # (checkpoint can be changed in the script (adapter_path: Path = Path("out/dst/adapter/lit-llama-lora-finetuned.pth")
```bash 
python generate/adapter_test.py 
```

#### Preprocessing steps for the generated output to prepare it for the evaluation script
```bash 
python scripts/preprocess_outputs.py 
```

#### Setting up Lit-Parrot # Note: it has been renamed to lit-gpt
```bash 
git clone https://github.com/Lightning-AI/lit-gpt.git
cd lit-gpt
git checkout 93b3f6f527
```


#### Copy customized implementations
```bash 
cp ../customized/lit-parrot/scripts/prepare_dst.py ./scripts/
cp ../customized/lit-parrot/finetune/adapter_ckpt.py ./finetune/
cp ../customized/lit-parrot/generate/adapter.py ./generate/
cp ../customized/lit-parrot/install_requirements.sh ./

pip install -r requirements.txt

python scripts/download.py --repo_id tiiuae/falcon-7b-instruct
python scripts/convert_hf_checkpoint.py --checkpoint_dir checkpoints/tiiuae/falcon-7b-instruct
```
#### Preprocess the dataset for Lit-Parrot
```bash 
python scripts/prepare_dst.py --destination_path data/dst/train   --checkpoint_dir checkpoints/tiiuae/falcon-7b-instruct
```

#### Finetune LLaMa using Adapter. If you want to continue training from a checkpoint, the checkpoint needs to be entered in the script (adapter_checkpoint = torch.load())
```bash 
python finetune/adapter.py --data_dir data/dst/ --out_dir out/dst/adapter
```


#### Generate predictions on the test set: # (checkpoint can be changed in the script (adapter_path: Path = Path("out/dst/adapter/lit-llama-lora-finetuned.pth")
```bash 
python generate/adapter_test.py 
```

#### Preprocessing steps for the generated output to prepare it for the evaluation script
```bash 
python scripts/preprocess_outputs.py
```