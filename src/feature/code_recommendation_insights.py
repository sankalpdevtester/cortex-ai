import os
import requests
from typing import List, Dict
from src.utils.cache import Cache
from src.feature.llm_code_review_insights import LLMCodeReviewInsights
from src.feature.code_metrics_insights import CodeMetricsInsights
from src.feature.code_health_insights import CodeHealthInsights
from src.feature.code_security_audit import CodeSecurityAudit
from src.feature.code_similarity import CodeSimilarity
from src.feature.code_clone_detection import CodeCloneDetection
from src.routes.llm_code_review import LLMCodeReview

class CodeRecommendationInsights:
    def __init__(self, github_token: str, openai_token: str):
        self.github_token = github_token
        self.openai_token = openai_token
        self.cache = Cache()

    def get_code_recommendations(self, repository: str, pull_request: int) -> List[Dict]:
        cache_key = f"code_recommendations_{repository}_{pull_request}"
        if self.cache.exists(cache_key):
            return self.cache.get(cache_key)

        # Get the pull request files using the GitHub API
        github_api_url = f"https://api.github.com/repos/{repository}/pulls/{pull_request}/files"
        headers = {"Authorization": f"Bearer {self.github_token}"}
        response = requests.get(github_api_url, headers=headers)
        files = response.json()

        # Get the code review insights using the LLMCodeReviewInsights class
        llm_code_review_insights = LLMCodeReviewInsights(self.openai_token)
        code_review_insights = llm_code_review_insights.get_code_review_insights(files)

        # Get the code metrics insights using the CodeMetricsInsights class
        code_metrics_insights = CodeMetricsInsights()
        metrics_insights = code_metrics_insights.get_code_metrics_insights(files)

        # Get the code health insights using the CodeHealthInsights class
        code_health_insights = CodeHealthInsights()
        health_insights = code_health_insights.get_code_health_insights(files)

        # Get the code security audit using the CodeSecurityAudit class
        code_security_audit = CodeSecurityAudit()
        security_audit = code_security_audit.get_code_security_audit(files)

        # Get the code similarity using the CodeSimilarity class
        code_similarity = CodeSimilarity()
        similarity = code_similarity.get_code_similarity(files)

        # Get the code clone detection using the CodeCloneDetection class
        code_clone_detection = CodeCloneDetection()
        clone_detection = code_clone_detection.get_code_clone_detection(files)

        # Use the LLM to generate code recommendations based on the insights
        llm_api_url = "https://api.openai.com/v1/completions"
        headers = {"Authorization": f"Bearer {self.openai_token}"}
        data = {
            "model": "code-davinci-002",
            "prompt": "Generate code recommendations based on the following insights: "
                      + str(code_review_insights)
                      + str(metrics_insights)
                      + str(health_insights)
                      + str(security_audit)
                      + str(similarity)
                      + str(clone_detection),
            "max_tokens": 2048,
            "temperature": 0.7,
        }
        response = requests.post(llm_api_url, headers=headers, json=data)
        recommendations = response.json()["choices"][0]["text"]

        # Cache the recommendations for 1 hour
        self.cache.set(cache_key, recommendations, 3600)

        return [recommendations]

# Example usage:
github_token = os.environ["GITHUB_TOKEN"]
openai_token = os.environ["OPENAI_TOKEN"]
code_recommendation_insights = CodeRecommendationInsights(github_token, openai_token)
repository = "example/repository"
pull_request = 123
recommendations = code_recommendation_insights.get_code_recommendations(repository, pull_request)
print(recommendations)