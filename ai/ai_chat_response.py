# ai/ai_chat_response.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ai_response(prompt: str) -> str:
    """
    Sends a prompt to OpenRouter and returns the AI response.
    Tries multiple models for reliability.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "⚠️ Missing API key. Please check your .env file."

    # List of fallback models
    models = [
        "mistralai/mistral-7b-instruct",
        "openai/gpt-4-turbo",  # If access is available
        "anthropic/claude-3-haiku"
    ]

    for model in models:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost"  # Replace with your domain if deployed
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                },
                timeout=10
            )

            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        except requests.exceptions.HTTPError as http_err:
            print(f"[AI ERROR] {model} => HTTP {http_err.response.status_code}")
        except Exception as e:
            print(f"[AI ERROR] {model} => {str(e)}")

    return "⚠️ All AI models failed. Please try again later."
