import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.database import init_db, SessionLocal
from app.seed import seed_database
from app.routes.public import router as public_router
from app.routes.admin import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerenciador de ciclo de vida da aplicação:
    Executa a criação das tabelas e o seed inicial dos produtos na inicialização.
    """
    print(f"[*] Inicializando {settings.APP_NAME}...")
    init_db()
    
    # Executa o seed inicial de produtos se o banco estiver vazio
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
        
    print(f"[OK] {settings.APP_NAME} pronto para receber conexões em {settings.APP_URL}")
    yield
    print(f"[*] Encerrando {settings.APP_NAME}...")


# Instanciação da aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="Vitrine de Produtos Afiliados (Mercado Livre) - Nicho: Ferramentas & Eletrônicos",
    version="1.0.0",
    lifespan=lifespan
)

# Monta diretório de arquivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), "app", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Rota direta para favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(static_dir, "img", "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    return HTMLResponse(status_code=204)

# Inclusão de rotas
app.include_router(public_router)
app.include_router(admin_router)

# Configuração de templates
templates = Jinja2Templates(directory="app/templates")


# Tratamento personalizado de página não encontrada (404)
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        context={
            "app_name": settings.APP_NAME,
            "telegram_url": settings.TELEGRAM_VIP_URL,
            "whatsapp_url": settings.WHATSAPP_VIP_URL,
            "slug": None
        },
        status_code=404
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
