```python
import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from typing import Optional
from nextapp import NextApp
from github import Github
from openai import OpenAI

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI()

# Initialize the Next.js app
next_app = NextApp()

# Initialize the GitHub API
github = Github(os.environ.get("GITHUB_TOKEN"))

# Initialize the OpenAI API
openai = OpenAI(os.environ.get("OPENAI_API_KEY"))

# Define the CORS origins
origins = [
    "http://localhost:3000",
    "https://cortex-app.vercel.app",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model
class PullRequest(BaseModel):
    id: int
    title: str
    body: str
    repository: str
    owner: str

# Define the response model
class ReviewResponse(BaseModel):
    id: int
    title: str
    body: str
    repository: str
    owner: str
    review: str

# Define the route for reviewing pull requests
@app.post("/review", response_model=ReviewResponse)
async def review_pull_request(pull_request: PullRequest):
    try:
        # Get the pull request from GitHub
        repo = github.get_repo(pull_request.repository)
        pull_request_obj = repo.get_pull(pull_request.id)

        # Generate a review using the OpenAI API
        review = openai.generate_text(pull_request.body)

        # Return the review response
        return ReviewResponse(
            id=pull_request.id,
            title=pull_request.title,
            body=pull_request.body,
            repository=pull_request.repository,
            owner=pull_request.owner,
            review=review,
        )
    except Exception as e:
        logger.error(f"Error reviewing pull request: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

# Define the route for generating tests
@app.post("/generate-tests", response_model=ReviewResponse)
async def generate_tests(pull_request: PullRequest):
    try:
        # Get the pull request from GitHub
        repo = github.get_repo(pull_request.repository)
        pull_request_obj = repo.get_pull(pull_request.id)

        # Generate tests using the OpenAI API
        tests = openai.generate_tests(pull_request.body)

        # Return the review response
        return ReviewResponse(
            id=pull_request.id,
            title=pull_request.title,
            body=pull_request.body,
            repository=pull_request.repository,
            owner=pull_request.owner,
            review=tests,
        )
    except Exception as e:
        logger.error(f"Error generating tests: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

# Define the route for detecting security vulnerabilities
@app.post("/detect-vulnerabilities", response_model=ReviewResponse)
async def detect_vulnerabilities(pull_request: PullRequest):
    try:
        # Get the pull request from GitHub
        repo = github.get_repo(pull_request.repository)
        pull_request_obj = repo.get_pull(pull_request.id)

        # Detect security vulnerabilities using the OpenAI API
        vulnerabilities = openai.detect_vulnerabilities(pull_request.body)

        # Return the review response
        return ReviewResponse(
            id=pull_request.id,
            title=pull_request.title,
            body=pull_request.body,
            repository=pull_request.repository,
            owner=pull_request.owner,
            review=vulnerabilities,
        )
    except Exception as e:
        logger.error(f"Error detecting vulnerabilities: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

# Define the route for suggesting performance optimizations
@app.post("/suggest-optimizations", response_model=ReviewResponse)
async def suggest_optimizations(pull_request: PullRequest):
    try:
        # Get the pull request from GitHub
        repo = github.get_repo(pull_request.repository)
        pull_request_obj = repo.get_pull(pull_request.id)

        # Suggest performance optimizations using the OpenAI API
        optimizations = openai.suggest_optimizations(pull_request.body)

        # Return the review response
        return ReviewResponse(
            id=pull_request.id,
            title=pull_request.title,
            body=pull_request.body,
            repository=pull_request.repository,
            owner=pull_request.owner,
            review=optimizations,
        )
    except Exception as e:
        logger.error(f"Error suggesting optimizations: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```