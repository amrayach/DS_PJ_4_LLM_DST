import pickle
import ast

import json

# Read in the predictions of the baseline bert model
# The predictions are generated from the fine-tuned bert model from the evaluation script
# The predictions are in json format and saved as a pickled dictionary
with open('bert_hyp_dataset.pickle', 'rb') as f:
    bert_hyp_dataset = pickle.load(f)


# Read in the predictions of the llm (LLaMA or Falcon) model
# The predictions are generated from the fine-tuned llm model in a separate script
# from Lit-LLaMA or Lit-Parrot
# the predictions are indexed by the dialogue turn id similar to the baseline bert model
# entries looks like this:

# {'input': 'system: \nuser: Hi, could you get me a restaurant booking on the 8th please?',
# 'generated': "Active intent: FindRestaurants\nRequested slots: \nSlot values: {'city': '[CLS]', 'date': '8'}", 'true': "Active intent: ReserveRestaurant\nRequested slots: \nSlot values: {'date': 'the 8th'}",
# 'example_id': 'test-1_00000-00-Restaurants_2'}

with open('parrot_preds.json', "r") as file:
    llama_preds = file.read()

llama_preds = json.loads(llama_preds)


# This part iterates over the keys (ids) and tries to extract the
# random generated response from the llm model
# slot_values, active_intent, requested_slots
# while calculating the number of errors due to formatting issues



# llama errors: out of 46116 entries the following are the number of fault entries
# active_intents: 35 fault entries
# requested_slots: 138 fault entries
# slot_values: 1201 fault entries
# ---------------------------------------
# falcon errors: out of 46116 entries the following are the number of fault entries
# active_intents: 143 fault entries
# requested_slots: 229 fault entries
# slot_values: 1063 fault entries


# each partial entry is extracted seperately and saved in a list


# Active intent

active_intents = []
active_intents_error = []

# iterate over the keys (ids) and extract the active intent
for i in llama_preds.keys():

    # try to extract the active intent
    try:
        # get the current prediction
        curr_pred_no_split = llama_preds[i]['generated']
        # split the prediction by newline
        curr_pred = llama_preds[i]['generated'].split('\n')
        # if the prediction is shorter than 2 lines, then there is an error
        if len(curr_pred) < 2:
            # save the error to count later
            active_intents_error.append(curr_pred[0])
            active_intents.append('')
            continue

        # extract the active intent
        active_intent = curr_pred[0]
        # split the active intent by ":" since the active intent is in the format
        # "Active intent: <intent>"
        active_intents.append(active_intent.split(':')[1].strip())

    except:
        # if there is an error, save the error to count later
        active_intents_error.append(curr_pred[0])
        active_intents.append('')


# Requested slots
requested_slots = []
requested_slots_error = []
# iterate over the keys (ids) and extract the requested slots
for i in llama_preds.keys():
    try:
        # get the current prediction
        curr_pred_no_split = llama_preds[i]['generated']
        # split the prediction by newline but now take the second line
        curr_pred = llama_preds[i]['generated'].split('\n')
        # if the prediction is shorter than 2 lines, then there is an error
        if len(curr_pred) < 2:
            # save the error to count later
            requested_slots_error.append(curr_pred[1])
            requested_slots.append([])
            continue

        # extract the requested slots
        requested_slot = curr_pred[1].split(':')
        # if the requested slot is empty, then there is no requested slot
        if len(requested_slot[1:]) > 1:
            requested_slots_error.append(curr_pred[1])
            requested_slots.append([])
        else:
            # split the requested slot by "," since the requested slot is in the format
            values = requested_slot[1].strip()
            # if the requested slot is empty, then there is no requested slot
            if values == '':
                requested_slots.append([])
            else:
                try:
                    # split the requested slot by "," since the requested slot is in the format
                    # "Requested slots: <slot1>, <slot2>, ..."
                    values = list(map(lambda x: x.strip(), values.split(',')))
                    requested_slots.append(values)
                except:
                    requested_slots.append([])

    except:
        # if there is an error, save the error to count later
        requested_slots_error.append(curr_pred)
        requested_slots.append([])
        pass


# Slot values
slot_values = []
slot_values_error = []
# iterate over the keys (ids) and extract the slot values
for i in llama_preds.keys():
    try:
        # get the current prediction
        curr_pred_no_split = llama_preds[i]['generated']
        # split the prediction by newline but now take the third line
        curr_pred = llama_preds[i]['generated'].split('\n')
        # if the prediction is shorter than 3 lines, then there is an error
        if len(curr_pred) < 3:
            slot_values_error.append(curr_pred[2])
            slot_values.append(ast.literal_eval('{}'))
            continue
        # extract the slot values
        slot_value = ':'.join(curr_pred[2].split(':')[1:]).strip()
        # if the slot value is empty, then there is no slot value
        # save it as an empty dictionary
        if slot_value == '':
            slot_values.append(ast.literal_eval('{}'))
        elif slot_value == '{}':
            slot_values.append(ast.literal_eval('{}'))
        else:
            try:
                # if the slot value is not empty, then try to extract it
                slot_value = slot_value.split("{")[1].split("}")[0]
                # if the slot value is not empty, then try to extract it
                slot_value = "{" + slot_value + "}"
                # save the slot value as a dictionary
                # since the format is "Slot values: {<slot1>: <value1>, <slot2>: <value2>, ...}"
                # use ast to convert the string to a dictionary
                slot_values.append(ast.literal_eval(slot_value))
            except:
                # if there is an error, save the error to count later
                slot_values_error.append(curr_pred[2])
                slot_values.append(ast.literal_eval('{}'))
    except:
        # if there is an error, save the error to count later
        slot_values_error.append(curr_pred)
        slot_values.append(ast.literal_eval('{}'))


# last slot values error check to
# validate that all the slot values are dictionaries
for i in range(len(slot_values)):
    if type(slot_values[i]) != dict:
        slot_values[i] = ast.literal_eval('{}')
        slot_values_error.append('')



pred_index = 0

# iterate over the keys (ids) of the bert hypothesis dataset (baseline)
for i in bert_hyp_dataset.keys():
    # get the current dialogue id, services, and turns
    dia_id = bert_hyp_dataset[i]['dialogue_id']
    dia_services = bert_hyp_dataset[i]['services']
    dia_turn = bert_hyp_dataset[i]['turns']

    # iterate over the turns
    for j in range(len(dia_turn)):
        # if the speaker is the user, then inject the predictions
        if dia_turn[j]['speaker'] == 'USER':
            dia_turn_utt = dia_turn[j]['utterance']
            # iterate over the frames
            for k in dia_turn[j]['frames']:
                # get the current frame
                llm_pred = llama_preds[str(pred_index)]
                llm_usr_utt = llm_pred['input'].split('user: ')[1]

                # test if the user utterances are the same
                #if llm_usr_utt != dia_turn_utt:
                #    except()

                # inject the predictions
                k['state']['active_intent'] = active_intents[pred_index]
                k['state']['requested_slots'] = requested_slots[pred_index]
                k['state']['slot_values'] = slot_values[pred_index]

                # increment the prediction index
                pred_index += 1


# save the bert hypothesis dataset (baseline) with the injected predictions
# to a pickle file
# this file is now semi compatible to be used in google's baseline evaluation script
with open('bert_hyp_dataset_falcon_injected.pickle', 'wb') as f:
    pickle.dump(bert_hyp_dataset, f)

