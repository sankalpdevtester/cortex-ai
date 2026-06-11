import os
from typing import Dict, List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.utils.cache import cache
from src.feature.code_review_insights import get_code_review_insights
from src.feature.code_intelligence_dashboard import get_code_intelligence_dashboard
from src.feature.code_explainability_insights import get_code_explainability_insights
from src.feature.code_quality_insights import get_code_quality_insights
import requests
import json

router = APIRouter()

def get_code_difficulty_insights(code: str, language: str) -> Dict:
    """
    Get code difficulty insights using OpenAI API
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "code-difficulty",
        "prompt": code,
        "language": language
    }
    response = requests.post("https://api.openai.com/v1/completions", headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to get code difficulty insights"}

@router.get("/code_difficulty_insights")
async def get_code_difficulty_insights_endpoint(code: str, language: str):
    """
    API endpoint to get code difficulty insights
    """
    insights = get_code_difficulty_insights(code, language)
    return JSONResponse(content=insights, media_type="application/json")

def calculate_code_difficulty(code: str, language: str) -> float:
    """
    Calculate code difficulty using Halstead complexity metrics
    """
    # Calculate Halstead complexity metrics
    n1 = 0  # number of operators
    n2 = 0  # number of operands
    N1 = 0  # number of unique operators
    N2 = 0  # number of unique operands
    for token in code.split():
        if token in ["if", "else", "for", "while", "function"]:
            n1 += 1
            if token not in N1:
                N1 += 1
        else:
            n2 += 1
            if token not in N2:
                N2 += 1
    # Calculate difficulty using Halstead complexity metrics
    difficulty = (n1 + n2) * (N1 + N2) / (2 * (n1 + n2))
    return difficulty

def get_code_difficulty_insights_from_github(pr_number: int, repo_owner: str, repo_name: str) -> Dict:
    """
    Get code difficulty insights from GitHub API
    """
    # Get GitHub API token
    github_token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }
    # Get pull request files
    response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files", headers=headers)
    if response.status_code == 200:
        files = response.json()
        insights = []
        for file in files:
            # Get file contents
            response = requests.get(file["raw_url"], headers=headers)
            if response.status_code == 200:
                code = response.text
                language = file["filename"].split(".")[-1]
                difficulty = calculate_code_difficulty(code, language)
                insights.append({
                    "file": file["filename"],
                    "difficulty": difficulty
                })
        return insights
    else:
        return {"error": "Failed to get code difficulty insights from GitHub"}

@router.get("/code_difficulty_insights_from_github")
async def get_code_difficulty_insights_from_github_endpoint(pr_number: int, repo_owner: str, repo_name: str):
    """
    API endpoint to get code difficulty insights from GitHub
    """
    insights = get_code_difficulty_insights_from_github(pr_number, repo_owner, repo_name)
    return JSONResponse(content=insights, media_type="application/json")

# Integrate with existing files
def get_code_difficulty_insights_from_code_review_insights(code_review_insights: Dict) -> Dict:
    """
    Get code difficulty insights from code review insights
    """
    code = code_review_insights["code"]
    language = code_review_insights["language"]
    difficulty = calculate_code_difficulty(code, language)
    return {"difficulty": difficulty}

def get_code_difficulty_insights_from_code_intelligence_dashboard(code_intelligence_dashboard: Dict) -> Dict:
    """
    Get code difficulty insights from code intelligence dashboard
    """
    code = code_intelligence_dashboard["code"]
    language = code_intelligence_dashboard["language"]
    difficulty = calculate_code_difficulty(code, language)
    return {"difficulty": difficulty}

def get_code_difficulty_insights_from_code_explainability_insights(code_explainability_insights: Dict) -> Dict:
    """
    Get code difficulty insights from code explainability insights
    """
    code = code_explainability_insights["code"]
    language = code_explainability_insights["language"]
    difficulty = calculate_code_difficulty(code, language)
    return {"difficulty": difficulty}

def get_code_difficulty_insights_from_code_quality_insights(code_quality_insights: Dict) -> Dict:
    """
    Get code difficulty insights from code quality insights
    """
    code = code_quality_insights["code"]
    language = code_quality_insights["language"]
    difficulty = calculate_code_difficulty(code, language)
    return {"difficulty": difficulty}