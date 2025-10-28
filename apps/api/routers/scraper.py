"""
Scraper Router - Web scraping endpoints
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uuid

from lib.websocket_manager import ws_manager
from scrapers.playwright_scraper import PlaywrightScraper

router = APIRouter()

class ScrapeRequest(BaseModel):
    url: HttpUrl
    max_pages: Optional[int] = 50
    include_assets: bool = True
    screenshot: bool = True

class ScrapeResponse(BaseModel):
    job_id: str
    status: str
    message: str

@router.post("/start", response_model=ScrapeResponse)
async def start_scrape(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """
    Start web scraping job

    - **url**: Target website URL
    - **max_pages**: Maximum pages to scrape
    - **include_assets**: Download images, fonts, etc.
    - **screenshot**: Capture page screenshots
    """
    job_id = str(uuid.uuid4())

    # Start scraping in background
    background_tasks.add_task(
        run_scraper,
        job_id=job_id,
        url=str(request.url),
        max_pages=request.max_pages,
        include_assets=request.include_assets,
        screenshot=request.screenshot
    )

    return ScrapeResponse(
        job_id=job_id,
        status="started",
        message=f"Scraping job started for {request.url}"
    )

@router.get("/status/{job_id}")
async def get_scrape_status(job_id: str):
    """Get scraping job status"""
    # TODO: Implement job status tracking
    return {
        "job_id": job_id,
        "status": "in_progress",
        "pages_scraped": 0,
        "total_pages": 0,
        "progress_percentage": 0
    }

async def run_scraper(job_id: str, url: str, max_pages: int, include_assets: bool, screenshot: bool):
    """Background task to run scraper"""
    try:
        scraper = PlaywrightScraper(job_id)

        # Send initial status
        await ws_manager.broadcast({
            "type": "scrape:started",
            "job_id": job_id,
            "url": url
        })

        # Run scraping with progress callbacks
        result = await scraper.scrape(
            url=url,
            max_pages=max_pages,
            include_assets=include_assets,
            screenshot=screenshot,
            progress_callback=lambda p: ws_manager.broadcast({
                "type": "scrape:progress",
                "job_id": job_id,
                "progress": p
            })
        )

        # Send completion status
        await ws_manager.broadcast({
            "type": "scrape:completed",
            "job_id": job_id,
            "result": result
        })

    except Exception as e:
        await ws_manager.broadcast({
            "type": "scrape:error",
            "job_id": job_id,
            "error": str(e)
        })
