# from responses import start
import gradio as gr
from language_directions import *
from transformers import pipeline
from examples import example_sentences

source_lang_dict = get_all_source_languages()
target_lang_dict = {}
source_languages = source_lang_dict.keys()

def get_auto_detect_source_dropdown(input_text):
    source, _ = auto_detect_language_code(input_text)
    language_name = get_name_from_iso_code(source)
    source_dropdown_text = "Detected - " + language_name
    update_source_languages_dict(source_lang_dict, source_dropdown_text)
    source_language_dropdown = gr.Dropdown(choices=source_languages,
                                                  value=source_dropdown_text,
                                                  label="Source Language")
    return source_language_dropdown, language_name
  
def get_target_dropdown(source_language_name, input_text):
    global target_lang_dict
    target_lang_dict, source_language = get_target_languages(source_lang_dict[source_language_name], input_text)
    target_languages = list(target_lang_dict.keys())
    default_target_value = None
    if "English" in target_languages or "english" in target_languages:
        default_target_value = "English"
    else:
        default_target_value = target_languages[0]
    target_dropdown = gr.Dropdown(choices=target_languages, 
                                  value=default_target_value,
                                  label="Target Language")
    return target_dropdown
  
def get_dropdown_value(dropdown):
    if isinstance(dropdown, gr.Dropdown):
        dropdown_value = dropdown.constructor_args.get('value')
    elif isinstance(dropdown, str):
      dropdown_value = dropdown
    return dropdown_value
  
def get_dropdowns(source_dropdown, input_text):
    source_language_name = get_dropdown_value(source_dropdown)
    if input_text and source_language_name == "Auto Detect" or source_language_name.startswith("Detected"):
      source_dropdown, source_language_name = get_auto_detect_source_dropdown(input_text)
    target_dropdown = get_target_dropdown(source_language_name=source_language_name,
                                          input_text=input_text)
    return source_dropdown, target_dropdown

def input_changed(source_language_dropdown, input_text=""):
    return get_dropdowns(source_dropdown=source_language_dropdown,
                         input_text=input_text)

def translate(input_text, source, target):
    source_readable = source
    if source == "Auto Detect" or source.startswith("Detected"):
      source, _ = auto_detect_language_code(input_text)
    if source in source_lang_dict.keys():
      source = source_lang_dict[source]
    target_lang_dict, _ = get_target_languages(source)
    try:
      target = target_lang_dict[target]
      model = f"Helsinki-NLP/opus-mt-{source}-{target}"
      pipe = pipeline("translation", model=model)
      translation = pipe(input_text)
      return translation[0]['translation_text'], ""
    except KeyError:
      return "", f"Error: Translation direction {source_readable} to {target} is not supported by Helsinki Translation Models"


with gr.Blocks() as demo:
    gr.HTML("""<html>
  <head>
    <style>
      h1 {
        text-align: center;
      }
    </style>
  </head>
  <body>
    <h1>Open Translate</h1>
  </body>
</html>""")
    with gr.Row():
        with gr.Column():
            source_language_dropdown = gr.Dropdown(choices=source_languages,
                                                   value="Auto Detect",
                                                  label="Source Language")
            input_textbox = gr.Textbox(lines=5, placeholder="Enter text to translate", label="Input Text")
        with gr.Column():
            target_language_dropdown = gr.Dropdown(choices=["English", "French", "Spanish"],
                                                   value="English",
                                                   label="Target Language")
            translated_textbox = gr.Textbox(lines=5, placeholder="", label="Translated Text")
    info_label = gr.HTML("")
    btn = gr.Button("Translate")
    source_language_dropdown.change(input_changed, inputs=[source_language_dropdown, input_textbox], outputs=[source_language_dropdown, target_language_dropdown])
    input_textbox.change(input_changed, inputs=[source_language_dropdown, input_textbox], outputs=[source_language_dropdown, target_language_dropdown])
    btn.click(translate, inputs=[input_textbox,
                                 source_language_dropdown,
                                 target_language_dropdown],
                                   outputs=[translated_textbox, info_label])
    gr.Examples(example_sentences, inputs=[input_textbox])

if __name__ == "__main__":
    demo.launch()