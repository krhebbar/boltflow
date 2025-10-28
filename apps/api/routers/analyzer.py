"""
Analyzer Router - AI-powered analysis endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from ai.analyzer import DOMAnalyzer
from ai.classifier import ComponentClassifier

router = APIRouter()

class AnalyzeRequest(BaseModel):
    job_id: str
    html: str
    css: Optional[str] = None

class ComponentPattern(BaseModel):
    type: str  # header, hero, features, footer, etc.
    confidence: float
    html: str
    styles: Dict[str, Any]
    complexity_score: float

class AnalysisResponse(BaseModel):
    job_id: str
    page_type: str  # static, template, dynamic
    components: List[ComponentPattern]
    complexity_score: float
    estimated_hours: float

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_page(request: AnalyzeRequest):
    """
    Analyze scraped HTML with AI

    - **job_id**: Scraping job ID
    - **html**: HTML content to analyze
    - **css**: Optional CSS styles
    """
    try:
        # Initialize AI analyzer
        analyzer = DOMAnalyzer()
        classifier = ComponentClassifier()

        # Analyze page structure
        page_analysis = await analyzer.analyze(request.html, request.css)

        # Classify components
        components = await classifier.classify(page_analysis['sections'])

        # Calculate complexity and pricing
        complexity = calculate_complexity(components)
        estimated_hours = estimate_effort(complexity, len(components))

        return AnalysisResponse(
            job_id=request.job_id,
            page_type=page_analysis['page_type'],
            components=components,
            complexity_score=complexity,
            estimated_hours=estimated_hours
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calculate_complexity(components: List[Dict]) -> float:
    """Calculate overall complexity score (0-100)"""
    # Factors: number of components, style variety, JS complexity
    base_score = len(components) * 5
    style_complexity = sum(c.get('style_entropy', 0) for c in components)
    return min(base_score + style_complexity, 100)

def estimate_effort(complexity: float, component_count: int) -> float:
    """Estimate development hours"""
    base_hours = 8  # Base setup time
    component_hours = component_count * 0.5  # 30 min per component
    complexity_factor = complexity / 100
    return base_hours + component_hours * (1 + complexity_factor)

@router.post("/quote")
async def get_quote(request: AnalyzeRequest):
    """Get real-time pricing quote"""
    analysis = await analyze_page(request)

    hourly_rate = 100  # $100/hour
    total_cost = analysis.estimated_hours * hourly_rate

    return {
        "job_id": request.job_id,
        "complexity_score": analysis.complexity_score,
        "estimated_hours": analysis.estimated_hours,
        "hourly_rate": hourly_rate,
        "total_cost": total_cost,
        "breakdown": {
            "setup": 8 * hourly_rate,
            "components": (analysis.estimated_hours - 8) * hourly_rate,
            "testing": 0  # Included
        }
    }
