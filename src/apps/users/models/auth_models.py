from sqlalchemy import (
    Column, Integer, 
    String, LargeBinary
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.config.database import Base

import uuid
from datetime import datetime

class User(Base):

    __tablename__ = "user_account"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),  default=uuid.uuid4, primary_key=True, unique=True, index=True)
    email: Mapped[str] = mapped_column(String(), index=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(), index=True, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(), index=True)
    last_name: Mapped[str] = mapped_column(String(), index=True)
    password: Mapped[bytes] = mapped_column(LargeBinary(), nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.utcnow)

    movies_search = relationship("MovieSearch", cascade="all, delete", back_populates="owner")
    watchlist = relationship("WatchList", cascade="all, delete", back_populates="owner")
    def __repr__(self):
        return f"User(user_id={self.user_id}, email={self.email}, username={self.username}, first_name={self.first_name}, last_name={self.last_name}, created_at={self.created_at})"
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
