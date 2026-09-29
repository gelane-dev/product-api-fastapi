from pydantic import BaseModel, EmailStr, Field


class CriarUsuario(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=6)


class Login(BaseModel):
    email: EmailStr
    senha: str