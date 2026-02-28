from .auth_models import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    UUID, ForeignKey, 
    DateTime, func,
    String
)

import uuid
from datetime import datetime
import enum

class UserRole(enum.Enum):
    USER = "USER"
    AI = 'AI'

class Message(Base):
    __tablename__ = 'messages'

    message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                                primary_key=True, index=True, unique=True, default=uuid.uuid4)
    
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user_account.user_id"))

    user_role: Mapped[str] = mapped_column(String, nullable=False, index=True, default=UserRole.USER.value)

    message: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), 
        nullable=False)
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), 
        nullable=False, onupdate=func.now())

    owner = relationship("User", back_populates="message")


    def __repr__(self) -> str:
        return f"Message(message_id={self.message_id}, user_id={self.user_id}, user_role={self.user_role}, message={self.message}, created_at={self.created_at}, updated_at={self.updated_at})"
    
