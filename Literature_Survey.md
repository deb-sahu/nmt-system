# Literature Survey: Automatic Evaluation Metrics for Neural Machine Translation

**Course:** Natural Language Processing  
**Assignment:** 2 — Part 2  
**Topic:** Automatic Evaluation Metrics for Neural Machine Translation  

---

## Abstract

Automatic evaluation of machine translation (MT) quality is essential for rapid development and comparison of translation systems. This survey reviews the major evaluation metrics used for Neural Machine Translation (NMT), from traditional n-gram-based methods like BLEU to modern neural embedding-based approaches like BERTScore and COMET. We discuss the strengths, weaknesses, and use cases of each metric, and highlight recent trends in MT evaluation research.

---

## 1. Introduction

### 1.1 The Need for Automatic Evaluation

Human evaluation remains the gold standard for assessing translation quality, but it is:
- **Expensive:** Requires trained bilingual annotators
- **Slow:** Cannot scale to thousands of system outputs
- **Inconsistent:** Inter-annotator agreement varies

Automatic metrics address these limitations by providing fast, reproducible, and cost-effective evaluation. However, the central challenge is designing metrics that correlate well with human judgments of translation adequacy and fluency.

### 1.2 Scope of This Survey

This survey covers:
1. **N-gram-based metrics:** BLEU, NIST, chrF
2. **Edit-distance metrics:** TER, WER
3. **Alignment-based metrics:** METEOR
4. **Neural embedding-based metrics:** BERTScore, BLEURT, COMET, YiSi
5. **Recent trends and WMT Metrics Shared Task findings**

---

## 2. N-gram-Based Metrics

### 2.1 BLEU (Bilingual Evaluation Understudy)

**Reference:** Papineni et al. (2002). "BLEU: a Method for Automatic Evaluation of Machine Translation." ACL.

**Definition:**
BLEU computes the geometric mean of modified n-gram precisions (1-gram to 4-gram) multiplied by a brevity penalty:

$$
\text{BLEU} = \text{BP} \times \exp\left( \sum_{n=1}^{N} w_n \log p_n \right)
$$

Where:
- $p_n$ = modified n-gram precision (clipped by max reference count)
- $w_n$ = weight (typically $1/N$ for uniform weighting)
- $\text{BP} = \min(1, e^{1 - r/c})$ where $c$ = candidate length, $r$ = closest reference length

**Strengths:**
- Simple, fast, language-independent
- Widely adopted; enables cross-study comparison
- Correlates reasonably well with human judgment at corpus level

**Weaknesses:**
- **No semantic understanding:** Treats all words equally; ignores synonyms and paraphrases
- **Precision-only:** Does not reward recall (addressed by brevity penalty, but imperfectly)
- **Sentence-level weakness:** Poor correlation with human judgment for single sentences
- **Tokenization sensitivity:** Results vary with tokenization choices

**Variants:**
- **SacreBLEU** (Post, 2018): Standardized BLEU with explicit tokenization and versioning for reproducibility
- **Sentence-BLEU:** Smoothed versions for sentence-level evaluation (Chen & Cherry, 2014)

---

### 2.2 NIST

**Reference:** Doddington (2002). "Automatic Evaluation of Machine Translation Quality Using N-gram Co-Occurrence Statistics." HLT.

**Definition:**
NIST is similar to BLEU but weights n-grams by their information content (rarer n-grams contribute more). It also uses a different brevity penalty.

**Strengths:**
- Rewards informative (less frequent) n-grams
- More stable for small test sets

**Weaknesses:**
- Less commonly used than BLEU; harder to compare across studies

---

### 2.3 chrF (Character n-gram F-score)

**Reference:** Popović (2015). "chrF: character n-gram F-score for automatic MT evaluation." WMT.

**Definition:**
chrF computes F-score over character n-grams (typically 1–6) rather than word n-grams:

$$
\text{chrF} = (1 + \beta^2) \times \frac{\text{chrP} \times \text{chrR}}{\beta^2 \times \text{chrP} + \text{chrR}}
$$

Where chrP = character n-gram precision, chrR = character n-gram recall, $\beta$ controls precision/recall balance (often $\beta=2$ for chrF++).

**Strengths:**
- **Morphologically robust:** Better for morphologically rich languages (German, Finnish, Turkish)
- **Tokenization-free:** Operates on raw characters
- **Recall-aware:** Includes recall via F-score

**Weaknesses:**
- May reward character-level similarity without semantic correctness

---

## 3. Edit-Distance Metrics

### 3.1 TER (Translation Edit Rate)

**Reference:** Snover et al. (2006). "A Study of Translation Edit Rate with Targeted Human Annotation." AMTA.

