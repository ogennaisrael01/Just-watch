from fastapi.encoders import jsonable_encoder
from fastapi_cache.decorator import cache
from src.config.settings import base_setting

from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI

from .crud import (
    save_message, retreive_messages, 
    delete_chat_history
)
from ..models.message_model import UserRole
from .security import retry_on_failure

class ChatBoxService:
    API_KEY = getattr(base_setting, "TOKEN_MIX_API_KEY")
    MODEL = getattr(base_setting, "TOKEN_MIX_MODEL")

    def __init__(self, current_user, db: AsyncSession):
        self.current_user = current_user
        self.db = db

    @classmethod
    async def  Verify_gemini_credentials(cls) -> tuple[str, str]:
        if cls.API_KEY is None:
            raise ValueError("API KEY Cannot be empty")
        
        if cls.MODEL is None:
            raise ValueError('Please provide the gemini model.')
        
        return cls.API_KEY, cls.MODEL
    
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
    
    async def history_for_AI(self):
        history = []
        roles_and_contents = {
            "role": str, 'content': str
        }
        for data in await self.list_chat_history():
            if data['user_role'] == UserRole.USER.value:
                roles_and_contents["role"] = "user"
                roles_and_contents['content'] = data["message"]
            if data['user_role'] == UserRole.AI.value:
                roles_and_contents["role"] == "system"
                roles_and_contents["content"] = data['message']
            
            history.append(roles_and_contents)
        return history
    
    # @retry_on_failure
    from fastapi import BackgroundTasks

    async def chat_ai(self, message: str, background_tasks: BackgroundTasks):
        await self.save_user_chat_in_db(message=message)
        api_key, model = await ChatBoxService.Verify_gemini_credentials()

        history = await self.history_for_AI()
        history.append({"role": "user", "content": message})

        full_ai_response = []

        try:
            client = AsyncOpenAI(api_key=api_key, base_url="https://api.tokenmix.ai/v1")
            response = await client.chat.completions.create(
                model=model,
                messages=history,
                stream=True,
                max_tokens=1024
            )

            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_ai_response.append(content)
                    yield content
        except Exception as e:
            yield f"\n[API Error: {str(e)}]"
        finally:
            final_text = "".join(full_ai_response)
            if final_text:
                background_tasks.add_task(self.save_ai_response_in_db, message=final_text)