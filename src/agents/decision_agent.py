# src/agents/decision_agent.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

def get_final_decision(dossier: Dict) -> Dict:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return {"action": "FLAG_FOR_REVIEW", "reasoning": "Gemini agent is not configured."}

    try:
        genai.configure(api_key=api_key)
        
        # --- PROMPT MELHORADO ---
        prompt = f"""
        You are a decisive data quality analyst. Your task is to make a final standardization decision based on a dossier of evidence. Your bias is towards action, trusting the consensus of your specialist agents.

        **Case Dossier:**
        - User Input: "{dossier.get('user_input')}"
        - Lexical Agent Suggestion: "{dossier.get('best_match_lexical')}" (Score: {dossier.get('score_lexical'):.2f})
        - Semantic Agent Suggestion: "{dossier.get('best_match_semantic')}" (Score: {dossier.get('score_semantic'):.2f})

        **Decision Rules:**
        1.  **Rule of Consensus:** If the Lexical Agent and the Semantic Agent suggest the EXACT SAME company, you have very strong evidence. In this case, you SHOULD "AUTO_CORRECT", even if their individual scores are not perfect.
        2.  **Rule of High Confidence:** If either agent has a score above 0.95, you can trust it and "AUTO_CORRECT".
        3.  **Rule of Doubt:** If the agents suggest DIFFERENT companies or their scores are very low (below 0.75), then "FLAG_FOR_REVIEW".

        **Your Task:**
        Apply the rules to the dossier and provide your final verdict.

        **Response Format:**
        Respond with a single, minified JSON object with three keys: "action" (string), "corrected_name" (string, or null), and "reasoning" (a brief, one-sentence explanation applying the rules).
        """

        generation_config = {"temperature": 0.0, "response_mime_type": "application/json"}
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config=generation_config)
        response = model.generate_content(prompt)
        decision_str = response.text
        return json.loads(decision_str)

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {"action": "FLAG_FOR_REVIEW", "reasoning": f"An error occurred in the Gemini agent: {e}"}