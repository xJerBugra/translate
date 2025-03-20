import pycld2 as cld2
from langdetect import detect

def detect_language(input_text):
    if not input_text:
        return "unknown"
    _, _, details = cld2.detect(input_text)
    detected_langauge = details[0][0].lower()
    if detected_langauge == "unknown":
        language_code = detect(input_text)
        return language_code
    else:
        return detected_langauge