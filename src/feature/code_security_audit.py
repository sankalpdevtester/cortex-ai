import os
import requests
from typing import List, Dict
from fastapi import APIRouter, Depends
from github import Github
from openai import OpenAI
from src.main import get_github_token, get_openai_token

router = APIRouter()

def get_github_client(token: str):
    """Get a GitHub client instance"""
    return Github(token)

def get_openai_client(token: str):
    """Get an OpenAI client instance"""
    return OpenAI(token)

@router.post("/code-security-audit")
async def code_security_audit(
    repo_owner: str,
    repo_name: str,
    branch: str,
    github_token: str = Depends(get_github_token),
    openai_token: str = Depends(get_openai_token)
):
    """Perform a code security audit on a GitHub repository"""
    github_client = get_github_client(github_token)
    openai_client = get_openai_client(openai_token)

    # Get the repository and branch
    repo = github_client.get_repo(f"{repo_owner}/{repo_name}")
    commit = repo.get_commit(branch)

    # Get the code files in the repository
    code_files = []
    for file in commit.files:
        if file.filename.endswith(('.py', '.java', '.js', '.cpp', '.c')):
            code_files.append(file)

    # Analyze each code file for security vulnerabilities
    vulnerabilities = []
    for file in code_files:
        # Get the file contents
        file_contents = repo.get_contents(file.filename, ref=branch).content

        # Use OpenAI to analyze the code for security vulnerabilities
        response = openai_client.analyze_code(file_contents, "security-vulnerabilities")
        vulnerabilities.extend(response["vulnerabilities"])

    # Return the list of vulnerabilities
    return {"vulnerabilities": vulnerabilities}

def analyze_code_for_vulnerabilities(code: str) -> List[Dict]:
    """Analyze code for security vulnerabilities using OpenAI"""
    openai_token = os.environ["OPENAI_TOKEN"]
    openai_client = OpenAI(openai_token)

    response = openai_client.analyze_code(code, "security-vulnerabilities")
    return response["vulnerabilities"]

def get_code_files(repo_owner: str, repo_name: str, branch: str, github_token: str) -> List:
    """Get the code files in a GitHub repository"""
    github_client = Github(github_token)
    repo = github_client.get_repo(f"{repo_owner}/{repo_name}")
    commit = repo.get_commit(branch)

    code_files = []
    for file in commit.files:
        if file.filename.endswith(('.py', '.java', '.js', '.cpp', '.c')):
            code_files.append(file)

    return code_files