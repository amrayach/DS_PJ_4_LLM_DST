# Data Utils

---

## Description

This Section describes all process related to data manipulation and data processing related to the DST project. 
Most of the code is based upon the [google-research/schema_guided_dst/](https://github.com/google-research/google-research/tree/master/schema_guided_dst) repository. Furthermore, the section
also includes code for pre- / post- processing as well as evaluation of the DST models.

---

### 1. Generate Data for LLM's (LLaMa & Falcon):

1. Clone the [google-research/schema_guided_dst/](https://github.com/google-research/google-research/tree/master/schema_guided_dst) repository from the main 
    [google-research](https://github.com/google-research/google-research/tree/master) following the instructions in the README.md

2. Follow the instructions in the [google-research/schema_guided_dst/README.md](https://github.com/google-research/google-research/tree/master/schema_guided_dst#baseline-model-and-evaluation-script-for-dstc8-schema-guided-dialogue-state-tracking), such as
setting up a virtual environment, installing dependencies, and downloading the initial BERT checkpoint.
3. Replace the original cloned **baseline** directory with the one [baseline](baseline) provided in this repository. 
this directory contains adjusted code for the data generation process. Especially, the [data_utils.py](baseline/data_utils.py).
4. run the following command to generate the data for LLaMa:
    ```bash
    CUDA_VISIBLE_DEVICES=0 python -m schema_guided_dst.baseline.train_and_predict --bert_ckpt_dir ./schema_guided_dst/cased_L-12_H-768_A-12 \
   --dstc8_data_dir ./DS_PJ_4/dstc8-schema-guided-dialogue-master/ \
   --dialogues_example_dir ./schema_guided_dst/dialouges_example_output/ \
   --schema_embedding_dir ./schema_guided_dst/schema_embed_output/ \
   --output_dir ./schema_guided_dst/ft_model/ \
   --dataset_split train --run_mode train --task_name dstc8_all
    ```
  **NOTE 1:** All directories in the command should be previously created. 
  
  **NOTE 2:** The parameter **--dataset_split** can be either **train**, **dev**, or **test** and accordingly the textual output will be.
   
  **NOTE 2:**: Finally, the textual data will be generated as a pickle file. 

---

### 2. Preprocess the generated data:
Once the data is generated from the previous step as a json file, use the following script to get the data into the (prompt, input, output) format.
Use the [preprocess_outputs.py](..%2Fcustomized%2Flit-llama%2Fscripts%2Fpreprocess_outputs.py) 


---

### 3. Postprocess the generated data:

This part is responsible for converting the free textual predictions of the fine-tuned models to the required format for the google evaluation script.

Since the generated data from step one are sorted iteratively by id, the postprocessing script is capable to take in the predictions of the fine-tuned models as a json file and the 
extracted format complaint BERT prediction (which work with googles evaluation script) and inject/replace them to generate a new pickle file that
contains the llm's predictions in the required format instead of Bert's.

In the supplied zipped [post_process_data_bundle.zip](PostProcessing%2Fpost_process_data_bundle.zip) following files are included:
- bert_hyp_dataset.pickle: The extracted format complaint BERT prediction (which work with googles evaluation script)
- llama_preds.json: The predictions of the fine-tuned LLaMa model as a json file.
- parrot_preds.json: The predictions of the fine-tuned Falcon model as a json file.
- bert_hyp_dataset_llama_injected.pickle: The injected LLaMa predictions in the required format instead of Bert's.
- bert_hyp_dataset_falcon_injected.pickle: The injected Falcon predictions in the required format instead of Bert's.

However, to generate the injected predictions, the following command should be executed:
```bash
python post_process_data.py 
```
Please change the variables in the script according to your needs. Since they are hardcoded for now. 

The [post_process_data.py](PostProcessing%2Fpost_process_data.py) script mechanism is to extract the relevant dialogue state attributes from the predictions as follows:
- Active Intent --> String 
- Requested Slots --> List of Strings
- Slot Values --> Nested dictionary of Strings

Then, the script will inject the extracted values to the relevant dialogue state attributes in the original pickle file.

---

### 4. Evaluation of the fine-tuned models:

This is the final step in the data utils section. It is responsible for evaluating the fine-tuned models using the google evaluation script.

Similar to the first step, the general directory should be setup and working with all the relevant subdirectories and files. Then the scripts in the [Evaluation](Evaluation) folder
should be replaced with their counterparts since they are adjusted to deal with the generated pickle files from the previous steps.

After that, the following command should be executed:
```bash
CUDA_VISIBLE_DEVICES=0 python -m schema_guided_dst.evaluate --dstc8_data_dir ./schema_guided_dst/dstc8-schema-guided-dialogue/ \
--prediction_dir ./schema_guided_dst/ft_model/pred_res_103000_test_dstc8_all_/ \
--eval_set test \
--output_metric_file ./schema_guided_dst/output_metric_results/test_res.json
```
**NOTE:** Please adjust the variables in the script according to your needs. Since they are hardcoded for now.

After running the evaluation script, the results will be saved in the output_metric_file as a json file.

The metric results for our project are saved in the [Evaluation](Evaluation) folder as well. 

Or you can check them out in the [Metric evaluation.xlsx](Evaluation%2FMetric%20evaluation.xlsx) excel file, neatly visualized.

---


