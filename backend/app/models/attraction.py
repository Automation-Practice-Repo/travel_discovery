import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, Table, Column, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# Many-to-many relationship mapping between SearchQuery and Attraction
search_query_association = Table(
    "search_query_association",
    Base.metadata,
    Column("search_query_id", ForeignKey("search_queries.id", ondelete="CASCADE"), primary_key=True),
    Column("attraction_place_id", ForeignKey("attractions.place_id", ondelete="CASCADE"), primary_key=True),
)

class SearchQuery(Base):
    __tablename__ = "search_queries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    location_name: Mapped[str] = mapped_column(String(255), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    radius_km: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    attractions: Mapped[List["Attraction"]] = relationship(
        secondary=search_query_association,
        back_populates="search_queries"
    )

class Attraction(Base):
    __tablename__ = "attractions"

    place_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    user_ratings_total: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    opening_hours: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    search_queries: Mapped[List[SearchQuery]] = relationship(
        secondary=search_query_association,
        back_populates="attractions"
    )
