"""Component Classifier using embeddings"""
from typing import List, Dict, Any
from openai import AsyncOpenAI
import os

class ComponentClassifier:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def classify(self, sections: List[Dict]) -> List[Dict]:
        """Classify components and calculate similarity"""
        
        classified = []
        for section in sections:
            # Get embedding for semantic similarity
            embedding = await self.get_embedding(section['html'])
            
            # Match against pattern library
            pattern = await self.match_pattern(embedding)
            
            classified.append({
                "type": section['type'],
                "confidence": 0.85,  # Mock confidence
                "html": section['html'],
                "styles": {},
                "complexity_score": section.get('complexity', 50),
                "matched_pattern": pattern
            })
        
        return classified
    
    async def get_embedding(self, text: str) -> List[float]:
        """Get text embedding for similarity search"""
        response = await self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text[:1000]  # Truncate
        )
        return response.data[0].embedding
    
    async def match_pattern(self, embedding: List[float]) -> str:
        """Match to pattern library (mock implementation)"""
        # In production: Use vector database (Supabase pgvector)
        return "modern-hero"
