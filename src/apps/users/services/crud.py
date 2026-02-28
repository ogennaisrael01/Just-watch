
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from src.apps.users.models.message_model import Message


async def save_message(current_user, message, user_role, db: AsyncSession):
    message_instance = Message(
        user_id=current_user.user_id, 
        user_role=user_role, message=message
        )
    db.add(message)
    await db.commit()
    await db.refresh(message_instance)
    return message_instance

async def retreive_messages(current_user, db: AsyncSession):
    stmt = select(Message).where((Message.user_id == current_user.user_id))
    query = await db.execute(stmt)

    # fetch only the latest 10 messages
    result = query.scalars().fetchall()[:10]

    if result is None:
        return False
    return result

async def delete_chat_history(current_user, message_id: int | None, db):
    if message_id is None:
        stmt = delete(Message).where((Message.user_id == current_user.user_id))
    else:
        stmt = delete(Message).where(
            (Message.user_id == current_user.user_id), (Message.message_id == message_id)
        )

    query = await db.execute(stmt)
    await db.commit()
    if query.rowcount == 0:
        return False
    return query.rowcount
