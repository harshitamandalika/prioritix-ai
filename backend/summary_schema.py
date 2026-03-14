from pydantic import BaseModel
from typing import Dict, Any


class SummaryRequest(BaseModel):
    max_reviews: int = 100
    include_sample_reviews: bool = True


class SummaryResponse(BaseModel):
    summary: str
    structured_summary: Dict[str, Any]