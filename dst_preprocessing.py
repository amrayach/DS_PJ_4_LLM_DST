import pickle
import json

train_file_path = "./data/extracted/train_examples.pkl"
test_file_path = "./data/extracted/test_examples.pkl"

with open(train_file_path, 'rb') as file:
    train_data = pickle.load(file)
with open(test_file_path, 'rb') as file:
    test_data = pickle.load(file)

instruction = "For the following dialogue extract the current state (i.e. Active intent, Requested slots, and Slot values):"

def preprocess(data, train = True):
    new_data = dict()
    for i in range(len(data)):

        new_data[i] = dict()
        input = ""
        input += data[i]["system_utterance"]
        input += "\n"
        input += data[i]["user_utterance"]

        output = ""
        output += "Service name: " + data[i]["service_name"] + "\n"
        output += "Active intent: " + data[i]["active_intent"] + "\n"
        output += "Requested slots: " + ", ".join(data[i]["requested_slots"]) + "\n"
        output += "Slot values: " + str(data[i]["slot_values_in_state"]) + ""

        new_data[i]["input"]=input
        new_data[i]["output"]=output


    l = list()
    for i in range(len(data)):
        entry = dict()
        entry["instruction"] = instruction
        entry["input"] = new_data[i]["input"]
        entry["output"] = new_data[i]["output"]    
        l.append(entry)

    if train==True:
        file_path = './data/instruction_based_dst_train.json'
    else: 
        file_path = './data/instruction_based_dst_test.json'

    with open(file_path, 'w') as file:
         json.dump(l, file, indent=4)
            
preprocess(train_data, train = True)
preprocess(test_data, train = False)