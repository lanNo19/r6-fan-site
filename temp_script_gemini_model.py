import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get LLM API key from environment variables
LLM_API_KEY = os.getenv('LLM_API_KEY')

if not LLM_API_KEY:
    print("Error: LLM_API_KEY environment variable not set in .env file.")
    exit()

try:
    genai.configure(api_key=LLM_API_KEY)
    print("Gemini API configured. Listing available models...\n")

    found_text_model = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
            print(f"  Description: {m.description}")
            print(f"  Supported Methods: {m.supported_generation_methods}\n")
            found_text_model = True

    if not found_text_model:
        print("No models found that support 'generateContent'.")
    else:
        print("\nLook for a model name that is suitable for text generation (e.g., 'gemini-pro' or 'models/gemini-pro')")
        print("If 'gemini-pro' isn't listed or doesn't support generateContent, choose another suitable model.")

except Exception as e:
    print(f"An error occurred while listing models: {e}")
    print("Please ensure your LLM_API_KEY is correct and has the necessary permissions.")

