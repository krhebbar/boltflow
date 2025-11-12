"""Playwright-based web scraper"""
from playwright.async_api import async_playwright, Browser
from typing import Callable, Optional, Dict, Any

class PlaywrightScraper:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.browser: Optional[Browser] = None
    
    async def scrape(
        self,
        url: str,
        max_pages: int = 50,
        include_assets: bool = True,
        screenshot: bool = True,
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Scrape website with Playwright"""
        
        async with async_playwright() as p:
            self.browser = await p.chromium.launch(headless=True)
            page = await self.browser.new_page()
            
            # Navigate to URL
            await page.goto(url, wait_until='networkidle')
            
            # Extract HTML/CSS
            html = await page.content()
            
            # Take screenshot if requested
            screenshot_path = None
            if screenshot:
                screenshot_path = f"scraped/{self.job_id}/screenshot.png"
                await page.screenshot(path=screenshot_path, full_page=True)
            
            # Extract all links for crawling
            links = await page.evaluate("""
                () => Array.from(document.querySelectorAll('a')).map(a => a.href)
            """)
            
            # Report progress
            if progress_callback:
                await progress_callback({
                    "pages_scraped": 1,
                    "total_pages": min(len(links), max_pages),
                    "current_url": url
                })
            
            await self.browser.close()
            
            return {
                "url": url,
                "html": html,
                "links": links[:max_pages],
                "screenshot": screenshot_path,
                "assets": [] if include_assets else None
            }
