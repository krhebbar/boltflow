"""
Scraper Router - Web scraping endpoints with database persistence
"""
from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import BaseModel, HttpUrl, validator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog

from models.user import User
from models.project import Project
from models.job import Job
from models.scraped_page import ScrapedPage
from config.database import get_db
from config.settings import settings
from lib.auth import get_current_user
from lib.websocket_manager import ws_manager
from lib.exceptions import NotFoundError, ValidationError
from scrapers.playwright_scraper import PlaywrightScraper

router = APIRouter()
logger = structlog.get_logger(__name__)


class ScrapeRequest(BaseModel):
    url: HttpUrl
    project_name: str
    max_pages: int | None = 50
    include_assets: bool = True
    screenshot: bool = True

    @validator('max_pages')
    def validate_max_pages(cls, v):
        if v and v > settings.max_pages_limit:
            raise ValidationError(
                f"max_pages cannot exceed {settings.max_pages_limit}",
                details={"field": "max_pages", "max": settings.max_pages_limit}
            )
        return v

    @validator('url')
    def validate_url_domain(cls, v):
        """Prevent scraping localhost/internal URLs"""
        if v.host in ['localhost', '127.0.0.1', '0.0.0.0']:
            raise ValidationError(
                "Cannot scrape localhost or internal URLs",
                details={"field": "url", "host": v.host}
            )
        return v


class ScrapeResponse(BaseModel):
    job_id: str
    project_id: str
    status: str
    message: str


@router.post("/start", response_model=ScrapeResponse)
async def start_scrape(
    request: ScrapeRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Start web scraping job

    - **url**: Target website URL
    - **project_name**: Name for this migration project
    - **max_pages**: Maximum pages to scrape (default: 50, max: 100)
    - **include_assets**: Download images, fonts, etc.
    - **screenshot**: Capture page screenshots

    Requires authentication.
    """
    logger.info(
        "scrape_request",
        user_id=str(current_user.id),
        url=str(request.url),
        max_pages=request.max_pages
    )

    # Create project
    project = Project(
        user_id=current_user.id,
        name=request.project_name,
        url=str(request.url),
        status="scraping",
        max_pages=request.max_pages
    )
    db.add(project)
    await db.flush()

    # Create scraping job
    job = Job(
        project_id=project.id,
        type="scrape",
        status="pending",
        progress=0
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    await db.refresh(project)

    # Start scraping in background
    background_tasks.add_task(
        run_scraper,
        job_id=str(job.id),
        project_id=str(project.id),
        url=str(request.url),
        max_pages=request.max_pages or 50,
        include_assets=request.include_assets,
        screenshot=request.screenshot
    )

    logger.info(
        "scrape_started",
        job_id=str(job.id),
        project_id=str(project.id),
        user_id=str(current_user.id)
    )

    return ScrapeResponse(
        job_id=str(job.id),
        project_id=str(project.id),
        status="started",
        message=f"Scraping job started for {request.url}"
    )


@router.get("/status/{job_id}")
async def get_scrape_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get scraping job status"""

    # Get job from database
    result = await db.execute(
        select(Job).where(Job.id == job_id)
    )
    job = result.scalar_one_or_none()

    if not job:
        raise NotFoundError("Job", job_id)

    # Verify user owns this job's project
    result = await db.execute(
        select(Project).where(Project.id == job.project_id)
    )
    project = result.scalar_one_or_none()

    if not project or project.user_id != current_user.id:
        raise NotFoundError("Job", job_id)

    # Count scraped pages
    result = await db.execute(
        select(ScrapedPage).where(ScrapedPage.job_id == job_id)
    )
    scraped_pages = result.scalars().all()

    return {
        "job_id": str(job.id),
        "status": job.status,
        "progress": job.progress,
        "pages_scraped": len(scraped_pages),
        "total_pages": project.max_pages,
        "progress_percentage": job.progress,
        "error": job.error
    }


async def run_scraper(
    job_id: str,
    project_id: str,
    url: str,
    max_pages: int,
    include_assets: bool,
    screenshot: bool
):
    """Background task to run scraper and save results to database"""
    from config.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        try:
            # Update job status to running
            result = await db.execute(select(Job).where(Job.id == job_id))
            job = result.scalar_one()
            job.status = "running"
            await db.commit()

            # Send initial WebSocket notification
            await ws_manager.broadcast({
                "type": "scrape:started",
                "job_id": job_id,
                "project_id": project_id,
                "url": url
            })

            logger.info("scraper_running", job_id=job_id, url=url)

            # Initialize scraper
            scraper = PlaywrightScraper(job_id)

            # Progress callback to update database and WebSocket
            async def progress_callback(progress_data):
                # Update job progress
                job.progress = progress_data.get("percentage", 0)
                await db.commit()

                # Broadcast progress
                await ws_manager.broadcast({
                    "type": "scrape:progress",
                    "job_id": job_id,
                    "project_id": project_id,
                    "progress": progress_data
                })

            # Run scraping
            result_data = await scraper.scrape(
                url=url,
                max_pages=max_pages,
                include_assets=include_assets,
                screenshot=screenshot,
                progress_callback=progress_callback
            )

            # Save scraped pages to database
            if "pages" in result_data:
                for page_data in result_data["pages"]:
                    scraped_page = ScrapedPage(
                        job_id=job.id,
                        url=page_data.get("url"),
                        html=page_data.get("html"),
                        css=page_data.get("css"),
                        screenshot=page_data.get("screenshot"),
                        metadata=page_data.get("metadata", {})
                    )
                    db.add(scraped_page)

            # Update job as completed
            job.status = "completed"
            job.progress = 100
            job.result = result_data

            # Update project status
            result = await db.execute(select(Project).where(Project.id == project_id))
            project = result.scalar_one()
            project.status = "scraped"

            await db.commit()

            logger.info(
                "scraper_completed",
                job_id=job_id,
                pages_scraped=len(result_data.get("pages", []))
            )

            # Send completion notification
            await ws_manager.broadcast({
                "type": "scrape:completed",
                "job_id": job_id,
                "project_id": project_id,
                "result": result_data
            })

        except Exception as e:
            logger.error("scraper_failed", job_id=job_id, error=str(e), exc_info=True)

            # Update job with error
            job.status = "failed"
            job.error = str(e)
            await db.commit()

            # Send error notification
            await ws_manager.broadcast({
                "type": "scrape:error",
                "job_id": job_id,
                "project_id": project_id,
                "error": str(e)
            })
