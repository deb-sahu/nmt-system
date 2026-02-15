# Code Documentation — NMT Application

## Overview

This document describes the structure, frameworks, and design of the Neural Machine Translation (NMT) application with BLEU evaluation.

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|--------|
| **Language** | Python 3.8+ | Core implementation |
| **NMT framework** | Hugging Face `transformers` | Model loading and inference |
| **NMT models** | MarianMT (Helsinki-NLP) | Transformer-based translation (e.g. `opus-mt-en-de`) |
| **Frontend** | Streamlit | Web UI (inputs, file upload, results) |
| **BLEU** | Custom implementation | Modified n-gram precision, brevity penalty, no external BLEU library |

---

## Project Structure

```
nlpa2/
├── app.py                      # Streamlit frontend and evaluation flow
├── nmt_service.py              # NMT translation (MarianMT)
├── bleu_utils.py               # BLEU computation and n-gram table
├── requirements.txt            # Python dependencies
├── README.md                   # Run instructions and overview
├── DOCUMENTATION.md            # This file — code and architecture
├── REPORT.md                   # Design choices, challenges, integration report
├── Quality_Improvement_Strategy.md   # Task B (submit as PDF)
└── screenshots/                 # (Optional) Place screenshots here for report
```

---

## Module Descriptions

### 1. `app.py` (Frontend)

- **Purpose:** Single-page Streamlit UI for source input, reference input (paste/upload), translation trigger, and BLEU results.
- **Key elements:**
  - **Sidebar:** Model selection (MarianMT variant), beam size.
  - **Main area:** Source text area → Translate button; reference (paste or file upload); NMT output display; optional extra candidates (one per line); BLEU section with expandable per-candidate results (score, brevity penalty, n-gram table).
- **Libraries:** `streamlit` for UI; `bleu_utils` for tokenization and BLEU; `nmt_service` for `translate()`.

### 2. `nmt_service.py` (NMT Backend)

- **Purpose:** Load and run MarianMT translation via Hugging Face `pipeline("translation", model=...)`.
- **Functions:**
  - `_get_pipeline(model_name)`: Lazy-loads one pipeline per model; avoids reloading when the same model is used.
  - `translate(text, model_name, max_length, num_beams)`: Translates a single string; returns translated string.
  - `translate_batch(texts, ...)`: Translates a list of strings (e.g. for batch evaluation).
- **Design:** Pipeline is cached globally per `model_name` to reduce repeated model loads.

### 3. `bleu_utils.py` (Evaluation)

- **Purpose:** BLEU score with modified n-gram precision (clipped by max reference count), brevity penalty, and per-n-gram stats for the table.
- **Functions:**
  - `get_ngrams(segment, n)`: Returns n-gram counts for a token list.
  - `modified_precision(candidate, references, n)`: Returns (precision, clipped_matches, total) for order n.
  - `brevity_penalty(candidate, references)`: BP = exp(1 - r/c) when c ≤ r, else 1.
  - `compute_bleu(candidate, references, max_n=4)`: Geometric mean of 1–4 gram precisions × BP; returns (score, details dict with `bp`, `precisions`, `ngram_table`, lengths).
  - `tokenize_for_bleu(text)`: Whitespace tokenization for BLEU (standard).
- **Design:** No external BLEU package; implementation follows the standard BLEU definition for clarity and control over the n-gram table.

---

## Data Flow

1. User enters source text and (optionally) selects model and beam size.
2. User provides reference(s) by pasting or uploading a file (one reference per line).
3. User clicks **Translate** → `nmt_service.translate()` is called → NMT output is shown and stored.
4. User may add extra candidates (one per line) for comparison.
5. For each candidate, `bleu_utils.tokenize_for_bleu()` and `compute_bleu()` are called; results (BLEU, BP, n-gram table) are displayed in the UI.

---

## Dependencies (requirements.txt)

- **streamlit** — Web UI.
- **transformers** — Hugging Face; loads MarianMT and translation pipeline.
- **torch** — Backend for transformers (CPU or GPU).
- **sentencepiece** — Used by some Marian tokenizers.
- **numpy** — Used by transformers/torch.

---

## References

- MarianMT: [Helsinki-NLP on Hugging Face](https://huggingface.co/Helsinki-NLP)
- BLEU: Papineni et al., "BLEU: a Method for Automatic Evaluation of Machine Translation", ACL 2002.
