import os
import requests
from typing import List, Dict
from fastapi import APIRouter, Depends
from github import Github
from openai import OpenAI
from src.main import get_github_token, get_openai_token

router = APIRouter()

# Initialize OpenAI and GitHub APIs
openai = OpenAI(get_openai_token())
github = Github(get_github_token())

def get_code_refactoring_suggestions(file_path: str, code: str) -> List[Dict]:
    """
    Get code refactoring suggestions using OpenAI API.

    Args:
    - file_path (str): The path to the file.
    - code (str): The code to refactor.

    Returns:
    - List[Dict]: A list of refactoring suggestions.
    """
    # Use OpenAI API to get code refactoring suggestions
    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=f"Refactor the following code: {code}",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Parse the response
    suggestions = []
    for choice in response.choices:
        suggestion = choice.text.strip()
        suggestions.append({"suggestion": suggestion})

    return suggestions

@router.post("/code-refactoring-suggestions")
async def get_code_refactoring_suggestions_endpoint(file_path: str, code: str):
    """
    Get code refactoring suggestions endpoint.

    Args:
    - file_path (str): The path to the file.
    - code (str): The code to refactor.

    Returns:
    - List[Dict]: A list of refactoring suggestions.
    """
    # Get code refactoring suggestions
    suggestions = get_code_refactoring_suggestions(file_path, code)

    return {"suggestions": suggestions}

def create_pull_request(title: str, body: str, head: str, base: str, repo: str) -> str:
    """
    Create a pull request using GitHub API.

    Args:
    - title (str): The title of the pull request.
    - body (str): The body of the pull request.
    - head (str): The head of the pull request.
    - base (str): The base of the pull request.
    - repo (str): The repository name.

    Returns:
    - str: The pull request URL.
    """
    # Create a pull request
    repo = github.get_repo(repo)
    pull_request = repo.create_pull(title=title, body=body, head=head, base=base)

    return pull_request.html_url

@router.post("/create-pull-request")
async def create_pull_request_endpoint(title: str, body: str, head: str, base: str, repo: str):
    """
    Create a pull request endpoint.

    Args:
    - title (str): The title of the pull request.
    - body (str): The body of the pull request.
    - head (str): The head of the pull request.
    - base (str): The base of the pull request.
    - repo (str): The repository name.

    Returns:
    - str: The pull request URL.
    """
    # Create a pull request
    pull_request_url = create_pull_request(title, body, head, base, repo)

    return {"pull_request_url": pull_request_url}