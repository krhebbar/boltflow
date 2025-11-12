"""Component pattern model for AI classification"""
from sqlalchemy import Column, String, Float, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base, TimestampMixin


class ComponentPattern(Base, TimestampMixin):
    __tablename__ = "component_patterns"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False, index=True)  # header, hero, footer, etc.
    html_sample = Column(Text)
    css_sample = Column(Text)
    embedding = Column(Text)  # JSON array of embeddings (will use pgvector later)
    confidence_threshold = Column(Float, default=0.8)

    def __repr__(self):
        return f"<ComponentPattern {self.type}>"
