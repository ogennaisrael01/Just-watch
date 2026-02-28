from src.config.database.base import Base

from sqlalchemy import (
    Integer, String, ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime
from typing import List

class MovieSearch(Base):

    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(Integer(), primary_key=True, unique=True, index=True) 
    movie_title: Mapped[str] = mapped_column(String(), nullable=True, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.user_id"))
    release_date: Mapped[str] = mapped_column(String(), nullable=True, index=True) 
    gerne_ids: Mapped[list] = mapped_column(List(), nullable=False, index=True)

    poster_path: Mapped[str] = mapped_column(String(), nullable=True, index=True)

    saved_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    owner = relationship("User", back_populates="movies_search")


class WatchList(Base):
    __tablename__ = "watchlist"

    watchlist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, 
             unique=True, index=True)
    
    movie_id: Mapped[int] = mapped_column(Integer(), unique=True, index=True)
    owner_id: Mapped[uuid.UUID]= mapped_column(ForeignKey("user_account.user_id"), index=True)

    owner = relationship("User", back_populates="watchlist")

    added_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self):
        return f"WatchList(watchlist_id={self.watchlist_id}, movie_id={self.movie_id}, owner_id={self.owner_id}, added_at={self.added_at})"

class Rate(Base):
    __tablename__ = "rating"

    rating_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True, unique=True
    )
    movie_id: Mapped[int] = mapped_column(Integer(), unique=True, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.user_id"), index=True)

    owner = relationship("User", back_populates="ratings")
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    score: Mapped[int] = mapped_column(Integer(), nullable=False)

    def __repr__(self):
        return f"Rate(rating_id={self.rating_id}, movie_id={self.movie_id}, owner_id={self.owner_id}, score={self.score}, created_at={self.created_at})"
    
    @validates("score")
    def validate_score(self, key, value):
        if value < 1 or value > 10:
            raise ValueError("Score can only be between 1 and 10")
        return value
    
