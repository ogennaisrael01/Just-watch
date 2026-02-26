from src.config.database.base import Base

from sqlalchemy import (
    Integer, String, ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from datetime import datetime

class MovieSearch(Base):

    __tablename__ = "movies"

    movie_id: Mapped[int] = mapped_column(Integer(), primary_key=True, unique=True, index=True) 
    movie_title: Mapped[str] = mapped_column(String(), nullable=True, index=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.user_id"))
    release_date: Mapped[str] = mapped_column(String(), nullable=True, index=True) 

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
