"""
Módulo de Autenticação para o Painel Administrativo.
Utiliza cookies assinados criptograficamente via itsdangerous.
"""
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.config import settings

# Serializador com a chave secreta da aplicação
serializer = URLSafeTimedSerializer(settings.SECRET_KEY, salt="pinhatech-admin-salt")

SESSION_COOKIE_NAME = "pinhatech_admin_session"
SESSION_MAX_AGE = 60 * 60 * 24 * 7  # 7 dias em segundos


def verify_credentials(username: str, password: str) -> bool:
    """Valida as credenciais comparando com o .env."""
    return (
        username.strip() == settings.ADMIN_USERNAME.strip() and
        password == settings.ADMIN_PASSWORD
    )


def create_session_token(username: str) -> str:
    """Gera um token criptografado para o cookie de sessão."""
    return serializer.dumps({"user": username})


def get_current_admin(request: Request) -> Optional[str]:
    """Lê e valida o token do cookie de sessão. Retorna o username ou None."""
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    try:
        data = serializer.loads(token, max_age=SESSION_MAX_AGE)
        return data.get("user")
    except (BadSignature, SignatureExpired):
        return None


def require_admin(request: Request):
    """
    Dependency para proteger rotas administrativas.
    Se o usuário não estiver autenticado, redireciona para a página de login.
    """
    admin_user = get_current_admin(request)
    if not admin_user:
        # Se for uma rota que renderiza página, redireciona para /admin/login
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            headers={"Location": f"/admin/login?next={request.url.path}"}
        )
    return admin_user
