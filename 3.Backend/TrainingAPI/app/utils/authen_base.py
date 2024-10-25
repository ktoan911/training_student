from pydantic import BaseModel

class AuthenBase(BaseModel):
    username: str
    password: str