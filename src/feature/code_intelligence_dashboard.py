# src/feature/code_intelligence_dashboard.py
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from typing import List, Dict
from src.utils.cache import Cache
from src.feature.code_review_insights import CodeReviewInsights
from src.feature.code_explainability_insights import CodeExplainabilityInsights
from src.feature.code_quality_insights import CodeQualityInsights
from src.feature.code_security_audit import CodeSecurityAudit
from src.feature.code_compliance_insights import CodeComplianceInsights
from src.feature.code_recommendation import CodeRecommendation
from src.feature.code_refactoring_suggestions import CodeRefactoringSuggestions
from src.feature.code_similarity import CodeSimilarity
from src.feature.code_clone_detection import CodeCloneDetection

router = APIRouter()

@router.get("/code-intelligence-dashboard")
async def get_code_intelligence_dashboard(
    request: Request,
    cache: Cache = Depends(),
    code_review_insights: CodeReviewInsights = Depends(),
    code_explainability_insights: CodeExplainabilityInsights = Depends(),
    code_quality_insights: CodeQualityInsights = Depends(),
    code_security_audit: CodeSecurityAudit = Depends(),
    code_compliance_insights: CodeComplianceInsights = Depends(),
    code_recommendation: CodeRecommendation = Depends(),
    code_refactoring_suggestions: CodeRefactoringSuggestions = Depends(),
    code_similarity: CodeSimilarity = Depends(),
    code_clone_detection: CodeCloneDetection = Depends(),
):
    # Get insights and metrics from various features
    review_insights = code_review_insights.get_insights()
    explainability_insights = code_explainability_insights.get_insights()
    quality_insights = code_quality_insights.get_insights()
    security_audit = code_security_audit.get_audit()
    compliance_insights = code_compliance_insights.get_insights()
    recommendation = code_recommendation.get_recommendation()
    refactoring_suggestions = code_refactoring_suggestions.get_suggestions()
    similarity = code_similarity.get_similarity()
    clone_detection = code_clone_detection.get_detection()

    # Cache the insights and metrics
    cache.set("code_intelligence_dashboard", {
        "review_insights": review_insights,
        "explainability_insights": explainability_insights,
        "quality_insights": quality_insights,
        "security_audit": security_audit,
        "compliance_insights": compliance_insights,
        "recommendation": recommendation,
        "refactoring_suggestions": refactoring_suggestions,
        "similarity": similarity,
        "clone_detection": clone_detection,
    })

    # Return the cached insights and metrics
    return JSONResponse(content=cache.get("code_intelligence_dashboard"), media_type="application/json")

@router.get("/code-intelligence-dashboard/refresh")
async def refresh_code_intelligence_dashboard(
    request: Request,
    cache: Cache = Depends(),
    code_review_insights: CodeReviewInsights = Depends(),
    code_explainability_insights: CodeExplainabilityInsights = Depends(),
    code_quality_insights: CodeQualityInsights = Depends(),
    code_security_audit: CodeSecurityAudit = Depends(),
    code_compliance_insights: CodeComplianceInsights = Depends(),
    code_recommendation: CodeRecommendation = Depends(),
    code_refactoring_suggestions: CodeRefactoringSuggestions = Depends(),
    code_similarity: CodeSimilarity = Depends(),
    code_clone_detection: CodeCloneDetection = Depends(),
):
    # Refresh the insights and metrics
    review_insights = code_review_insights.refresh_insights()
    explainability_insights = code_explainability_insights.refresh_insights()
    quality_insights = code_quality_insights.refresh_insights()
    security_audit = code_security_audit.refresh_audit()
    compliance_insights = code_compliance_insights.refresh_insights()
    recommendation = code_recommendation.refresh_recommendation()
    refactoring_suggestions = code_refactoring_suggestions.refresh_suggestions()
    similarity = code_similarity.refresh_similarity()
    clone_detection = code_clone_detection.refresh_detection()

    # Cache the refreshed insights and metrics
    cache.set("code_intelligence_dashboard", {
        "review_insights": review_insights,
        "explainability_insights": explainability_insights,
        "quality_insights": quality_insights,
        "security_audit": security_audit,
        "compliance_insights": compliance_insights,
        "recommendation": recommendation,
        "refactoring_suggestions": refactoring_suggestions,
        "similarity": similarity,
        "clone_detection": clone_detection,
    })

    # Return the cached insights and metrics
    return JSONResponse(content=cache.get("code_intelligence_dashboard"), media_type="application/json")