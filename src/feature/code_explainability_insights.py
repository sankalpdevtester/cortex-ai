import os
import requests
from typing import Dict, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.main import app
from src.feature.code_review_insights import get_code_review_insights

# Define the router for the new feature
router = APIRouter()

# Define the model for the explainability insights
class ExplainabilityInsights(BaseModel):
    code_snippet: str
    explanation: str

# Define the function to get explainability insights
def get_explainability_insights(code_snippet: str, github_repo: str, github_token: str) -> ExplainabilityInsights:
    # Use OpenAI API to generate an explanation for the code snippet
    openai_api_url = "https://api.openai.com/v1/completions"
    openai_api_key = os.environ["OPENAI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "code-davinci-002",
        "prompt": f"Explain the following code snippet: {code_snippet}",
        "max_tokens": 1024,
        "temperature": 0.7
    }
    response = requests.post(openai_api_url, headers=headers, json=data)
    explanation = response.json()["choices"][0]["text"]

    # Use GitHub API to get the context of the code snippet
    github_api_url = f"https://api.github.com/repos/{github_repo}/contents/{github_repo.split('/')[-1]}.py"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(github_api_url, headers=headers)
    context = response.json()["content"]

    # Return the explainability insights
    return ExplainabilityInsights(code_snippet=code_snippet, explanation=explanation)

# Define the API endpoint for the new feature
@router.post("/explainability_insights")
async def get_explainability_insights_endpoint(code_snippet: str, github_repo: str, github_token: str):
    insights = get_explainability_insights(code_snippet, github_repo, github_token)
    return {"insights": insights}

# Add the new feature to the main app
app.include_router(router)

# Define a function to integrate the new feature with the existing code review insights feature
def get_code_review_insights_with_explainability(github_repo: str, github_token: str, code_snippet: str):
    review_insights = get_code_review_insights(github_repo, github_token, code_snippet)
    explainability_insights = get_explainability_insights(code_snippet, github_repo, github_token)
    return {"review_insights": review_insights, "explainability_insights": explainability_insights}

# Define the API endpoint for the integrated feature
@router.post("/code_review_insights_with_explainability")
async def get_code_review_insights_with_explainability_endpoint(github_repo: str, github_token: str, code_snippet: str):
    insights = get_code_review_insights_with_explainability(github_repo, github_token, code_snippet)
    return {"insights": insights}