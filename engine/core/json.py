import json
import os

def serialize_tuples(input_tuples:tuple):
    return str(input_tuples)

def deserialize_tuples(input_string:str):
    input_string = input_string.removeprefix("("); input_string = input_string.removesuffix(")")
    input_string = input_string.split(", ")
    for i, element in enumerate(input_string):
        input_string[i] = int(element)
    return tuple(input_string)

def serialize_tuples_dictionary_keys(input_dictionary:dict):
    return_dict = {}
    for key in input_dictionary.keys():
        return_dict[serialize_tuples(key)] = input_dictionary[key]
    return return_dict

def deserialize_tuples_dictionary_keys(input_dictionary:dict):
    return_dict = {}
    for key in input_dictionary.keys():
        return_dict[deserialize_tuples(key)] = input_dictionary[key]
    return return_dict 

def serialize_tuples_dictionary_values(input_dictionary:dict):
    return_dict = {}
    for key in input_dictionary.keys():
        return_dict[key] = serialize_tuples(input_dictionary[key])
    return return_dict

def deserialize_tuples_dictionary_values(input_dictionary:dict):
    return_dict = {}
    for key in input_dictionary.keys():
        return_dict[key] = deserialize_tuples(input_dictionary[key])
    return return_dict 

def serialize_tuples_list_elements(input_list:list):
    return_list = []
    for element in input_list:
        return_list.append(list(element))
    return return_list

def deserialize_tuples_list_elements(input_list:list):
    return_list = []
    for element in input_list:
        return_list.append(tuple(element))
    return return_list

def serialize_tuples_set_elements(input_set:set):
    return_list = []
    for element in input_set:
        return_list.append(list(element))
    return return_list

def deserialize_tuples_set_elements(input_list:list):
    return_set = set()
    for element in input_list:
        return_set.add(tuple(element))
    return return_set

def serialize_integer_dictionary_keys(input_dictionary:dict):
    return_dict = {}
    for key in input_dictionary.keys():
        return_dict[str(key)] = input_dictionary[key]
    return return_dict

def deserialize_integer_dictionary_keys(input_dictionary:dict):
    return_dict = {}
    for key in input_dictionary.keys():
        temp_key:str = key
        try:
            temp_key = int(temp_key)
        except:
            temp_key = float(temp_key)
        return_dict[temp_key] = input_dictionary[key]
    return return_dict 

def save_JSON(path:str, data:dict):
    file = open(path, "w")
    json.dump(data, file)
    file.close()

def load_JSON(path:str):
    file = open(path, "r")
    save = json.load(file)
    file.close()
    return save

def get_JSON_file_from_main_directoy():
    for file in os.listdir():
        if file.endswith(".json"):
            return file