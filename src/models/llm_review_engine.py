from pydantic import BaseModel
from typing import List, Dict

class LLMReviewEngineRequest(BaseModel):
    code: str
    language: str

class LLMReviewEngineResponse(BaseModel):
    review: str
    tests: List[str]
    vulnerabilities: List[str]
    optimizations: List[str]
    insights: Dict

class LLMReviewEngineInsights(BaseModel):
    review_insights: Dict
    explainability_insights: Dict
    clone_detection_insights: Dict