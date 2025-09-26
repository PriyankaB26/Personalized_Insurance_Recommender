import google.generativeai as genai

genai.configure(api_key="AIzaSyCWibAn4KWZNFPFisCK2KJ9B5d6dh1TR_o")
models = list(genai.list_models())  # convert generator to list
for model in models:
    print(model)