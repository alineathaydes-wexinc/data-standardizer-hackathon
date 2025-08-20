# src/schema.py
from pydantic import BaseModel
from typing import Optional, Dict

class StandardizationRequest(BaseModel):
    """The request model for a standardization task."""
    company_name: str # Only the company name is needed by the backend logic

class StandardizationResponse(BaseModel):
    """The response model containing the agent squad's verdict."""
    status: str
    action: str
    best_match: Optional[str] = None
    reason: Optional[str] = None
    evidence: Optional[Dict] = None