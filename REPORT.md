# NMT Application — Design Report

**Project:** Neural Machine Translation with Automatic BLEU Evaluation  
**Domain:** Medical/Healthcare-oriented  
**Deliverable:** Part 1 — Brief report (design choices, challenges, NMT integration)

---

## 1. Design Choices

### 1.1 Frontend: Streamlit

- **Choice:** Streamlit for the web UI instead of Flask/FastAPI + HTML/JS or a separate frontend.
- **Reason:** Streamlit provides a single Python codebase, quick iteration, built-in file upload and text areas, and no separate frontend build. It fits the scope of an NMT demo with input → translate → BLEU output.
- **Trade-off:** Less control over exact layout and styling than a custom frontend; acceptable for a coursework/demo application.

### 1.2 NMT: MarianMT (Helsinki-NLP) via Hugging Face

- **Choice:** Transformer-based NMT using MarianMT models (`opus-mt-*`) from Hugging Face `transformers`.
- **Reason:** MarianMT offers many language pairs, is well-supported in `transformers`, runs on CPU or GPU, and is suitable for extension (e.g. fine-tuning for medical domain). No custom training code required for the baseline.
- **Alternatives considered:** Generic seq2seq or custom Transformer would require training; using MarianMT keeps the deliverable focused on integration and evaluation.

### 1.3 BLEU: Custom Implementation

- **Choice:** Custom BLEU in `bleu_utils.py` (modified n-gram precision, brevity penalty, 1–4 gram table) instead of only using `nltk.translate.bleu_score` or `sacrebleu`.
- **Reason:** The assignment asks for BLEU with **brevity penalty** and **n-gram precision table** (1-gram, 2-gram, etc.). A custom implementation makes these components explicit and gives full control over the displayed table (clipped matches, totals per n).
- **Standard alignment:** Formula follows the standard BLEU definition (geometric mean of precisions × BP) so results are interpretable and comparable.

### 1.4 Reference and Candidate Input

- **Choice:** Reference via either paste (multi-line = multiple references) or file upload; candidates = NMT output + optional extra lines (multiple candidates).
- **Reason:** Supports single/multiple references and comparison of NMT vs other candidates (e.g. another system or manual translation) as required by the assignment.

---

## 2. Challenges Faced

### 2.1 Model Download and Resource Use

- **Challenge:** First run downloads the chosen MarianMT model (hundreds of MB); inference on CPU can be slow for long texts.
- **Mitigation:** Pipeline is cached per model so the same model is not re-downloaded; UI shows a “Running NMT…” spinner; user can choose a smaller beam for faster runs. For production, GPU would be recommended.

### 2.2 Tokenization Consistency for BLEU

- **Challenge:** BLEU is sensitive to tokenization. MarianMT uses subword tokenization; references are usually word-level.
- **Mitigation:** BLEU is computed on **whitespace-tokenized** text (candidate and references) so that the evaluation is word-based and comparable to standard BLEU reporting. NMT output is used as plain text (no subword tokens exposed in the metric).

### 2.3 Medical Domain

- **Challenge:** Default MarianMT models are general-domain; medical terminology may be translated less accurately.
- **Mitigation:** The app allows model selection and documents in Task B that **fine-tuning on domain-specific (medical) data** is the recommended way to improve quality and BLEU; the current app provides the pipeline and evaluation framework to plug in a fine-tuned model later.

---

## 3. How the NMT Model Was Integrated and Used

### 3.1 Integration Stack

- **Library:** Hugging Face `transformers`.
- **API used:** `pipeline("translation", model=model_name)` with `model_name` e.g. `Helsinki-NLP/opus-mt-en-de`.
- **Flow:** User selects model in UI → on “Translate”, `nmt_service.translate(source_text, model_name=..., num_beams=...)` is called → pipeline runs encoder–decoder inference → translated string is returned and displayed.

### 3.2 Usage in the Application

1. **Configuration:** Model choice and beam size are set in the Streamlit sidebar.
2. **Translation:** When the user clicks “Translate”, the app calls `translate()` with the current source text and options; the result is stored and shown in the “NMT output” area.
3. **Evaluation:** The same output (and any extra candidates) is passed to `bleu_utils.compute_bleu()` after tokenization; BLEU score, brevity penalty, and n-gram table are shown per candidate.
4. **Multiple candidates:** Additional candidates can be pasted (one per line); each is evaluated against the same reference(s) so the user can compare BLEU and n-gram precisions across systems.

### 3.3 Extensibility

- **New models:** Any Hugging Face translation model compatible with `pipeline("translation", ...)` can be added to the sidebar list and used without changing the rest of the code.
- **Fine-tuned model:** A fine-tuned MarianMT (e.g. on medical data) can be loaded by using its Hugging Face model id or local path as `model_name`.

---

## 4. Screenshots — Application Flow (with Results/Output)

*Include the following screenshots in your final report (e.g. paste into this section or into a separate document that you submit).*

### 4.1 Application home / input screen

**[INSERT SCREENSHOT 1]**  
*Caption: Main interface showing (1) Source text area with sample medical text, (2) Reference translation section (paste or upload), (3) Model selection in sidebar (e.g. Helsinki-NLP/opus-mt-en-de) and beam size.*

---

### 4.2 After clicking “Translate” — NMT output

**[INSERT SCREENSHOT 2]**  
*Caption: Same screen after “Translate” was clicked. NMT output is visible in the “NMT output” text area. Reference is present so the BLEU section is active.*

---

### 4.3 BLEU evaluation — score and n-gram table

**[INSERT SCREENSHOT 3]**  
*Caption: BLEU evaluation section expanded for “NMT output”: BLEU score, brevity penalty, candidate/reference lengths, and the n-gram precision table (1-gram through 4-gram with Precision, Clipped matches, Total n-grams).*

---

### 4.4 Multiple candidates (optional)

**[INSERT SCREENSHOT 4]**  
*Caption: (Optional) Extra candidates added in the “Add more candidates” box; two or more expanders shown (e.g. “NMT output” and “Candidate 1”) with different BLEU scores and n-gram tables.*

---

### 4.5 Reference via file upload

**[INSERT SCREENSHOT 5]**  
*Caption: Reference translation provided via “Upload file” and a .txt file, with BLEU results displayed.*

---

**Checklist for screenshots:**

- [ ] Screenshot 1: Main UI with source text (and optionally reference)
- [ ] Screenshot 2: NMT output visible after Translate
- [ ] Screenshot 3: BLEU score + brevity penalty + n-gram table
- [ ] Screenshot 4 (optional): Multiple candidates compared
- [ ] Screenshot 5 (optional): File upload for reference

Once you have taken these screenshots, paste them into this report (or into the PDF version) in the order above and add the captions. This documents the full flow and results of the application.
