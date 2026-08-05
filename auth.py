import os
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def obter_usuario_atual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

def exigir_admin(usuario: dict = Depends(obter_usuario_atual)):
    if usuario["role"] == "admin":
      return usuario
    else:
      raise HTTPException(status_code=403, detail="Token inválido ou expirado")