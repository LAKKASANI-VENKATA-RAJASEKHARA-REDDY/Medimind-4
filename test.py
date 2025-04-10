import google.generativeai as genai

# Configure API Key
genai.configure(api_key="AIzaSyCXWcN9zWhx7qYARfieyryTzPgMygYVKlk")

# Get the list of available Gemini models
def list_gemini_models():
    try:
        models = genai.list_models()
        model_names = [model.name for model in models]
        return model_names
    except Exception as e:
        return str(e)

# Print available models
print(list_gemini_models())
