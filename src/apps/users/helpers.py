import bcrypt


async def hash_password(password: str):
    pasword_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(pasword_bytes, salt=bcrypt.gensalt(rounds=15))
    return hashed_password

async def verify_hashed_password(password: str, hashed_password: bytes) -> bool:
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        return True
    return False