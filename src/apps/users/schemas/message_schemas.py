from pydantic import BaseModel

import uuid
from datetime import datetime

class MessageIn(BaseModel):
    message: str

class MessageOut(BaseModel):
    message_id: uuid.UUID
    message: str
    user_id: uuid.UUID
    user_role: str
    created_at: datetime
    updated_at: datetime
