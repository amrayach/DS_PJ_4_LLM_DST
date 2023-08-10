import torch
import pickle
import json
import pandas as pd
import numpy as np
import os


file_path = "./data/extracted/test_examples.pkl"
with open(file_path, 'rb') as file:
    data = pickle.load(file)

file_path =  "./out/generated/adapter/generated.json"
with open(file_path, "r") as file:
    generated = file.read()
generated = json.loads(generated)

new_dict = dict()
index = 0
for entry in generated:
    new_dict[list(entry.keys())[0]] = entry[list(entry.keys())[0]]
    new_dict[list(entry.keys())[0]]["example_id"] = data[index]["example_id"]
    index+=1
    
file_path = './out/generated/adapter/preds.json'
directory = os.path.dirname(file_path)
os.makedirs(directory, exist_ok=True)
with open(file_path, 'w') as file:
     json.dump(new_dict, file, indent=4)

## checking
#file_path = 'preds.json'
#with open(file_path, "r") as file:
#    preds = file.read()
#preds = json.loads(preds)
#
#print("Keys look like this:",list(preds.keys())[:10])
#print()
#print("First entry looks like this:")
#print(preds["0"])
#print()