# Import required libraries
from typing import Dict, List
import requests
from src.utils.cache import Cache
from src.feature.code_quality_insights import CodeQualityInsights
from src.feature.code_security_audit import CodeSecurityAudit
from src.feature.code_metrics_insights import CodeMetricsInsights
from src.feature.code_difficulty_insights import CodeDifficultyInsights

class CodeHealthInsights:
    def __init__(self, github_token: str, openai_token: str):
        self.github_token = github_token
        self.openai_token = openai_token
        self.cache = Cache()

    def get_code_health_insights(self, repo_owner: str, repo_name: str, commit_hash: str) -> Dict:
        # Check if insights are already cached
        cache_key = f"code_health_insights_{repo_owner}_{repo_name}_{commit_hash}"
        if self.cache.exists(cache_key):
            return self.cache.get(cache_key)

        # Initialize insights dictionary
        insights = {
            "maintainability": 0,
            "reliability": 0,
            "security": 0,
            "performance": 0,
            "code_quality": 0,
            "code_difficulty": 0,
        }

        # Get code quality insights
        code_quality_insights = CodeQualityInsights(self.github_token, self.openai_token)
        insights["code_quality"] = code_quality_insights.get_code_quality_insights(repo_owner, repo_name, commit_hash)

        # Get code security audit insights
        code_security_audit = CodeSecurityAudit(self.github_token, self.openai_token)
        insights["security"] = code_security_audit.get_code_security_audit_insights(repo_owner, repo_name, commit_hash)

        # Get code metrics insights
        code_metrics_insights = CodeMetricsInsights(self.github_token, self.openai_token)
        insights["performance"] = code_metrics_insights.get_code_metrics_insights(repo_owner, repo_name, commit_hash)

        # Get code difficulty insights
        code_difficulty_insights = CodeDifficultyInsights(self.github_token, self.openai_token)
        insights["code_difficulty"] = code_difficulty_insights.get_code_difficulty_insights(repo_owner, repo_name, commit_hash)

        # Calculate maintainability and reliability insights
        insights["maintainability"] = (insights["code_quality"] + insights["code_difficulty"]) / 2
        insights["reliability"] = (insights["security"] + insights["performance"]) / 2

        # Cache insights for 1 hour
        self.cache.set(cache_key, insights, 3600)

        return insights

    def get_code_health_score(self, repo_owner: str, repo_name: str, commit_hash: str) -> float:
        insights = self.get_code_health_insights(repo_owner, repo_name, commit_hash)
        return (insights["maintainability"] + insights["reliability"] + insights["security"] + insights["performance"] + insights["code_quality"] + insights["code_difficulty"]) / 6

# Example usage
if __name__ == "__main__":
    github_token = "your_github_token"
    openai_token = "your_openai_token"
    code_health_insights = CodeHealthInsights(github_token, openai_token)
    repo_owner = "your_repo_owner"
    repo_name = "your_repo_name"
    commit_hash = "your_commit_hash"
    insights = code_health_insights.get_code_health_insights(repo_owner, repo_name, commit_hash)
    print(insights)
    score = code_health_insights.get_code_health_score(repo_owner, repo_name, commit_hash)
    print(score)