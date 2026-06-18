from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.feature.llm_review_engine import LLMReviewEngine
from src.utils.cache import Cache

router = APIRouter()

class CodeReviewRequest(BaseModel):
    code: str
    language: str

@router.post("/review")
async def review_code(code_review_request: CodeReviewRequest, cache: Cache = Depends()):
    llm_review_engine = LLMReviewEngine(cache)
    review = llm_review_engine.review_code(code_review_request.code, code_review_request.language)
    return review

@router.post("/tests")
async def generate_tests(code_review_request: CodeReviewRequest, cache: Cache = Depends()):
    llm_review_engine = LLMReviewEngine(cache)
    tests = llm_review_engine.generate_tests(code_review_request.code, code_review_request.language)
    return tests

@router.post("/vulnerabilities")
async def detect_vulnerabilities(code_review_request: CodeReviewRequest, cache: Cache = Depends()):
    llm_review_engine = LLMReviewEngine(cache)
    vulnerabilities = llm_review_engine.detect_vulnerabilities(code_review_request.code, code_review_request.language)
    return vulnerabilities

@router.post("/optimizations")
async def suggest_optimizations(code_review_request: CodeReviewRequest, cache: Cache = Depends()):
    llm_review_engine = LLMReviewEngine(cache)
    optimizations = llm_review_engine.suggest_optimizations(code_review_request.code, code_review_request.language)
    return optimizations

@router.post("/insights")
async def get_insights(code_review_request: CodeReviewRequest, cache: Cache = Depends()):
    llm_review_engine = LLMReviewEngine(cache)
    insights = llm_review_engine.get_insights(code_review_request.code, code_review_request.language)
    return insights