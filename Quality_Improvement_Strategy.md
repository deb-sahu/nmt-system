# Task B: Quality Improvement Strategy — How to Increase BLEU

This document explains how BLEU score can be increased in an NMT system using:

1. **Fine-tuning on domain-specific datasets**  
2. **Better tokenization strategies**  
3. **Ensemble methods or beam search optimization**

---

## 1. Fine-tuning on domain-specific datasets

**Why it helps BLEU:**  
BLEU measures n-gram overlap with reference translations. When the NMT model is trained (or fine-tuned) on in-domain data (e.g. medical/healthcare), it produces outputs that use the same terminology, style, and phrasing as the references. That increases lexical and n-gram overlap, hence higher precision and BLEU.

**How to do it:**

- **Data:** Collect or use existing parallel corpora in the target domain (e.g. medical reports, clinical notes, drug labels) in source–target language pairs.
- **Base model:** Start from a strong general-purpose NMT model (e.g. Helsinki-NLP MarianMT `opus-mt-{src}-{tgt}`).
- **Fine-tuning:** Continue training the model on the domain corpus for a few epochs, with a small learning rate, so it adapts to medical vocabulary and constructions without forgetting general language.
- **Effect:** References in medical evaluations are usually from the same domain; in-domain outputs match them better → higher 1–4 gram precision and thus higher BLEU.

---

## 2. Better tokenization strategies

**Why it helps BLEU:**  
BLEU is computed on token sequences. If the evaluation uses different tokenization (e.g. subwords vs words) than the references, n-gram boundaries can misalign and scores drop. Consistent, appropriate tokenization aligns candidate and reference n-grams better and can also improve model quality.

**How to do it:**

- **Match tokenization at evaluation:** Use the same tokenizer (and the same pre-processing, e.g. lowercasing, punctuation) for both the NMT output and the reference(s) when computing BLEU. Many toolkits use space-based word tokenization for BLEU; if you use subwords (e.g. SentencePiece), either:
  - compute BLEU in the same subword space, or  
  - detokenize both sides and use a common word-level tokenizer (e.g. `moses truecase/tokenizer`) so BLEU is comparable.
- **Model-side tokenization:** For medical text, use or train a subword tokenizer (e.g. BPE, SentencePiece) on in-domain data so that medical terms are split consistently and the model sees stable subword units. This reduces rare-word issues and can improve translation quality and n-gram overlap.
- **Result:** Better alignment of n-grams between hypothesis and reference → higher modified n-gram precision and more stable BLEU.

---

## 3. Ensemble methods or beam search optimization

**Why it helps BLEU:**  
BLEU is computed on a single candidate translation. Better candidates (closer to the reference) yield higher BLEU. Ensembles and improved decoding produce better candidates.

**Ensemble methods:**

- **Model ensemble:** Train or use several NMT models (e.g. different seeds or checkpoints, or different architectures). For each source sentence, get one translation per model, then either:
  - **Choose the best:** Score each candidate with a language model or a metric (e.g. BLEU against a dev set) and pick the best, or  
  - **Combine:** Use minimum Bayes risk (MBR) decoding or similar to select the candidate that is “closest” on average to the others (often closer to references as well).
- **Effect:** The chosen or combined translation is often more accurate and lexically closer to references → higher n-gram overlap and BLEU.

**Beam search optimization:**

- **Larger beam:** Increasing beam size (e.g. from 1–2 to 4–8) allows the decoder to explore more hypotheses and often find a higher-scoring translation. This can improve both quality and BLEU, with a trade-off in speed.
- **Length normalization:** Tuning length normalization (or length penalty) in beam search can reduce systematic length bias (e.g. too short or too long), improving brevity penalty and n-gram coverage and thus BLEU.
- **Result:** Better decoding → better candidate sentences → higher BLEU when references are fixed.

---

## Summary

| Strategy                    | Main effect on BLEU |
|----------------------------|----------------------|
| Domain fine-tuning         | Better lexical and n-gram match to in-domain references. |
| Better tokenization        | Consistent n-gram boundaries and fewer mismatches. |
| Ensembles / beam search    | Higher-quality candidates → more n-gram overlap with references. |

Using all three together—fine-tuning on medical data, consistent and domain-aware tokenization, and improved decoding (beam search and/or ensembles)—typically yields the largest gains in BLEU for medical/healthcare NMT.
