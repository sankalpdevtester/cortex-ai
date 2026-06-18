from typing import List, Dict
from fastapi import Depends
from pydantic import BaseModel
from src.utils.cache import Cache
from src.feature.code_review_insights import CodeReviewInsights
from src.feature.code_explainability_insights import CodeExplainabilityInsights
from src.feature.code_clone_detection import CodeCloneDetection
import openai

class LLMReviewEngine:
    def __init__(self, cache: Cache):
        self.cache = cache
        self.openai_api_key = "YOUR_OPENAI_API_KEY"
        openai.api_key = self.openai_api_key

    def review_code(self, code: str, language: str) -> Dict:
        # Use OpenAI API to review code
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=f"Review the following {language} code: {code}",
            max_tokens=2048,
            temperature=0.7,
        )
        review = response.choices[0].text
        return {"review": review}

    def generate_tests(self, code: str, language: str) -> List[str]:
        # Use OpenAI API to generate tests
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=f"Generate tests for the following {language} code: {code}",
            max_tokens=2048,
            temperature=0.7,
        )
        tests = response.choices[0].text.split("\n")
        return tests

    def detect_vulnerabilities(self, code: str, language: str) -> List[str]:
        # Use OpenAI API to detect vulnerabilities
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=f"Detect vulnerabilities in the following {language} code: {code}",
            max_tokens=2048,
            temperature=0.7,
        )
        vulnerabilities = response.choices[0].text.split("\n")
        return vulnerabilities

    def suggest_optimizations(self, code: str, language: str) -> List[str]:
        # Use OpenAI API to suggest optimizations
        response = openai.Completion.create(
            model="code-davinci-002",
            prompt=f"Suggest optimizations for the following {language} code: {code}",
            max_tokens=2048,
            temperature=0.7,
        )
        optimizations = response.choices[0].text.split("\n")
        return optimizations

    def get_insights(self, code: str, language: str) -> Dict:
        # Use existing features to get insights
        review_insights = CodeReviewInsights().get_insights(code, language)
        explainability_insights = CodeExplainabilityInsights().get_insights(code, language)
        clone_detection_insights = CodeCloneDetection().get_insights(code, language)
        return {
            "review_insights": review_insights,
            "explainability_insights": explainability_insights,
            "clone_detection_insights": clone_detection_insights,
        }