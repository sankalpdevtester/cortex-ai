# src/feature/code_metrics_insights.py
from typing import Dict, List
from src.utils.cache import Cache
from src.feature.llm_code_review import LLMCodeReview
from src.feature.code_difficulty_insights import CodeDifficultyInsights
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
import requests
import json

class CodeMetricsInsights:
    def __init__(self, cache: Cache, llm_code_review: LLMCodeReview, code_difficulty_insights: CodeDifficultyInsights):
        self.cache = cache
        self.llm_code_review = llm_code_review
        self.code_difficulty_insights = code_difficulty_insights

    def calculate_code_metrics(self, code: str) -> Dict:
        # Calculate complexity metrics (e.g., cyclomatic complexity, halstead complexity)
        complexity_metrics = self.calculate_complexity_metrics(code)
        
        # Calculate maintainability metrics (e.g., maintainability index)
        maintainability_metrics = self.calculate_maintainability_metrics(code)
        
        # Calculate readability metrics (e.g., readability score)
        readability_metrics = self.calculate_readability_metrics(code)
        
        return {
            "complexity": complexity_metrics,
            "maintainability": maintainability_metrics,
            "readability": readability_metrics
        }

    def calculate_complexity_metrics(self, code: str) -> Dict:
        # Use a library like radon to calculate complexity metrics
        import radon
        complexity = radon.complexity.cc_rank(code)
        return {
            "cyclomatic_complexity": complexity,
            "halstead_complexity": self.calculate_halstead_complexity(code)
        }

    def calculate_maintainability_metrics(self, code: str) -> Dict:
        # Use a library like radon to calculate maintainability metrics
        import radon
        maintainability_index = radon.mi_score(code)
        return {
            "maintainability_index": maintainability_index
        }

    def calculate_readability_metrics(self, code: str) -> Dict:
        # Use a library like textstat to calculate readability metrics
        import textstat
        readability_score = textstat.flesch_reading_ease(code)
        return {
            "readability_score": readability_score
        }

    def calculate_halstead_complexity(self, code: str) -> float:
        # Calculate halstead complexity using the formula: V = N * log2(N)
        # where N is the number of operators and operands
        import re
        operators = re.findall(r'\W', code)
        operands = re.findall(r'\w', code)
        N = len(operators) + len(operands)
        V = N * (N ** 0.5)
        return V

    def get_code_metrics_insights(self, request: Request) -> JSONResponse:
        code = request.json.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Code is required")
        
        cache_key = f"code_metrics_insights_{code}"
        cached_response = self.cache.get(cache_key)
        if cached_response:
            return JSONResponse(content=cached_response, media_type="application/json")
        
        code_metrics = self.calculate_code_metrics(code)
        self.cache.set(cache_key, code_metrics, 60)  # cache for 1 minute
        return JSONResponse(content=code_metrics, media_type="application/json")

# Example usage:
# from src.feature.code_metrics_insights import CodeMetricsInsights
# code_metrics_insights = CodeMetricsInsights(Cache(), LLMCodeReview(), CodeDifficultyInsights())
# code = "def add(a, b): return a + b"
# print(code_metrics_insights.calculate_code_metrics(code))