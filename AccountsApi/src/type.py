from pydantic import BaseModel, Field
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"

class Account(BaseModel):
    username: str = Field(min_length=3, max_length=111, pattern=r'^\w+$')
    password: str = Field(min_length=5, max_length=111, pattern=r'^[\w!?$-]+$')


class AccountStat(BaseModel):
    username: str = Field(min_length=3, max_length=111, pattern=r'^\w+$')
    points: int = Field(ge=0)

class AccountDB(BaseModel):
    role: Role = Role.USER
    password: str
    refresh_token: str
    expires: str