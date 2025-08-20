# src/core/orchestrator.py
from src.agents import triage_agent, decision_agent
from src.agents.semantic_agent import SemanticSearchAgent
from typing import List, Dict

def run_standardization_pipeline(user_input: str, semantic_agent: SemanticSearchAgent) -> Dict:
    """
    Manages the full pipeline of agents to standardize a company name.
    """
    # === STAGE 1: Triage Agent ===
    triage_result = triage_agent.run_triage(user_input, semantic_agent.canonical_names)

    if triage_result["status"] == "RESOLVED":
        # The case was simple and resolved by the Triage Agent
        return triage_result

    # === STAGE 2: Semantic Agent (Escalation) ===
    semantic_result = semantic_agent.find_best_match(user_input)

    # === STAGE 3: Decision Agent (Final Verdict) ===
    # Compile all evidence into a dossier for the final agent
    dossier = {
        "user_input": user_input,
        **triage_result,
        **semantic_result
    }
    
    final_decision = decision_agent.get_final_decision(dossier)
    
    # Combine results for a comprehensive final output
    return {
        "status": "RESOLVED_BY_LLM",
        "action": final_decision.get("action"),
        "best_match": final_decision.get("corrected_name"),
        "reason": final_decision.get("reasoning"),
        "evidence": dossier # Include all evidence for transparency
    }