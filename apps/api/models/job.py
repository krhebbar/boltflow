"""Job model"""
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import uuid
from .base import Base, TimestampMixin


class Job(Base, TimestampMixin):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False, index=True)
    type = Column(String, nullable=False)  # scrape, analyze, generate, deploy
    status = Column(String, nullable=False, default="pending", index=True)  # pending, running, completed, failed
    progress = Column(Integer, default=0)
    result = Column(JSONB)
    error = Column(Text)
    completed_at = Column(DateTime)

    # Relationships
    project = relationship("Project", back_populates="jobs")
    scraped_pages = relationship("ScrapedPage", back_populates="job", cascade="all, delete-orphan")
    generated_components = relationship("GeneratedComponent", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Job {self.type} ({self.status})>"
