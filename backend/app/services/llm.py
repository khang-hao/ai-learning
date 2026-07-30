import httpx

from app.core.config import get_settings


def generate_grounded_response(system_prompt: str, user_prompt: str) -> str:
    settings = get_settings()
    payload = {
        "model": settings.ollama_chat_model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }

    try:
        response = httpx.post(
            f"{settings.ollama_base_url}/api/chat",
            json=payload,
            timeout=settings.ollama_timeout_seconds,
        )
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Could not reach Ollama at the configured base URL. "
            "Make sure Ollama is installed and running."
        ) from exc

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Ollama returned a non-JSON response.") from exc

    if response.is_error:
        message = data.get("error") if isinstance(data, dict) else None
        raise RuntimeError(message or f"Ollama request failed with status {response.status_code}.")

    if not isinstance(data, dict):
        raise RuntimeError("Ollama returned an unexpected response format.")

    message = data.get("message")
    if not isinstance(message, dict):
        raise RuntimeError("Ollama response did not include a message object.")

    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("The model returned an empty response.")

    return content.strip()
