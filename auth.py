from passlib.context import CryptContext
from jose import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
  )

def hash_senha(senha:str):

  senha = pwd_context.hash(senha)
  return senha


def verificar_senha(senha:str, hash_salvo: str):

  verificar = pwd_context.verify(senha, hash_salvo)
  return verificar

def criar_token(dados:dict):

    expiracao = datetime.now() + timedelta(minutes=60)
    dados["exp"] = expiracao
    token = jwt.encode(dados,key=os.getenv("SECRET_KEY"),algorithm="HS256")
    return token