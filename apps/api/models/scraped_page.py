"""Scraped page model"""
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from .base import Base


class ScrapedPage(Base):
    __tablename__ = "scraped_pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False, index=True)
    url = Column(String, nullable=False)
    html = Column(Text)
    css = Column(Text)
    screenshot = Column(Text)
    metadata = Column(JSONB)
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    job = relationship("Job", back_populates="scraped_pages")

    def __repr__(self):
        return f"<ScrapedPage {self.url}>"
