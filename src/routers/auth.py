from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from database import get_session
from models.usuario import UsuarioLogin, UsuarioResponse, UsuarioDB
from repositories.usuario import get_usuario_by_email
from security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginResponse(UsuarioResponse):
    access_token: str

@router.post("/login", response_model=LoginResponse)
def login(payload: UsuarioLogin, session: Session = Depends(get_session)) -> LoginResponse:
    user: UsuarioDB | None = get_usuario_by_email(session, payload.email)
    if not user or not verify_password(payload.senha, user.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Usuário inválido: id ausente",
        )

    token = create_access_token(subject=user.id)
    return LoginResponse(
        id=user.id,
        nome=user.nome,
        email=user.email,
        funcao=user.funcao,
        biografia=user.biografia,
        access_token=token,
    )


