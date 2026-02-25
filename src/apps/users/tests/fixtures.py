from httpx import ASGITransport, AsyncClient

import pytest


from src.manage import app

@pytest.fixture
async def client_fixture():
    async with AsyncClient(
        transport=ASGITransport(app=app)
    ) as client:
        return client