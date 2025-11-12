"""Generated component model"""
from sqlalchemy import Column, String, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from .base import Base, TimestampMixin


class GeneratedComponent(Base, TimestampMixin):
    __tablename__ = "generated_components"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False, index=True)
    component_type = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    # Relationships
    job = relationship("Job", back_populates="generated_components")

    def __repr__(self):
        return f"<GeneratedComponent {self.filename}>"
