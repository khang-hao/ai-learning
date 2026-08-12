from functools import lru_cache
from io import BytesIO

import numpy as np
from PIL import Image, ImageOps
from rapidocr import RapidOCR

from app.core.config import get_settings


@lru_cache
def _load_ocr_engine() -> RapidOCR:
    return RapidOCR()


def extract_text_from_image_bytes(content: bytes) -> str:
    settings = get_settings()
    image_array = _load_image_array(content)
    result = _load_ocr_engine()(image_array)

    boxes, txts, scores = _extract_result_parts(result)

    if not txts:
        raise ValueError("No readable text was found in the image.")

    entries: list[tuple[float, float, str]] = []
    for index, text in enumerate(txts):
        cleaned = str(text).strip()
        if not cleaned:
            continue

        score = _coerce_score(scores[index]) if index < len(scores) else 1.0
        if score < settings.ocr_min_score:
            continue

        y_pos, x_pos = _get_sort_position(boxes[index]) if index < len(boxes) else (float(index), 0.0)
        entries.append((y_pos, x_pos, cleaned))

    if not entries:
        raise ValueError("OCR found text, but confidence was too low to keep useful content.")

    entries.sort(key=lambda item: (round(item[0] / 10), item[1]))
    lines = [text for _, _, text in entries]
    joined = "\n".join(lines).strip()

    if len(joined) < 20:
        raise ValueError("The image did not contain enough readable text for study use.")

    return joined


def _load_image_array(content: bytes) -> np.ndarray:
    with Image.open(BytesIO(content)) as image:
        normalized = ImageOps.exif_transpose(image).convert("RGB")
        return np.array(normalized)


def _extract_result_parts(result: object) -> tuple[list[object], list[object], list[object]]:
    if isinstance(result, (list, tuple)) and len(result) >= 3:
        return (
            _to_list(result[0]),
            _to_list(result[1]),
            _to_list(result[2]),
        )

    return (
        _to_list(getattr(result, "boxes", [])),
        _to_list(getattr(result, "txts", [])),
        _to_list(getattr(result, "scores", [])),
    )


def _to_list(value: object) -> list[object]:
    if value is None:
        return []
    if isinstance(value, np.ndarray):
        return list(value.tolist())
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


def _coerce_score(value: object) -> float:
    if value is None:
        return 1.0

    if isinstance(value, np.ndarray):
        if value.size == 0:
            return 1.0
        flattened = value.astype(float).reshape(-1)
        return float(flattened[0])

    if isinstance(value, (list, tuple)):
        if not value:
            return 1.0
        return _coerce_score(value[0])

    return float(value)


def _get_sort_position(box: object) -> tuple[float, float]:
    if box is None:
        return 0.0, 0.0

    try:
        points = np.asarray(box, dtype=float)
    except Exception:
        return 0.0, 0.0

    if points.size == 0:
        return 0.0, 0.0

    ys = points[:, 1]
    xs = points[:, 0]
    return float(np.mean(ys)), float(np.min(xs))
