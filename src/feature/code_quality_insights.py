import os
import requests
from typing import Dict, List
from fastapi import APIRouter, Depends
from github import Github
from openai import OpenAI
from src.main import get_github_token, get_openai_token

router = APIRouter()

def get_code_quality_insights(github_token: str, openai_token: str, repo_owner: str, repo_name: str, pull_request_number: int):
    """
    Get code quality insights for a given pull request.
    
    Args:
    - github_token (str): GitHub token for authentication.
    - openai_token (str): OpenAI token for API access.
    - repo_owner (str): Repository owner.
    - repo_name (str): Repository name.
    - pull_request_number (int): Pull request number.
    
    Returns:
    - A dictionary containing code quality insights.
    """
    
    # Initialize GitHub and OpenAI clients
    g = Github(github_token)
    openai = OpenAI(openai_token)
    
    # Get the repository and pull request
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    pull_request = repo.get_pull(pull_request_number)
    
    # Get the pull request files
    files = pull_request.get_files()
    
    # Initialize code quality insights dictionary
    insights = {
        "code_smells": [],
        "security_vulnerabilities": [],
        "performance_optimizations": []
    }
    
    # Iterate over the pull request files
    for file in files:
        # Get the file contents
        file_contents = file.contents
        
        # Analyze the file contents using OpenAI API
        response = openai.analyze_code(file_contents, "python")
        
        # Extract code quality insights from the response
        code_smells = response["code_smells"]
        security_vulnerabilities = response["security_vulnerabilities"]
        performance_optimizations = response["performance_optimizations"]
        
        # Add the insights to the dictionary
        insights["code_smells"].extend(code_smells)
        insights["security_vulnerabilities"].extend(security_vulnerabilities)
        insights["performance_optimizations"].extend(performance_optimizations)
    
    return insights

@router.get("/code-quality-insights")
async def get_code_quality_insights_endpoint(repo_owner: str, repo_name: str, pull_request_number: int):
    """
    Get code quality insights for a given pull request.
    
    Args:
    - repo_owner (str): Repository owner.
    - repo_name (str): Repository name.
    - pull_request_number (int): Pull request number.
    
    Returns:
    - A dictionary containing code quality insights.
    """
    
    # Get the GitHub and OpenAI tokens
    github_token = get_github_token()
    openai_token = get_openai_token()
    
    # Get the code quality insights
    insights = get_code_quality_insights(github_token, openai_token, repo_owner, repo_name, pull_request_number)
    
    return insights