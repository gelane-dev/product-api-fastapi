from collections.abc import Generator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decodificar_token

oauth2_scheme = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def obter_usuario_atual(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> dict:
    try:
        return decodificar_token(token.credentials)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


def exigir_admin(usuario: dict = Depends(obter_usuario_atual)) -> dict:
    if usuario["role"] == "admin":
        return usuario
    raise HTTPException(status_code=403, detail="Acesso restrito a administradores")