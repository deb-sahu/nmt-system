# NMT System with Automatic BLEU Evaluation

Medical/healthcare-oriented Neural Machine Translation (NMT) application with BLEU-based quality evaluation.

---

## Deliverables Checklist

### Part 1: Task A & B (10 Marks)

| Deliverable | Status | Location |
|-------------|--------|----------|
| Well-documented code (Python, NMT libraries, frontend) | ✅ | `app.py`, `nmt_service.py`, `bleu_utils.py`, `DOCUMENTATION.md` |
| Instructions for running the application locally | ✅ | This README, section **“How to run locally”** |
| Brief report (design choices, challenges, NMT integration) | ✅ | `REPORT.md` |
| Screenshots explaining full flow with results | Placeholders in report | `REPORT.md` §4 — add your screenshots there |
| Task B (Quality Improvement Strategy) as PDF | Content ready | Export `Quality_Improvement_Strategy.md` to PDF (see below) |

### Part 2: Literature Survey (5 Marks)

| Deliverable | Status | Location |
|-------------|--------|----------|
| Literature Survey: Automatic Evaluation Metrics for NMT | ✅ | `Literature_Survey.md` — export to PDF |

---

## How to Run the Application Locally

### Prerequisites

- **Python:** 3.8 or 3.9+ recommended.
- **OS:** Windows, macOS, or Linux.
- **Network:** Required for first run (downloads MarianMT model from Hugging Face).
- **Disk:** ~500 MB free for model cache.

### Steps

1. **Clone or copy the project** and open a terminal in the project folder:
   ```bash
   cd /path/to/nlpa2
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser:**  
   The terminal will show a URL (e.g. `http://localhost:8501`). Open it in your browser.

6. **Use the app:**
   - Enter or paste **source text** (e.g. medical sentence in English).
   - Choose **reference**: paste translation(s) or upload a `.txt` file (one reference per line).
   - Click **Translate** to get NMT output.
   - View **BLEU score**, **brevity penalty**, and **n-gram precision table** (1–4 grams).
   - Optionally add **extra candidates** (one per line) to compare multiple translations.
   - **Sample inputs:** see **`SAMPLE_EXAMPLES.md`** for copy-paste source and reference examples.

### Troubleshooting

- **“No module named 'streamlit'”** → Run `pip install -r requirements.txt` inside the same venv.
- **First translation is slow** → Model is downloaded on first use; later runs reuse the cached model.
- **Out of memory** → Use a smaller beam size in the sidebar or shorten the source text.
- **PermissionError on Hugging Face cache** (e.g. when switching to opus-mt-en-es) → The app now uses a **project-local cache** (`.cache/huggingface/` inside the project). Restart the app and try again; models will download into the project folder. If you still see permission errors, remove any stale lock: `rm -rf ~/.cache/huggingface/hub/.locks/models--Helsinki-NLP--opus-mt-en-es` (and the same for other model names if needed).

---

## Task B: Submit as PDF

Task B is written in **`Quality_Improvement_Strategy.md`**. To submit it as a **.pdf document**:

1. **Option A — Pandoc (command line):**
   ```bash
   pandoc Quality_Improvement_Strategy.md -o Quality_Improvement_Strategy.pdf
   ```

2. **Option B — VS Code / Cursor:**  
   Install a “Markdown PDF” or “Print” extension, open `Quality_Improvement_Strategy.md`, then export or print to PDF.

3. **Option C — Browser:**  
   Open the `.md` file in a Markdown preview or a site that renders Markdown, then use the browser’s Print → Save as PDF.

Submit the generated **`Quality_Improvement_Strategy.pdf`** (or the same content in a single PDF with your report) as required.

---

## Project Layout

| File | Description |
|------|-------------|
| `app.py` | Streamlit frontend: source input, reference (paste/upload), NMT output, BLEU results |
| `nmt_service.py` | NMT translation using MarianMT (Helsinki-NLP) via Hugging Face |
| `bleu_utils.py` | BLEU computation: modified n-gram precision, brevity penalty, n-gram table |
| `requirements.txt` | Python dependencies (Streamlit, transformers, torch, etc.) |
| `README.md` | This file — run instructions and deliverables |
| `DOCUMENTATION.md` | Code and architecture documentation |
| `REPORT.md` | Design report: design choices, challenges, NMT integration, screenshot placeholders |
| `Quality_Improvement_Strategy.md` | Task B content — export to PDF for submission |
| `Literature_Survey.md` | Part 2: Literature survey (5 marks) — export to PDF |

---

## Task A Summary

- **UI:** Source text input; reference by paste or file upload; display of NMT output, BLEU score, brevity penalty, and n-gram precision table (1–4).
- **Translation:** MarianMT (Helsinki-NLP) Transformer models; optional beam size.
- **Evaluation:** Custom BLEU with modified n-gram precision and brevity penalty; support for multiple references and multiple candidates.
