"""
NMT translation service using MarianMT (Helsinki-NLP) Transformer models.
Medical/healthcare-oriented: default to a general model; fine-tuning recommended for domain.
"""
from typing import List, Optional
import os

# Ensure project-local HF cache is set before transformers is imported (see app.py)
if "TRANSFORMERS_CACHE" not in os.environ:
    _pkg_dir = os.path.dirname(os.path.abspath(__file__))
    _cache = os.path.join(_pkg_dir, ".cache", "huggingface")
    os.environ.setdefault("HF_HOME", _cache)
    os.environ.setdefault("TRANSFORMERS_CACHE", os.path.join(_cache, "hub"))

_pipeline = None
_loaded_model_name = None


def _get_pipeline(model_name: str = "Helsinki-NLP/opus-mt-en-de"):
    """Load MarianMT translation pipeline once per model."""
    global _pipeline, _loaded_model_name
    if _pipeline is None or _loaded_model_name != model_name:
        from transformers import pipeline
        _pipeline = pipeline(
            "translation",
            model=model_name,
            device=-1,
        )
        _loaded_model_name = model_name
    return _pipeline


def translate(
    text: str,
    model_name: str = "Helsinki-NLP/opus-mt-en-de",
    max_length: Optional[int] = 512,
    num_beams: int = 4,
) -> str:
    """
    Translate source text using MarianMT.
    Default: English -> German. For medical domain, consider fine-tuned models.
    """
    if not (text and text.strip()):
        return ""
    pipe = _get_pipeline(model_name)
    out = pipe(
        text.strip(),
        max_length=max_length or 512,
        num_beams=num_beams,
        truncation=True,
    )
    if isinstance(out, list) and len(out) > 0:
        result = out[0].get("translation_text", "")
        return result.strip() if result else ""
    return ""


def translate_batch(
    texts: List[str],
    model_name: str = "Helsinki-NLP/opus-mt-en-de",
    max_length: Optional[int] = 512,
    num_beams: int = 4,
) -> List[str]:
    """Translate multiple segments."""
    pipe = _get_pipeline(model_name)
    results = []
    for t in texts:
        if not (t and t.strip()):
            results.append("")
            continue
        out = pipe(
            t.strip(),
            max_length=max_length or 512,
            num_beams=num_beams,
            truncation=True,
        )
        if isinstance(out, list) and out:
            results.append((out[0].get("translation_text") or "").strip())
        else:
            results.append("")
    return results
