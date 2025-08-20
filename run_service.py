# run_service.py
import streamlit as st
import pandas as pd
from fastapi import FastAPI, HTTPException
from src.schema import StandardizationRequest, StandardizationResponse
from src.core.orchestrator import run_standardization_pipeline
from src.agents.semantic_agent import SemanticSearchAgent

# --- App Initialization ---
app = FastAPI(
    title="AI Agent Squad API",
    description="An API for standardizing data using a multi-agent system.",
    version="1.0.0"
)

# --- Singleton Pattern for Agent ---
# This ensures the heavy model is loaded only once when the service starts.
@st.cache_resource
def get_semantic_agent_cached():
    """Loads and caches the SemanticSearchAgent."""
    try:
        companies_df = pd.read_csv("data/enterprise_companies.csv")
        canonical_names = companies_df['CompanyName'].tolist()
        return SemanticSearchAgent(canonical_names=canonical_names)
    except FileNotFoundError:
        return None

semantic_agent = get_semantic_agent_cached()

# --- API Endpoints ---
@app.post("/standardize", response_model=StandardizationResponse)
async def standardize_data(request: StandardizationRequest):
    """
    Receives company name and returns the standardization verdict from the AI Agent Squad.
    """
    if not semantic_agent:
        raise HTTPException(status_code=503, detail="Semantic agent not initialized. Please check server logs.")
        
    final_result = run_standardization_pipeline(request.company_name, semantic_agent)
    
    return StandardizationResponse(**final_result)

@app.get("/health")
def health_check():
    """Health check endpoint to verify service status."""
    return {"status": "ok", "semantic_agent_loaded": semantic_agent is not None}