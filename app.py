"""
NMT Application with BLEU Evaluation (Streamlit frontend).

Flow: (1) User enters source text and reference(s) [paste or file upload].
      (2) User clicks Translate → MarianMT produces NMT output.
      (3) BLEU is computed for NMT output (and any extra candidates); results
          show BLEU score, brevity penalty, and n-gram precision table (1–4).
Libraries: streamlit (UI), nmt_service (MarianMT), bleu_utils (BLEU).
"""
import os

# Use project-local cache to avoid permission errors in ~/.cache/huggingface
_app_dir = os.path.dirname(os.path.abspath(__file__))
_cache_dir = os.path.join(_app_dir, ".cache", "huggingface")
os.environ.setdefault("HF_HOME", _cache_dir)
os.environ.setdefault("TRANSFORMERS_CACHE", os.path.join(_cache_dir, "hub"))

import streamlit as st
from bleu_utils import tokenize_for_bleu, compute_bleu
from nmt_service import translate

st.set_page_config(
    page_title="NMT with BLEU Evaluation",
    page_icon="🌐",
    layout="wide",
)

st.title("🌐 NMT System with Automatic Evaluation")
st.caption("Medical/Healthcare-oriented translation & BLEU evaluation")

# --- Sidebar: model and options ---
with st.sidebar:
    st.subheader("Model & options")
    model_choice = st.selectbox(
        "Translation model",
        [
            "Helsinki-NLP/opus-mt-en-de",
            "Helsinki-NLP/opus-mt-en-es",
            "Helsinki-NLP/opus-mt-en-fr",
            "Helsinki-NLP/opus-mt-de-en",
        ],
        help="MarianMT models; for medical domain consider fine-tuning.",
    )
    num_beams = st.slider("Beam size", 1, 8, 4, help="Larger = better quality, slower.")
    st.divider()
    st.markdown("**Task B:** See `Quality_Improvement_Strategy.md` for how to improve BLEU.")

# --- Main: input source text ---
st.subheader("1. Source text (input)")
source = st.text_area(
    "Enter or paste source text to translate",
    height=120,
    placeholder="e.g. The patient presented with fever and cough. Blood pressure was elevated.",
)
translate_btn = st.button("Translate", type="primary")

# --- Reference: upload or paste ---
st.subheader("2. Reference translation")
ref_mode = st.radio("Reference input", ["Paste text", "Upload file"], horizontal=True)
reference_text = ""
if ref_mode == "Paste text":
    reference_text = st.text_area(
        "Paste reference translation(s). One per line for multiple references.",
        height=80,
        placeholder="e.g. Der Patient präsentierte sich mit Fieber und Husten.",
    )
else:
    ref_file = st.file_uploader("Upload reference (e.g. .txt)", type=["txt"])
    if ref_file:
        reference_text = ref_file.read().decode("utf-8", errors="replace")

# Parse references: one per line, non-empty
references_raw = [r.strip() for r in (reference_text or "").strip().split("\n") if r.strip()]
references_tok = [tokenize_for_bleu(r) for r in references_raw]

# --- Candidates: NMT + optional extra candidates ---
st.subheader("3. Candidate translation(s)")
if "nmt_output" not in st.session_state:
    st.session_state["nmt_output"] = ""

if translate_btn and source.strip():
    with st.spinner("Running NMT..."):
        nmt_out = translate(source, model_name=model_choice, num_beams=num_beams)
    st.session_state["nmt_output"] = nmt_out

# Build list: NMT first, then any extra candidates
candidates_raw = []
if st.session_state["nmt_output"]:
    candidates_raw.append(("NMT output", st.session_state["nmt_output"]))

# Show NMT output
if st.session_state["nmt_output"]:
    st.text_area("NMT output", value=st.session_state["nmt_output"], height=100, disabled=True)

# Optional: add more candidates for comparison
st.markdown("**Add more candidates** (e.g. another system or manual translation) to compare BLEU:")
extra_candidates = st.text_area(
    "One candidate per line (optional)",
    height=80,
    placeholder="Paste additional translation(s), one per line.",
)
if extra_candidates.strip():
    for i, line in enumerate(extra_candidates.strip().split("\n")):
        if line.strip():
            candidates_raw.append((f"Candidate {i+1}", line.strip()))

# --- Evaluation: BLEU and n-gram table ---
st.subheader("4. BLEU evaluation")
if not references_tok:
    st.info("Add at least one reference (paste or upload) to compute BLEU.")
else:
    if not candidates_raw:
        st.info("Translate to get an NMT candidate, or add candidates above.")
    else:
        for label, cand_text in candidates_raw:
            if not cand_text.strip():
                continue
            cand_tok = tokenize_for_bleu(cand_text)
            bleu, details = compute_bleu(cand_tok, references_tok, max_n=4)

            with st.expander(f"**{label}** — BLEU: {bleu:.4f}", expanded=(label == "NMT output")):
                st.write("**Translation:**")
                st.write(cand_text)
                st.write("---")
                st.write("**BLEU score:**", f"**{bleu:.4f}**")
                st.write("**Brevity penalty:**", f"{details['bp']:.4f}")
                st.write("**Lengths:** candidate =", details["candidate_len"], "| reference(s) =", details["reference_lens"])
                st.write("**N-gram precision table:**")
                table_data = []
                for row in details["ngram_table"]:
                    table_data.append({
                        "n": row["n"],
                        "Precision": f"{row['precision']:.4f}",
                        "Clipped matches": row["clipped"],
                        "Total n-grams": row["total"],
                    })
                st.table(table_data)

st.divider()
st.markdown("---")
st.caption("NMT: MarianMT (Helsinki-NLP). BLEU: modified n-gram precision + brevity penalty.")
