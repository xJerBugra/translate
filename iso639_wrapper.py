from iso639 import Lang, iter_langs
from regex import R


langs = [lang for lang in iter_langs()]

# iso 1
iso1_code_to_name = {lg.pt1: lg.name for lg in langs}
iso1_name_to_code = {lg.name: lg.pt1 for lg in langs}

# iso 2
iso2b_code_to_name = {lg.pt2b: lg.name for lg in langs}
iso2b_name_to_code = {lg.name: lg.pt2b for lg in langs}
iso2t_code_to_name = {lg.pt2t: lg.name for lg in langs}
iso2t_name_to_code = {lg.name: lg.pt2t for lg in langs}

# iso 3
iso3_code_to_name = {lg.pt3: lg.name for lg in langs}
iso3_name_to_code = {lg.name: lg.pt3 for lg in langs}

# iso 5
iso5_code_to_name = {lg.pt5: lg.name for lg in langs}
iso5_name_to_code = {lg.name: lg.pt5 for lg in langs}

# https://github.com/Helsinki-NLP/Tatoeba-Challenge/blob/master/README.md#in-more-detail
helsinki_precendence = ["iso3", "iso5", "iso1", "iso2t", "iso2b"]

rename_dict = {"Panjabi":  "Punjabi"}

def rename_languages(language):
    if language in rename_dict:
        return rename_dict[language]
    return language
    
def rename_return_value(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, str):
            return rename_languages(result)
        elif isinstance(result, list):
            return [rename_languages(item) for item in result]
        elif isinstance(result, dict):
            return {key: rename_languages(value) for key, value in result.items()}
        else:
            return result
    return wrapper

@rename_return_value
def get_name_from_iso_code(iso_code, precedence=helsinki_precendence):
    for code_type in precedence:
        if code_type == "iso1" and iso_code in iso1_code_to_name.keys():
            return iso1_code_to_name[iso_code]
        elif code_type == "iso2b" and iso_code in iso2b_code_to_name.keys():
            return iso2b_code_to_name[iso_code]
        elif code_type == "iso2t" and iso_code in iso2t_code_to_name.keys():
            return iso2t_code_to_name[iso_code]
        elif code_type == "iso3" and iso_code in iso3_code_to_name.keys():
            return iso3_code_to_name[iso_code]
        elif code_type == "iso5" and iso_code in iso5_code_to_name.keys():
            return iso5_code_to_name[iso_code]