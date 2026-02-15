# NMT System with BLEU Evaluation

A web app for neural machine translation with automatic quality evaluation. Built for medical/healthcare text, but works with any content.

---

## What This Project Does

- Translates text using MarianMT (Transformer-based models from Helsinki-NLP)
- Computes BLEU score to measure translation quality
- Shows a detailed breakdown: n-gram precision (1-gram through 4-gram), brevity penalty, match counts
- Lets you compare multiple translations side by side

---

## Quick Start

**You'll need:** Python 3.8+, about 500MB disk space, internet connection (first run downloads the model)

```bash
# 1. Go to the project folder
cd /path/to/nlpa2

# 2. Set up a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Open the URL shown in terminal (usually http://localhost:8501).

---

## How to Use

1. **Enter source text** — Type or paste the text you want to translate (e.g., a medical sentence in English)
2. **Add a reference** — Paste a human translation, or upload a .txt file. This is what BLEU compares against.
3. **Click Translate** — The NMT model translates your text
4. **See the results** — BLEU score, brevity penalty, and a table showing how many n-grams matched

Want to compare multiple translations? Paste them in the "Add more candidates" box (one per line).

Check `SAMPLE_EXAMPLES.md` for ready-to-use medical text examples.

---

## If Something Goes Wrong

- **"No module named streamlit"** — Make sure you activated the venv and ran `pip install -r requirements.txt`
- **Translation takes forever** — First run downloads the model (~300MB). After that it's cached.
- **Out of memory** — Try a smaller beam size (sidebar slider) or shorter text
- **Permission error with Hugging Face** — The app uses a local cache folder. Just restart and try again.

---

## Project Files

| File | What it does |
|------|--------------|
| `app.py` | The web interface (Streamlit) |
| `nmt_service.py` | Handles translation using MarianMT |
| `bleu_utils.py` | BLEU score calculation with n-gram precision and brevity penalty |
| `requirements.txt` | Python packages needed |
| `REPORT.md` | Design report for submission |
| `SAMPLE_EXAMPLES.md` | Example inputs to try |

---

## How the Code Works

### Translation (`nmt_service.py`)

Uses Hugging Face's `transformers` library to load MarianMT models. These are Transformer encoder-decoder models trained on millions of sentence pairs. The app supports multiple language pairs (en-de, en-es, en-fr, de-en) — just pick one from the sidebar.

Key function: `translate(text, model_name, num_beams)` — takes source text, returns translated text.

### BLEU Computation (`bleu_utils.py`)

Implements the standard BLEU formula from scratch:
- **Modified n-gram precision**: counts matching n-grams but clips by the max count in any reference (so repeating words doesn't game the score)
- **Brevity penalty**: penalizes translations that are too short
- **Final score**: geometric mean of 1-4 gram precisions × brevity penalty

Why not use sacrebleu or nltk? Because the assignment asks for the n-gram table with clipped counts, and building it ourselves makes that easy to display.

### Web UI (`app.py`)

Streamlit app with:
- Text area for source input
- Reference input (paste or file upload)
- Model selection and beam size in sidebar
- Results section showing BLEU, BP, and the n-gram precision table for each candidate

---