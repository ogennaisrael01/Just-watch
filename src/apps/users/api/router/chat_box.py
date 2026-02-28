from fastapi import APIRouter, status, Depends, HTTPException, Body, Request, Query

from .route_v1 import limiter, cache, UserService, User, get_db
from src.apps.users.schemas.message_schemas import MessageIn
from src.apps.users.services.chat_box_services import ChatBoxService

from sqlalchemy.ext.asyncio import AsyncSession
import uuid

router = APIRouter(
    prefix='/v1/ai', tags=["Chat-Box"]
)


@router.post("/chat-box/", status_code=status.HTTP_200_OK)
@limiter.limit('5/hour')
async def ai_chat_box(
    request: Request,
    current_user: User = Depends(UserService.get_current_user),
    message_data: MessageIn = Body(description="Message body"),
    db: AsyncSession = Depends(get_db)
):
    
    message_dict = message_data.model_dump()
    message = message_dict["message"]
    try:
        message_instance = ChatBoxService(
            current_user=current_user, 
            db=db
        )

        response_ai = await message_instance.chat_ai(message=message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {
        "status": "success",
        "result": response_ai
    }


@router.get("/chat-box/chats/", status_code=status.HTTP_200_OK)
@limiter.limit('10/minute')
@cache(expire=60 * 5)
async def ai_chat_box(
    request: Request,
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        message_instance = ChatBoxService(
            current_user=current_user, 
            db=db
        )

        response = await message_instance.list_chat_history()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {
        "status": "success",
        "result": response
    }


@router.delete("/chat-box/chats/", status_code=status.HTTP_200_OK)
async def ai_chat_box(
    message_id: uuid.UUID | None = Query(...),
    current_user: User = Depends(UserService.get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        message_instance = ChatBoxService(
            current_user=current_user, 
            db=db
        )

        result = await message_instance.clear_chat_history(message_id=message_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return {
        "status": "success",
        "deleted_row(s)": result
    }
