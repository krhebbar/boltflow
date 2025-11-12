"""Project model"""
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending, scraping, analyzing, etc.
    max_pages = Column(Integer, default=50)

    # Relationships
    user = relationship("User", back_populates="projects")
    jobs = relationship("Job", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project {self.name} ({self.status})>"
