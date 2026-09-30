from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import Session

from app.core.security import criar_token, hash_senha, verificar_senha
from app.dependencies import get_db
from app.models import Usuario
from app.schemas import CriarUsuario, Login

router = APIRouter(tags=["Autenticação"])


@router.post("/login/")
def login(credenciais: Login, db: Session = Depends(get_db)):
    try:
        usuario_login = db.query(Usuario).filter(Usuario.email == credenciais.email).first()

        if usuario_login is None or not verificar_senha(
            credenciais.senha, usuario_login.senha
        ):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        token = criar_token(
            {
                "role": usuario_login.role,
                "sub": usuario_login.email,
                "id": usuario_login.id,
            }
        )
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Erro ao consultar o banco de dados"
        )


@router.post("/cadastro/", status_code=201)
def criar_usuario(usuarios: CriarUsuario, db: Session = Depends(get_db)):
    try:
        cadastrar = Usuario(
            name=usuarios.name,
            email=usuarios.email,
            senha=hash_senha(usuarios.senha),
        )
        db.add(cadastrar)
        db.commit()
        return {"mensagem": "Usuário criado com sucesso"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    except HTTPException:
        raise
    except OperationalError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Erro ao criar usuário no banco de dados"
        )