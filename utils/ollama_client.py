"""
utils/ollama_client.py
Helpers for talking to a local Ollama server.

Model: qwen3.5:4b
"""

from ollama import chat

MODEL = "qwen2.5:3b"


def generate_response(prompt: str) -> str:
    """
    Return the full response text in one shot (no streaming).
    Useful for the evaluator / final-answer step.
    """
    response = chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    return response.message.content


def generate_stream(prompt: str):
    """
    Yield content chunks one at a time.
    Caller should iterate and push each chunk to the UI.

    Usage:
        for chunk in generate_stream(prompt):
            accumulated += chunk
            placeholder.markdown(accumulated + "▌")
    """
    stream = chat(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        token = chunk.message.content
        if token:
            yield token
