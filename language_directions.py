from helsinki_models import helsinki_models, get_clearly_formatted_langauge_directions
from iso639_wrapper import get_name_from_iso_code
from language_detection import detect_language
from collections import OrderedDict
from utils import convert_keys_to_lowercase, match_in_keys, match_in_values


def get_all_source_languages():
    """
    Returns a human-readable `dict source_languages_names:codes` 
    based on the available models.
    """
    source_languages = {}
    language_directions = get_clearly_formatted_langauge_directions()

    for direction in language_directions:
        source_lang_code = direction.split('-')[0]
        source_language_name = get_name_from_iso_code(source_lang_code)
        if source_language_name:
            source_languages[source_language_name] = source_lang_code
    source_languages = OrderedDict(sorted(source_languages.items()))
    all_source_langs_including_auto_detect = \
        { **{'Auto Detect' : 'Auto Detect'}, **source_languages}
    return all_source_langs_including_auto_detect

def update_source_languages_dict(source_languages_dict, auto_detected_language):
    source_languages_dict[auto_detected_language] = "Auto Detect"

def get_target_languages(source_language_code, input_text=None):
    """
    Returns a human-readable `dict of target languages names to codes` 
    based on the available models and the source language passed.
    """
    include_all_languages = False
    if source_language_code == "Auto Detect":
        source_language_code, include_all_languages = auto_detect_language_code(input_text)
        
    target_languages = {}
    language_directions = get_clearly_formatted_langauge_directions()
    for direction in language_directions:
        if direction.startswith(f"{source_language_code}-") or include_all_languages:
            target_language = direction.split('-')[1]  # Extracting the last part as the target language
            target_language_name = get_name_from_iso_code(target_language)
            if target_language_name:
                target_languages[target_language_name] = target_language
    return OrderedDict(sorted(target_languages.items())), source_language_code

def auto_detect_language_code(input_text):
    DEFAULT_SOURCE_LANGUAGE = "en"
    detected_language_string = DEFAULT_SOURCE_LANGUAGE
    if not input_text:
        return DEFAULT_SOURCE_LANGUAGE, True
    language_or_code = detect_language(input_text)
    if language_or_code == "unknown":
        return DEFAULT_SOURCE_LANGUAGE, True
    else:
        detected_language_string = match_in_keys(get_all_source_languages(), language_or_code)
        if not detected_language_string:
            detected_language_string = match_in_values(get_all_source_languages(), language_or_code)
        if detected_language_string:
            return detected_language_string, False
        else:
            return DEFAULT_SOURCE_LANGUAGE, True
    

# Example usage:
# all_source_languages = get_all_source_languages()
# print("All Source Languages:", all_source_languages)

# source_language_code = "pa"  # Replace with your desired source language
# target_languages = get_target_languages(source_language_code)
# print(f"Target Languages for {source_language_code}:", target_languages)
