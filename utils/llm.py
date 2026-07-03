import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load standard .env file
load_dotenv()

MODEL = "gemini-3.1-flash-lite"   # Gemini Flash Lite


def get_api_key():
    """Retrieve the API key from the environment or return None."""
    return os.getenv("GEMINI_API_KEY")


def configure_genai(api_key: str):
    """Configure the google-generativeai client with the provided API key."""
    if not api_key:
        raise ValueError("Gemini API key is required.")
    genai.configure(api_key=api_key)


def generate_text(prompt: str, api_key: str, system_instruction: str = None) -> str:
    """Return the full response text in one shot."""
    configure_genai(api_key)
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_instruction
    )
    response = model.generate_content(prompt)
    return response.text


def generate_stream(prompt: str, api_key: str, system_instruction: str = None):
    """
    Yield text chunks one at a time (streaming).

    Usage:
        for chunk in generate_stream(prompt, api_key):
            accumulated += chunk
            placeholder.markdown(accumulated + " ▌")
    """
    configure_genai(api_key)
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_instruction
    )
    for chunk in model.generate_content(prompt, stream=True):
        if chunk.text:
            yield chunk.text


def generate_structured(prompt: str, response_schema, api_key: str, system_instruction: str = None):
    """
    Generate structured JSON response.
    response_schema should be a Pydantic model class.
    Returns raw JSON string.
    """
    configure_genai(api_key)
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_instruction
    )
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=response_schema
        )
    )
    return response.text
