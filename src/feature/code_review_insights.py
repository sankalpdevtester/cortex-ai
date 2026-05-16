import os
import requests
from typing import Dict, List
from fastapi import APIRouter, Depends
from github import Github
from openai import OpenAI
from src.main import get_github_token, get_openai_token

router = APIRouter()

def get_github_client():
    token = get_github_token()
    return Github(token)

def get_openai_client():
    token = get_openai_token()
    return OpenAI(token)

@router.post("/code-review-insights")
async def get_code_review_insights(
    pull_request: Dict,
    github_client: Github = Depends(get_github_client),
    openai_client: OpenAI = Depends(get_openai_client)
):
    """
    Analyze a pull request and provide code review insights using OpenAI API.
    
    Args:
    pull_request (Dict): Pull request data from GitHub API.
    
    Returns:
    Dict: Code review insights, including suggestions and comments.
    """
    # Get the pull request files
    files = github_client.get_pull_request_files(pull_request["number"])
    
    # Initialize the insights dictionary
    insights = {
        "suggestions": [],
        "comments": []
    }
    
    # Loop through each file
    for file in files:
        # Get the file contents
        file_contents = github_client.get_file_contents(file["filename"])
        
        # Use OpenAI API to analyze the file contents
        analysis = openai_client.analyze_code(file_contents)
        
        # Extract suggestions and comments from the analysis
        suggestions = analysis["suggestions"]
        comments = analysis["comments"]
        
        # Add the suggestions and comments to the insights dictionary
        insights["suggestions"].extend(suggestions)
        insights["comments"].extend(comments)
    
    return insights

def get_code_similarity(
    file1: str,
    file2: str,
    openai_client: OpenAI = Depends(get_openai_client)
):
    """
    Calculate the similarity between two code files using OpenAI API.
    
    Args:
    file1 (str): Contents of the first file.
    file2 (str): Contents of the second file.
    
    Returns:
    float: Similarity score between 0 and 1.
    """
    # Use OpenAI API to calculate the similarity
    similarity = openai_client.calculate_similarity(file1, file2)
    
    return similarity

@router.post("/code-similarity")
async def get_code_similarity_score(
    file1: str,
    file2: str,
    openai_client: OpenAI = Depends(get_openai_client)
):
    """
    Calculate the similarity between two code files.
    
    Args:
    file1 (str): Contents of the first file.
    file2 (str): Contents of the second file.
    
    Returns:
    float: Similarity score between 0 and 1.
    """
    # Calculate the similarity score
    similarity_score = get_code_similarity(file1, file2, openai_client)
    
    return similarity_score

# Example usage
if __name__ == "__main__":
    # Get the GitHub token
    github_token = get_github_token()
    
    # Get the OpenAI token
    openai_token = get_openai_token()
    
    # Create a GitHub client
    github_client = Github(github_token)
    
    # Create an OpenAI client
    openai_client = OpenAI(openai_token)
    
    # Get a pull request
    pull_request = github_client.get_pull_request(1)
    
    # Get the code review insights
    insights = get_code_review_insights(pull_request, github_client, openai_client)
    
    # Print the insights
    print(insights)