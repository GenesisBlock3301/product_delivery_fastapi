from typing import Optional
from pydantic import BaseModel


class SignupModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "username": "sifat",
                "email": "nas@gmail.com",
                "password": "pass",
                "is_staff": False,
                "is_active": True
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = "7ce94a8d58477f88d79af4e76dc591884db8a98fe1eb750b9b9beae5370c785d"

class LoginModel(BaseModel):
    username:str
    password:str
