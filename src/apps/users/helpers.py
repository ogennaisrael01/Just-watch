import bcrypt


async def hash_password(password: str):
    hashed_password = bcrypt.hashpw(password, salt=bcrypt.gensalt(rounds=15))
    return hashed_password

async def verify_hashed_password(password: str, hashed_password: bytes) -> bool:
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False
    