"""AI DOM Analyzer using OpenAI GPT-4"""
import os
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

class DOMAnalyzer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def analyze(self, html: str, css: Optional[str] = None) -> Dict[str, Any]:
        """Analyze HTML structure with GPT-4"""
        
        prompt = f"""
        Analyze this HTML and identify:
        1. Page type (static/template/dynamic)
        2. Main sections (header, hero, features, footer, etc.)
        3. Complexity score (0-100)
        
        HTML:
        {html[:2000]}  # Truncate for token limits
        
        Return JSON format:
        {{
            "page_type": "static|template|dynamic",
            "sections": [
                {{"type": "header", "html": "...", "complexity": 0-100}}
            ],
            "overall_complexity": 0-100
        }}
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert web analyzer."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        # Parse JSON response
        import json
        result = json.loads(response.choices[0].message.content)
        return result
