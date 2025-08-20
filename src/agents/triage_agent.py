# src/agents/triage_agent.py
import jellyfish
from typing import List, Dict

# Thresholds ajustados para a nova estratégia
HIGH_CONFIDENCE_THRESHOLD = 0.95  # Apenas para acertos quase perfeitos
ESCALATION_THRESHOLD = 0.70     # Limiar para escalar para os especialistas

def run_triage(user_input: str, canonical_names: List[str]) -> Dict:
    """
    Performs a quick, low-cost check for obvious matches or clear non-matches.
    """
    if not user_input or not user_input.strip():
        return {"status": "REJECTED", "reason": "Invalid input"}

    scores = {name: jellyfish.jaro_winkler_similarity(user_input, name) for name in canonical_names}
    best_match = max(scores, key=scores.get)
    best_score = scores[best_match]

    if best_score >= HIGH_CONFIDENCE_THRESHOLD:
        return {
            "status": "RESOLVED",
            "action": "AUTO_CORRECT",
            "best_match": best_match,
            "score": best_score,
            "reason": "High confidence lexical match."
        }
    elif best_score < ESCALATION_THRESHOLD:
        return {
            "status": "RESOLVED",
            "action": "FLAG_FOR_REVIEW",
            "best_match": best_match,
            "score": best_score,
            "reason": "Low confidence lexical match."
        }
    else:
        # This is an "interesting" case that needs more analysis
        return {
            "status": "NEEDS_ESCALATION",
            "best_match_lexical": best_match,
            "score_lexical": best_score,
            "reason": "Ambiguous lexical match. Escalating to specialist agents."
        }