**Definition:**
TER measures the minimum number of edits (insertions, deletions, substitutions, shifts of contiguous word sequences) needed to transform the candidate into the reference, normalized by reference length:

$$
\text{TER} = \frac{\text{# edits}}{\text{# reference words}}
$$

**Strengths:**
- Intuitive interpretation (lower is better)
- Allows phrasal shifts (not just single-word edits)

**Weaknesses:**
- **No semantic matching:** "big" → "large" counts as an error
- **Shift operation is expensive:** Exact computation is NP-hard; approximations used

**Variants:**
- **TERp (TER-plus):** Adds stemming, synonyms, and paraphrase support
- **HTER (Human TER):** Uses human post-edits as reference; gold standard for effort estimation

---

### 3.2 WER (Word Error Rate)

**Definition:**
WER is the Levenshtein distance (insertions, deletions, substitutions) normalized by reference length. It is widely used in speech recognition and sometimes in MT.

**Difference from TER:**
WER does not allow phrasal shifts; only single-word operations.

---

## 4. Alignment-Based Metrics

### 4.1 METEOR (Metric for Evaluation of Translation with Explicit ORdering)

**Reference:** Banerjee & Lavie (2005). "METEOR: An Automatic Metric for MT Evaluation with Improved Correlation with Human Judgments." ACL Workshop.

**Definition:**
METEOR aligns candidate and reference words using exact match, stemming, synonyms (WordNet), and paraphrase tables. It computes:

$$
\text{METEOR} = F_{\text{mean}} \times (1 - \text{Penalty})
$$

Where:
- $F_{\text{mean}}$ = harmonic mean of precision and recall (weighted toward recall)
- Penalty = fragmentation penalty based on number of chunks (longer contiguous matches = lower penalty)

**Strengths:**
- **Recall-aware:** Explicitly rewards recall
- **Semantic matching:** Uses stemming and synonyms
- **Better sentence-level correlation:** Often outperforms BLEU at sentence level

**Weaknesses:**
- **Language-dependent resources:** Requires stemmer, synonym database, paraphrase tables
- **Slower than BLEU:** Alignment computation is more complex
- **Parameter tuning:** Weights tuned on specific language pairs; may not generalize

---

## 5. Neural Embedding-Based Metrics

### 5.1 BERTScore

**Reference:** Zhang et al. (2020). "BERTScore: Evaluating Text Generation with BERT." ICLR.

**Definition:**
BERTScore computes similarity between candidate and reference using contextual embeddings from BERT (or similar models). For each token in the candidate, it finds the most similar token in the reference (and vice versa), then aggregates:

$$
\text{BERTScore} = F_1(\text{Precision}, \text{Recall})
$$

Where precision and recall are based on cosine similarity of token embeddings.

**Strengths:**
- **Semantic similarity:** Captures meaning beyond surface form
- **Handles paraphrases:** "big" and "large" have similar embeddings
- **State-of-the-art correlation:** Often best or near-best in WMT Metrics tasks

**Weaknesses:**
- **Computationally expensive:** Requires running BERT for each sentence
- **Model-dependent:** Results vary with BERT variant and layer choice
- **Less interpretable:** Hard to explain why a score is high or low

---

### 5.2 BLEURT (Bilingual Evaluation Understudy with Representations from Transformers)

**Reference:** Sellam et al. (2020). "BLEURT: Learning Robust Metrics for Text Generation." ACL.

**Definition:**
BLEURT is a learned metric. It fine-tunes BERT on a mix of:
1. Synthetic data (backtranslation, word drops, etc.)
2. Human ratings from WMT

The model outputs a single quality score given (reference, candidate).

**Strengths:**
- **Trained on human judgments:** Directly optimizes for correlation with human scores
- **Robust:** Pre-training on synthetic data helps generalization

**Weaknesses:**
- **Requires training data:** May not generalize to new domains or languages without re-training
- **Expensive to train:** Fine-tuning BERT on large datasets

---

### 5.3 COMET (Crosslingual Optimized Metric for Evaluation of Translation)

**Reference:** Rei et al. (2020). "COMET: A Neural Framework for MT Evaluation." EMNLP.

**Definition:**
COMET uses multilingual encoders (e.g., XLM-RoBERTa) and is trained on Direct Assessment (DA) human scores from WMT. It can operate in:
- **Reference-based mode:** (source, candidate, reference) → score
- **Reference-free mode (QE-as-a-metric):** (source, candidate) → score

**Strengths:**
- **State-of-the-art correlation:** Winner of WMT Metrics Shared Task (2020–2022)
- **Source-aware:** Uses source sentence, unlike BLEU/BERTScore
- **Multilingual:** Works across many language pairs

**Weaknesses:**
- **Model size:** Requires large multilingual encoder
- **Domain shift:** Trained on news domain; may need adaptation for medical, legal, etc.

---

### 5.4 YiSi

**Reference:** Lo (2019). "YiSi – a Unified Semantic MT Quality Evaluation and Estimation Metric for Languages with Different Levels of Available Resources." WMT.

**Definition:**
YiSi computes semantic similarity using word embeddings (YiSi-1) or contextual embeddings (YiSi-2). It supports reference-based and reference-free modes.

**Strengths:**
- Modular: Can use static or contextual embeddings
- Supports low-resource languages (with cross-lingual embeddings)

---

## 6. Comparison of Metrics

| Metric | Type | Recall? | Semantic? | Speed | Sentence-Level | Corpus-Level |
|--------|------|---------|-----------|-------|----------------|--------------|
| BLEU | N-gram | No (BP only) | No | Fast | Poor | Good |
| chrF | Char n-gram | Yes (F-score) | No | Fast | Moderate | Good |
| TER | Edit distance | Implicit | No | Moderate | Moderate | Good |
| METEOR | Alignment | Yes | Partial | Moderate | Good | Good |
| BERTScore | Neural | Yes | Yes | Slow | Very Good | Very Good |
| BLEURT | Neural (learned) | — | Yes | Slow | Very Good | Very Good |
| COMET | Neural (learned) | — | Yes | Slow | Best | Best |

**Key Insight:** Neural metrics (BERTScore, COMET, BLEURT) consistently achieve higher correlation with human judgments than n-gram metrics, especially at the sentence level. However, they are computationally expensive and may require domain adaptation.

---

## 7. Recent Trends (2020–2025)

### 7.1 WMT Metrics Shared Task Findings

The Conference on Machine Translation (WMT) runs an annual Metrics Shared Task. Key findings:

| Year | Top Metrics | Observation |
|------|-------------|-------------|
| 2020 | COMET, BLEURT | Neural metrics dominate; BLEU ranks poorly |
| 2021 | COMET, BLEURT, BERTScore | Reference-free (QE) metrics emerge |
| 2022 | COMET-22, MetricX | Ensemble and fine-tuned metrics lead |
| 2023 | COMET-Kiwi, xCOMET | Explainability and error spans added |
| 2024 | xCOMET, MetricX-24 | Focus on fine-grained error detection |

**Trend:** The field is moving toward **learned, neural metrics** that are trained on human judgments and can operate without references (quality estimation).

### 7.2 Reference-Free Evaluation (Quality Estimation)

Quality Estimation (QE) predicts translation quality without a reference. Recent work (COMET-QE, TransQuest) achieves competitive correlation with human scores, enabling evaluation when references are unavailable (e.g., real-time systems).

### 7.3 Explainable Metrics

Recent metrics (xCOMET, MQM-based models) not only produce a score but also highlight error spans (e.g., "mistranslation at position 5–8"). This aids human post-editing and debugging.

### 7.4 Multidimensional Quality Metrics (MQM)

MQM (Multidimensional Quality Metrics) is an error-typology framework. Annotators mark errors by type (accuracy, fluency, terminology) and severity. Metrics like GEMBA-MQM and xCOMET now incorporate MQM-style error categories.

---

## 8. Strengths and Weaknesses of BLEU (Detailed)

Since BLEU is the most widely used metric, a detailed analysis is warranted.

### 8.1 Strengths

1. **Simplicity:** Easy to compute; no external resources beyond tokenizer.
2. **Speed:** Runs in milliseconds even on large corpora.
3. **Reproducibility:** With SacreBLEU, results are standardized and comparable.
4. **Language-agnostic:** Works for any language pair (given tokenization).

### 8.2 Weaknesses

1. **No semantic understanding:**
   - "The cat sat on the mat" vs. "The feline rested on the rug" → low BLEU despite similar meaning.

2. **Precision-only bias:**
   - A candidate that is a subset of the reference can score well even if missing content.

3. **Poor sentence-level correlation:**
   - BLEU was designed for corpus-level; sentence-level smoothing (BLEU+1) helps but is still weak.

4. **Tokenization sensitivity:**
   - Different tokenizers (Moses, SentencePiece, whitespace) yield different scores.

5. **Ignores word order (partially):**
   - N-grams capture local order, but global reordering is not penalized strongly.

6. **All n-grams weighted equally:**
   - Content words and function words contribute the same (NIST addresses this).

---

## 9. Recommendations for Practitioners

| Scenario | Recommended Metric(s) |
|----------|----------------------|
| **Quick development iteration** | BLEU (SacreBLEU), chrF |
| **Final system comparison** | COMET, BLEURT, BERTScore |
| **Morphologically rich languages** | chrF, COMET |
| **No reference available** | COMET-QE, TransQuest |
| **Sentence-level evaluation** | COMET, BERTScore, METEOR |
| **Explainable feedback for post-editing** | xCOMET, MQM-based |

---

## 10. Conclusion

Automatic evaluation metrics for NMT have evolved significantly from rule-based n-gram counting (BLEU) to learned neural models (COMET, BLEURT). While BLEU remains a useful baseline due to its simplicity and speed, modern neural metrics achieve substantially higher correlation with human judgments, especially at the sentence level.

Key takeaways:

1. **BLEU is necessary but not sufficient:** Use it for quick checks, but validate with neural metrics for final evaluation.
2. **Neural metrics are the new standard:** COMET and BLEURT are recommended by WMT for system ranking.
3. **Reference-free metrics are emerging:** Quality estimation enables evaluation without parallel references.
4. **Domain matters:** Metrics trained on news data may need adaptation for medical, legal, or conversational MT.

Future directions include:
- **Explainable metrics** that highlight specific errors
- **Multilingual and low-resource metrics** using cross-lingual embeddings
- **Fine-grained error typologies** (MQM integration)
- **Efficiency improvements** for neural metrics in real-time applications

---

## References

1. Papineni, K., Roukos, S., Ward, T., & Zhu, W. J. (2002). BLEU: a Method for Automatic Evaluation of Machine Translation. *ACL*.

2. Doddington, G. (2002). Automatic Evaluation of Machine Translation Quality Using N-gram Co-Occurrence Statistics. *HLT*.

3. Banerjee, S., & Lavie, A. (2005). METEOR: An Automatic Metric for MT Evaluation with Improved Correlation with Human Judgments. *ACL Workshop on Intrinsic and Extrinsic Evaluation Measures*.

4. Snover, M., Dorr, B., Schwartz, R., Micciulla, L., & Makhoul, J. (2006). A Study of Translation Edit Rate with Targeted Human Annotation. *AMTA*.

5. Popović, M. (2015). chrF: character n-gram F-score for automatic MT evaluation. *WMT*.

6. Post, M. (2018). A Call for Clarity in Reporting BLEU Scores. *WMT*.

7. Chen, B., & Cherry, C. (2014). A Systematic Comparison of Smoothing Techniques for Sentence-Level BLEU. *WMT*.

8. Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., & Artzi, Y. (2020). BERTScore: Evaluating Text Generation with BERT. *ICLR*.

9. Sellam, T., Das, D., & Parikh, A. P. (2020). BLEURT: Learning Robust Metrics for Text Generation. *ACL*.

10. Rei, R., Stewart, C., Farinha, A. C., & Lavie, A. (2020). COMET: A Neural Framework for MT Evaluation. *EMNLP*.

11. Lo, C. (2019). YiSi – a Unified Semantic MT Quality Evaluation and Estimation Metric. *WMT*.

12. Freitag, M., et al. (2022). Results of the WMT22 Metrics Shared Task. *WMT*.

13. Freitag, M., et al. (2023). Results of the WMT23 Metrics Shared Task. *WMT*.

14. Rei, R., et al. (2023). Scaling up COMETKiwi: Unbabel-IST 2023 Submission for the Quality Estimation Shared Task. *WMT*.

15. Lommel, A., Uszkoreit, H., & Burchardt, A. (2014). Multidimensional Quality Metrics (MQM): A Framework for Declaring and Describing Translation Quality Metrics. *Tradumàtica*.

---

## Appendix: Metric Formulas Summary

### BLEU
$$
\text{BLEU} = \text{BP} \times \exp\left( \sum_{n=1}^{4} \frac{1}{4} \log p_n \right)
$$

### chrF (with β=2)
$$
\text{chrF}_\beta = (1 + \beta^2) \times \frac{\text{chrP} \times \text{chrR}}{\beta^2 \times \text{chrP} + \text{chrR}}
$$

### TER
$$
\text{TER} = \frac{\text{insertions} + \text{deletions} + \text{substitutions} + \text{shifts}}{\text{reference length}}
$$

### METEOR
$$
\text{METEOR} = F_{\text{mean}} \times (1 - \gamma \times \text{frag}^\beta)
$$

### BERTScore
$$
P = \frac{1}{|c|} \sum_{c_i \in c} \max_{r_j \in r} \cos(\mathbf{c}_i, \mathbf{r}_j)
$$
$$
R = \frac{1}{|r|} \sum_{r_j \in r} \max_{c_i \in c} \cos(\mathbf{c}_i, \mathbf{r}_j)
$$
$$
\text{BERTScore} = 2 \times \frac{P \times R}{P + R}
$$

---

*End of Literature Survey*
