import os
import openai
import httpx
import google.generativeai as genai


def load_model(name, API_BASE="Default", API_KEY="Default", organization=False):
    client = None
    if "gpt" in name:
        API_BASE = "https://api.openai.com/v1" if API_BASE == "Default" else API_BASE
        API_KEY = os.getenv("OPENAI_API_KEY") if API_KEY == "Default" else API_KEY
        if organization:
            client = openai.OpenAI(
                base_url=API_BASE,
                api_key=API_KEY,
                organization=os.getenv("OPENAI_ORG_KEY"),
                timeout=httpx.Timeout(300.0, read=20.0, write=20.0, connect=10.0),
            )
        else:
            client = openai.OpenAI(
                base_url=API_BASE,
                api_key=API_KEY,
                timeout=httpx.Timeout(3000.0, read=20.0, write=20.0, connect=10.0),
            )
    elif "gemini" in name:
        API_KEY = os.getenv("GOOGLE_API") if API_KEY == "Default" else API_KEY
        genai.configure(api_key=API_KEY)
        generation_config = {
            "temperature": 0,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
            }
        thresh = "BLOCK_MEDIUM_AND_ABOVE"
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": thresh
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": thresh
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": thresh
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": thresh
            },
        ]
        client = genai.GenerativeModel(
            model_name=name,
            generation_config=generation_config,
            safety_settings=safety_settings,
        )
    elif "llama" in name.lower() or "mixtral" in name.lower():
        # Assume you use OpenAI wrapper for Llama and Mixtral
        client = openai.OpenAI(
            base_url=API_BASE,
            api_key=API_KEY,
            timeout=httpx.Timeout(3000.0),
        )
    return client

