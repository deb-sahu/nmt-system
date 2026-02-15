"""
BLEU score computation with modified n-gram precision and brevity penalty.
Supports single/multiple references and detailed n-gram precision table.
"""
from collections import Counter
import math
from typing import List, Tuple, Optional


def get_ngrams(segment: List[str], n: int) -> Counter:
    """Extract n-grams from a tokenized segment."""
    return Counter(tuple(segment[i : i + n]) for i in range(len(segment) - n + 1))


def modified_precision(
    candidate: List[str], references: List[List[str]], n: int
) -> Tuple[float, int, int]:
    """
    Modified n-gram precision (clip counts by max ref count).
    Returns (precision, clipped_matches, total_candidate_ngrams).
    """
    candidate_ngrams = get_ngrams(candidate, n)
    if not candidate_ngrams:
        return 0.0, 0, 0

    max_ref_counts = Counter()
    for ref in references:
        ref_ngrams = get_ngrams(ref, n)
        for ng, count in ref_ngrams.items():
            max_ref_counts[ng] = max(max_ref_counts.get(ng, 0), count)

    clipped_matches = 0
    for ng, count in candidate_ngrams.items():
        clipped_matches += min(count, max_ref_counts.get(ng, 0))

    total = sum(candidate_ngrams.values())
    precision = clipped_matches / total if total else 0.0
    return precision, clipped_matches, total


def brevity_penalty(candidate: List[str], references: List[List[str]]) -> float:
    """
    Brevity penalty: penalize short translations.
    BP = 1 if c > r else exp(1 - r/c)
    """
    c = len(candidate)
    ref_lens = [len(r) for r in references]
    r = min(ref_lens, key=lambda x: abs(x - c))
    if c > r:
        return 1.0
    if c == 0:
        return 0.0
    return math.exp(1 - r / c)


def compute_bleu(
    candidate: List[str],
    references: List[List[str]],
    max_n: int = 4,
    weights: Optional[List[float]] = None,
) -> Tuple[float, dict]:
    """
    Compute BLEU score with geometric mean of n-gram precisions and brevity penalty.
    Returns (BLEU_score, details_dict) where details has:
      - bp: brevity penalty
      - precisions: {1: p1, 2: p2, ...}
      - ngram_table: list of (n, precision, clipped, total) for display
    """
    if weights is None:
        weights = [1.0 / max_n] * max_n

    precisions = {}
    ngram_table = []

    for n in range(1, max_n + 1):
        p, clipped, total = modified_precision(candidate, references, n)
        precisions[n] = p
        ngram_table.append({"n": n, "precision": p, "clipped": clipped, "total": total})

    # Geometric mean of precisions (log-space to avoid underflow)
    log_prec_sum = sum(math.log(p + 1e-10) for p in precisions.values())
    geo_mean = math.exp(log_prec_sum / max_n)

    bp = brevity_penalty(candidate, references)
    bleu = bp * geo_mean

    details = {
        "bleu": bleu,
        "bp": bp,
        "precisions": precisions,
        "ngram_table": ngram_table,
        "candidate_len": len(candidate),
        "reference_lens": [len(r) for r in references],
    }
    return bleu, details


def tokenize_for_bleu(text: str) -> List[str]:
    """Simple whitespace tokenization for BLEU (standard practice)."""
    return text.strip().split()
