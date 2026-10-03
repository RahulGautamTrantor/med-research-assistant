"""
FastAPI Server for Medical Research Assistant.
Exposes RESTful endpoints for case processing, paper summarization, and clinical guidelines.
Also mounts static files for browser-based dashboard interface.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from med_assistant import (
    CaseStudyProcessor,
    PaperSummarizer,
    GuidelineEngine,
    SAMPLE_CASES,
    SAMPLE_PAPERS,
    GUIDELINES_DATA
)

app = FastAPI(
    title="Medical Research Assistant API",
    description="Specialist Clinical Intelligence & Decision Support Platform for MD Medicine",
    version="1.0.0"
)

# CORS configuration for browser compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize engines
case_processor = CaseStudyProcessor()
paper_summarizer = PaperSummarizer()
guideline_engine = GuidelineEngine()

# Pydantic schemas
class CaseAnalysisRequest(BaseModel):
    case_text: str
    title: Optional[str] = None

class PaperSummarizeRequest(BaseModel):
    paper_text: str
    title: Optional[str] = None

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

# Static directory mounting
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
async def serve_index():
    index_path = STATIC_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Medical Research Assistant API Online. Browse /docs for Swagger UI."}

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Medical Research Assistant",
        "version": "1.0.0",
        "pyodide_ready": True
    }

@app.get("/api/samples")
async def get_samples():
    """Returns pre-loaded clinical vignettes, trial abstracts, and guideline summaries."""
    return {
        "cases": SAMPLE_CASES,
        "papers": SAMPLE_PAPERS,
        "guidelines": GUIDELINES_DATA
    }

@app.post("/api/case/analyze")
async def analyze_case(request: CaseAnalysisRequest):
    """Processes a complex patient case study and returns MD specialist differential & workup."""
    if not request.case_text or not request.case_text.strip():
        raise HTTPException(status_code=400, detail="case_text cannot be empty.")
    try:
        result = case_processor.analyze_case(request.case_text, request.title)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Case processing error: {str(e)}")

@app.post("/api/paper/summarize")
async def summarize_paper(request: PaperSummarizeRequest):
    """Summarizes a clinical research paper/abstract with PICO, statistics, and takeaways."""
    if not request.paper_text or not request.paper_text.strip():
        raise HTTPException(status_code=400, detail="paper_text cannot be empty.")
    try:
        result = paper_summarizer.summarize(request.paper_text, request.title)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Paper summarization error: {str(e)}")

@app.get("/api/guidelines")
async def get_guidelines(
    specialty: Optional[str] = Query(None, description="Filter by medical specialty"),
    query: Optional[str] = Query(None, description="Search term for drug, disease, or trial")
):
    """Retrieves guidelines filtered by specialty or search keywords."""
    if query:
        results = guideline_engine.search_guidelines(query)
        if specialty and specialty.lower() != "all":
            results = [r for r in results if specialty.lower() in r.get("specialty", "").lower()]
        return {"guidelines": results, "count": len(results)}
    elif specialty:
        results = guideline_engine.filter_by_specialty(specialty)
        return {"guidelines": results, "count": len(results)}
    else:
        results = guideline_engine.get_all_guidelines()
        return {"guidelines": results, "count": len(results)}

@app.get("/api/guidelines/specialties")
async def get_specialties():
    """Returns distinct list of medical specialties in database."""
    return {"specialties": guideline_engine.get_specialties()}

@app.get("/api/guidelines/{guideline_id}")
async def get_guideline_by_id(guideline_id: str):
    """Retrieves a specific guideline by identifier."""
    result = guideline_engine.get_guideline_by_id(guideline_id)
    if not result:
        raise HTTPException(status_code=404, detail="Guideline not found.")
    return result

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Medical Research Assistant on http://localhost:{port}")
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
