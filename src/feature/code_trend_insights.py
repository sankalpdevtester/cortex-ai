import os
import json
from datetime import datetime, timedelta
from typing import List, Dict
from fastapi import HTTPException
from github import Github
from src.utils.cache import cache
from src.feature.code_metrics_insights import get_code_metrics
from src.feature.code_health_insights import get_code_health
from src.feature.code_security_audit import get_code_security_audit

class CodeTrendInsights:
    def __init__(self, github_token: str, repo_owner: str, repo_name: str):
        self.github_token = github_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github = Github(self.github_token)

    def get_code_trend_insights(self) -> Dict:
        """
        Get code trend insights for the given repository.

        Returns:
            A dictionary containing code trend insights.
        """
        repo = self.github.get_repo(f"{self.repo_owner}/{self.repo_name}")
        commits = repo.get_commits()

        # Get code metrics and health insights for each commit
        code_trend_insights = []
        for commit in commits:
            commit_hash = commit.sha
            code_metrics = get_code_metrics(commit_hash, self.repo_owner, self.repo_name)
            code_health = get_code_health(commit_hash, self.repo_owner, self.repo_name)
            code_security_audit = get_code_security_audit(commit_hash, self.repo_owner, self.repo_name)

            # Calculate code trend insights
            code_trend_insight = {
                "commit_hash": commit_hash,
                "commit_date": commit.commit.author.date,
                "code_metrics": code_metrics,
                "code_health": code_health,
                "code_security_audit": code_security_audit,
            }
            code_trend_insights.append(code_trend_insight)

        # Sort code trend insights by commit date
        code_trend_insights.sort(key=lambda x: x["commit_date"])

        return code_trend_insights

    def get_code_trend_insights_over_time(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Get code trend insights over a given time period.

        Args:
            start_date (str): The start date in YYYY-MM-DD format.
            end_date (str): The end date in YYYY-MM-DD format.

        Returns:
            A list of dictionaries containing code trend insights for each day.
        """
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        code_trend_insights_over_time = []
        current_date = start_date
        while current_date <= end_date:
            code_trend_insights = self.get_code_trend_insights()
            code_trend_insights_for_date = [
                insight for insight in code_trend_insights
                if insight["commit_date"].date() == current_date.date()
            ]

            if code_trend_insights_for_date:
                code_trend_insight_for_date = {
                    "date": current_date.strftime("%Y-%m-%d"),
                    "code_trend_insights": code_trend_insights_for_date,
                }
                code_trend_insights_over_time.append(code_trend_insight_for_date)

            current_date += timedelta(days=1)

        return code_trend_insights_over_time

def get_code_trend_insights(github_token: str, repo_owner: str, repo_name: str) -> Dict:
    """
    Get code trend insights for the given repository.

    Args:
        github_token (str): The GitHub token.
        repo_owner (str): The repository owner.
        repo_name (str): The repository name.

    Returns:
        A dictionary containing code trend insights.
    """
    code_trend_insights = CodeTrendInsights(github_token, repo_owner, repo_name)
    return code_trend_insights.get_code_trend_insights()

def get_code_trend_insights_over_time(github_token: str, repo_owner: str, repo_name: str, start_date: str, end_date: str) -> List[Dict]:
    """
    Get code trend insights over a given time period.

    Args:
        github_token (str): The GitHub token.
        repo_owner (str): The repository owner.
        repo_name (str): The repository name.
        start_date (str): The start date in YYYY-MM-DD format.
        end_date (str): The end date in YYYY-MM-DD format.

    Returns:
        A list of dictionaries containing code trend insights for each day.
    """
    code_trend_insights = CodeTrendInsights(github_token, repo_owner, repo_name)
    return code_trend_insights.get_code_trend_insights_over_time(start_date, end_date)