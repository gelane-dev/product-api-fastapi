from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import ALGORITHM, SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash_salvo: str) -> bool:
    return pwd_context.verify(senha, hash_salvo)


def criar_token(dados: dict) -> str:
    payload = dados.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=60)
    return jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> dict:
    return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])