import requests
from src.feature.llm_review_engine import LLMReviewEngine
from src.utils.cache import Cache

class GitHubLLMReviewEngine:
    def __init__(self, cache: Cache):
        self.cache = cache
        self.llm_review_engine = LLMReviewEngine(cache)
        self.github_token = "YOUR_GITHUB_TOKEN"

    def review_pull_request(self, pull_request_id: int) -> Dict:
        # Use GitHub API to get pull request code
        response = requests.get(
            f"https://api.github.com/repos/{self.github_token}/pulls/{pull_request_id}",
            headers={"Authorization": f"Bearer {self.github_token}"},
        )
        code = response.json()["body"]
        language = response.json()["head"]["ref"]

        # Use LLM review engine to review code
        review = self.llm_review_engine.review_code(code, language)
        tests = self.llm_review_engine.generate_tests(code, language)
        vulnerabilities = self.llm_review_engine.detect_vulnerabilities(code, language)
        optimizations = self.llm_review_engine.suggest_optimizations(code, language)
        insights = self.llm_review_engine.get_insights(code, language)

        return {
            "review": review,
            "tests": tests,
            "vulnerabilities": vulnerabilities,
            "optimizations": optimizations,
            "insights": insights,
        }