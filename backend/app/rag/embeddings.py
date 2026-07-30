import httpx

from app.core.config import get_settings


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    return _embed(texts)


def embed_query(text: str) -> list[float]:
    vectors = _embed([text])
    if not vectors:
        raise RuntimeError("Ollama returned no embedding for the query.")
    return vectors[0]


def _embed(inputs: list[str]) -> list[list[float]]:
    settings = get_settings()
    payload = {
        "model": settings.ollama_embed_model,
        "input": inputs,
    }

    try:
        response = httpx.post(
            f"{settings.ollama_base_url}/api/embed",
            json=payload,
            timeout=settings.ollama_timeout_seconds,
        )
    except httpx.HTTPError as exc:
        raise RuntimeError(
            "Could not reach Ollama at the configured base URL. "
            "Make sure Ollama is running locally."
        ) from exc

    data = _parse_json_response(response)
    embeddings = data.get("embeddings")
    if not isinstance(embeddings, list) or not embeddings:
        raise RuntimeError("Ollama returned an invalid embeddings response.")

    return embeddings


def _parse_json_response(response: httpx.Response) -> dict:
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError("Ollama returned a non-JSON response.") from exc

    if response.is_error:
        message = data.get("error") if isinstance(data, dict) else None
        raise RuntimeError(message or f"Ollama request failed with status {response.status_code}.")

    if not isinstance(data, dict):
        raise RuntimeError("Ollama returned an unexpected response format.")

    return data
