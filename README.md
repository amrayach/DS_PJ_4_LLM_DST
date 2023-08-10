# DS_PJ_4_LLM_SGD
---

## Clone this repository 

```bash 
git clone git@github.com:amrayach/DS_PJ_4_LLM_DST.git
cd DS_PJ_4_LLM_DST
```

<!-- Ammer please add the modified script file to extract the datasets -->
# Extract the dataset 

Expected output: all the necessary data structured and contained in: 

  ./data/extracted/train_examples.pkl
  
  ./data/extracted/test_examples.pkl

# pre-process dataset
```bash 
python dst_preprocessing.py
```

Expected output: preprocessed data in the prompt format:

'./data/instruction_based_dst_train.json'

'./data/instruction_based_dst_test.json'



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
cp ../customized/lit-llama/scripts/preprocess_outputs.py ./scripts/
cp ../customized/lit-llama/finetune/adapter.py ./finetune/
cp ../customized/lit-llama/generate/adapter_test.py ./generate/
cp ../customized/lit-llama/install_requirements.sh ./
./install_requirements.sh
```



### Download and prepare LLaMa weights for Lit-LLaMA
Either download the weights by filling this [form](https://forms.gle/jk851eBVbX1m5TAv5) or follow the next steps (based on https://github.com/juncongmoo/pyllama):	

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

#### Finetune LLaMa using Adapter. 
If you want to continue training from a checkpoint, the checkpoint path can be entered in the script (adapter_checkpoint = torch.load())
```bash 
python finetune/adapter.py --data_dir data/dst/ --out_dir out/dst/adapter
```


#### Generate predictions on the test set: 
The checkpoint can be changed in the script (adapter_path: Path = Path("out/dst/adapter/lit-llama-lora-finetuned.pth"))
```bash 
python generate/adapter_test.py 
```

#### Preprocessing steps for the generated output to prepare it for the evaluation script
```bash 
python scripts/preprocess_outputs.py 
```

#### Setting up Lit-Parrot 
Note: Lit-Parrot has been renamed to lit-gpt
```bash 
# Please make sure you are in the main folder (DS_PJ_4_LLM_DST/.)
git clone https://github.com/Lightning-AI/lit-gpt.git
cd lit-gpt
git checkout 93b3f6f527
```


#### Copy customized implementations
```bash 
cp ../customized/lit-parrot/scripts/prepare_dst.py ./scripts/
cp ../customized/lit-parrot/scripts/preprocess_outputs.py ./scripts/
cp ../customized/lit-parrot/finetune/adapter.py ./finetune/
cp ../customized/lit-parrot/generate/adapter_test.py ./generate/
cp ../customized/lit-parrot/install_requirements.sh ./
./install_requirements.sh
```


Download and prepare Falcon weights for Lit-Parrot
```bash 
python scripts/download.py --repo_id tiiuae/falcon-7b-instruct
python scripts/convert_hf_checkpoint.py --checkpoint_dir checkpoints/tiiuae/falcon-7b-instruct
```


#### Preprocess the dataset for Lit-Parrot
```bash 
python scripts/prepare_dst.py --destination_path data/dst/train   --checkpoint_dir checkpoints/tiiuae/falcon-7b-instruct
```

#### Finetune LLaMa using Adapter. 
If you want to continue training from a checkpoint, the checkpoint can be entered in the script (adapter_checkpoint = torch.load())
```bash 
python finetune/adapter.py --data_dir data/dst/ --out_dir out/dst/adapter
```


#### Generate predictions on the test set: 
The checkpoint can be changed in the script (adapter_path: Path = Path("out/dst/adapter/lit-llama-lora-finetuned.pth"))
```bash 
python generate/adapter_test.py 
```

#### Preprocessing steps for the generated output to prepare it for the evaluation script
```bash 
python scripts/preprocess_outputs.py
```

#### Textual results to structured results 

#### Evaluation

---
For any inquiries or questions, please do not hesitate to contact the authors or create an issue.
