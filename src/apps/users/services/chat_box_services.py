from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache
from src.config.settings import base_setting

from sqlalchemy.ext.asyncio import AsyncSession

from google import genai

from .crud import (
    save_message, retreive_messages, 
    delete_chat_history
)
from ..models.message_model import UserRole

class ChatBoxService:
    API_KEY = getattr(base_setting, "GEMINI_API_KEY")
    GEMINI_MODEL = getattr(base_setting, "GEMINI_MODEL")

    def __init__(self, current_user, db: AsyncSession):
        self.current_user = current_user
        self.db = db

    @classmethod
    async def  Verify_gemini_credentials(cls) -> tuple[str]:
        if cls.API_KEY is None:
            raise ValueError("API KEY Cannot be empty")
        
        if cls.GEMINI_MODEL is None:
            raise ValueError('Please provide the gemini model.')
        
        return cls.API_KEY, cls.GEMINI_MODEL
    
    async def save_user_chat_in_db(self, message: str):
        """ Save user chat in history for flow conversation."""
        user, db = self.current_user, self.db

        new_message = await save_message(
            current_user=user, message=message,
            user_role=UserRole.USER.value, db=db
        )
        return new_message
    
    async def save_ai_response_in_db(self, message: str):
        user, db = self.current_user, self.db

        new_message = await save_message(
            current_user=user, message=message,
            user_role=UserRole.AI.value, db=db
        )
        return new_message
    

    @cache(expire=60)
    async def list_chat_history(self):
        user, db = self.current_user, self.db
        chat_history = await retreive_messages(current_user=user, db=db)
        return jsonable_encoder(chat_history)
    
    
    async def clear_chat_history(self, message_id: int | None):
        user, db = self.current_user, self.db
        deleted_rows = await delete_chat_history(
            current_user=user,
            message_id=message_id,
            db=db
        )

        if not deleted_rows:
            return 0
        return deleted_rows
    
    async def history_for_gemini(self):
        history = []
        roles_and_parts = {
            "role": str,
            "parts": list
        }
        for data in await self.list_chat_history():
            if data['user_role'] == UserRole.USER.value:
                roles_and_parts["role"] = "user"
                roles_and_parts['parts'].append({"texts": data["message"]})
            else:
                roles_and_parts["role"] == "model"
                roles_and_parts['parts'].append({"texts": data["message"]})
            
            history.append(roles_and_parts)
        print("MessageHistory", history)
        return history
    
    async def chat_ai(self, message: str):
        api_key, model = await ChatBoxService.Verify_gemini_credentials()

        history = await self.history_for_gemini()
        try:
            client = genai.Client(api_key=api_key)

            chats = client.aio.chats.create(model=model, history=history)
            response = await chats.send_message(message=message)
    
        except Exception as e:
            raise ValueError(f"Error While generating chat: {str(e)}")

        ai_response = response.text
        print(ai_response)
        await self.save_ai_response_in_db(ai_response)
        await self.save_user_chat_in_db(message)

        return ai_response.strip()
    







        


    







