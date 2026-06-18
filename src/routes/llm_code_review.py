from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.feature.llm_code_review import llmCodeReview

app = FastAPI()

class LLMCodeReviewRequest(BaseModel):
    owner: str
    repo: str
    pullRequestNumber: int

@app.post("/llm-code-review")
async def llm_code_review(request: LLMCodeReviewRequest):
    try:
        insights = await llmCodeReview(request.owner, request.repo, request.pullRequestNumber)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))