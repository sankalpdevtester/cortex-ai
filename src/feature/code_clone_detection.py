import os
import requests
from typing import List
from fastapi import APIRouter, Depends
from github import Github
from openai import OpenAI
from src.main import get_github_token, get_openai_token

router = APIRouter()

# Initialize GitHub and OpenAI clients
github = Github(get_github_token())
openai = OpenAI(get_openai_token())

def get_code_clones(file_path: str, code: str) -> List[str]:
    """
    Detect code clones using OpenAI API.

    Args:
    file_path (str): The path to the file.
    code (str): The code to detect clones for.

    Returns:
    List[str]: A list of code clones.
    """
    # Use OpenAI API to detect code clones
    response = openai.search(
        query=code,
        max_rerank=10,
        file_path=file_path,
        model="code-search-text-001"
    )

    # Extract code clones from the response
    code_clones = []
    for result in response["data"]:
        code_clones.append(result["text"])

    return code_clones

def get_github_code_clones(repo: str, file_path: str, code: str) -> List[str]:
    """
    Detect code clones in a GitHub repository using GitHub API.

    Args:
    repo (str): The GitHub repository.
    file_path (str): The path to the file.
    code (str): The code to detect clones for.

    Returns:
    List[str]: A list of code clones.
    """
    # Use GitHub API to search for code clones
    repo = github.get_repo(repo)
    search_results = repo.search_code(query=code)

    # Extract code clones from the search results
    code_clones = []
    for result in search_results:
        code_clones.append(result.code)

    return code_clones

@router.post("/code-clone-detection")
async def detect_code_clones(file_path: str, code: str, repo: str = None):
    """
    Detect code clones using OpenAI API and GitHub API.

    Args:
    file_path (str): The path to the file.
    code (str): The code to detect clones for.
    repo (str): The GitHub repository (optional).

    Returns:
    List[str]: A list of code clones.
    """
    # Detect code clones using OpenAI API
    code_clones = get_code_clones(file_path, code)

    # If a GitHub repository is provided, detect code clones using GitHub API
    if repo:
        github_code_clones = get_github_code_clones(repo, file_path, code)
        code_clones.extend(github_code_clones)

    return code_clones

# Example usage
if __name__ == "__main__":
    file_path = "example.py"
    code = "def add(a, b): return a + b"
    repo = "example/repo"

    code_clones = detect_code_clones(file_path, code, repo)
    print(code_clones)