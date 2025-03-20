from functools import cache


def convert_keys_to_lowercase(input_dict):
    return {key.lower(): value for key, value in input_dict.items()}

def match_in_keys(dictionary, search_string):
    lowercase_dict = convert_keys_to_lowercase(dictionary)
    if search_string.lower() in list(lowercase_dict.keys()):
        return lowercase_dict.get(search_string.lower())
    for l_key in lowercase_dict.keys():
        if l_key.startswith(search_string.lower()):
            return lowercase_dict.get(l_key)

def match_in_values(dictionary, search_string):
    lowercase_dict = convert_keys_to_lowercase(dictionary)
    if search_string.lower() in list(lowercase_dict.values()):
        return search_string