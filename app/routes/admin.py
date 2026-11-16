import re
import unicodedata
from typing import Optional
from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models import Product
from app.config import settings
from app.auth import (
    verify_credentials,
    create_session_token,
    get_current_admin,
    require_admin,
    SESSION_COOKIE_NAME,
    SESSION_MAX_AGE
)

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory="app/templates")


def slugify(text: str) -> str:
    """Gera um slug limpo e seguro para URLs a partir de um texto."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)


# =====================================================================
# AUTENTICAÇÃO
# =====================================================================

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, next: Optional[str] = "/admin"):
    """Exibe o formulário de login para o painel administrativo."""
    if get_current_admin(request):
        return RedirectResponse(url=next or "/admin", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={
            "next": next or "/admin",
            "error": None,
            "app_name": settings.APP_NAME
        }
    )


@router.post("/login", response_class=HTMLResponse)
async def process_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next: Optional[str] = Form("/admin")
):
    """Processa a autenticação do administrador e define o cookie de sessão seguro."""
    if verify_credentials(username, password):
        token = create_session_token(username)
        redirect_url = next if (next and next.startswith("/admin")) else "/admin"
        response = RedirectResponse(url=redirect_url, status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=token,
            max_age=SESSION_MAX_AGE,
            httponly=True,
            samesite="lax",
            secure=False
        )
        return response
    
    return templates.TemplateResponse(
        request=request,
        name="admin/login.html",
        context={
            "next": next or "/admin",
            "error": "Usuário ou senha inválidos. Verifique as credenciais no seu arquivo .env.",
            "app_name": settings.APP_NAME
        },
        status_code=status.HTTP_401_UNAUTHORIZED
    )


@router.get("/logout")
async def logout():
    """Encerra a sessão do administrador removendo o cookie."""
    response = RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return response


# =====================================================================
# DASHBOARD E CRUD
# =====================================================================

@router.get("", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """
    Dashboard administrativo com métricas e listagem de produtos.
    """
    products = db.query(Product).order_by(Product.created_at.desc()).all()
    
    total_products = len(products)
    active_products = sum(1 for p in products if p.is_active)
    total_clicks = db.query(func.sum(Product.clicks_count)).scalar() or 0
    top_products = db.query(Product).order_by(Product.clicks_count.desc()).limit(5).all()

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "admin_user": admin_user,
            "products": products,
            "total_products": total_products,
            "active_products": active_products,
            "total_clicks": total_clicks,
            "top_products": top_products,
            "app_name": settings.APP_NAME,
            "app_url": settings.APP_URL
        }
    )


@router.get("/produtos/novo", response_class=HTMLResponse)
async def new_product_form(
    request: Request,
    admin_user: str = Depends(require_admin)
):
    """Formulário para adicionar um novo produto."""
    return templates.TemplateResponse(
        request=request,
        name="admin/product_form.html",
        context={
            "admin_user": admin_user,
            "product": None,
            "action_url": "/admin/produtos/novo",
            "page_title": "Cadastrar Novo Produto",
            "app_name": settings.APP_NAME
        }
    )


@router.post("/produtos/novo")
async def create_product(
    request: Request,
    title: str = Form(...),
    slug: Optional[str] = Form(None),
    category: str = Form(...),
    image_url: str = Form(...),
    old_price: Optional[float] = Form(None),
    current_price: float = Form(...),
    installments: Optional[str] = Form(None),
    badge: Optional[str] = Form(None),
    affiliate_url: str = Form(...),
    description: Optional[str] = Form(None),
    is_active: bool = Form(True),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Cria e salva um novo produto no banco de dados."""
    final_slug = slugify(slug) if (slug and slug.strip()) else slugify(title)
    
    existing = db.query(Product).filter(Product.slug == final_slug).first()
    counter = 1
    base_slug = final_slug
    while existing:
        final_slug = f"{base_slug}-{counter}"
        existing = db.query(Product).filter(Product.slug == final_slug).first()
        counter += 1

    new_prod = Product(
        title=title.strip(),
        slug=final_slug,
        category=category.strip(),
        image_url=image_url.strip(),
        old_price=old_price if (old_price and old_price > 0) else None,
        current_price=current_price,
        installments=installments.strip() if installments else None,
        badge=badge.strip() if badge else None,
        affiliate_url=affiliate_url.strip(),
        description=description.strip() if description else None,
        is_active=is_active,
        clicks_count=0
    )
    db.add(new_prod)
    db.commit()
    
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/produtos/editar/{product_id}", response_class=HTMLResponse)
async def edit_product_form(
    product_id: int,
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Formulário para editar um produto existente."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return templates.TemplateResponse(
        request=request,
        name="admin/product_form.html",
        context={
            "admin_user": admin_user,
            "product": product,
            "action_url": f"/admin/produtos/editar/{product_id}",
            "page_title": f"Editar: {product.title[:40]}...",
            "app_name": settings.APP_NAME
        }
    )


@router.post("/produtos/editar/{product_id}")
async def update_product(
    product_id: int,
    request: Request,
    title: str = Form(...),
    slug: str = Form(...),
    category: str = Form(...),
    image_url: str = Form(...),
    old_price: Optional[float] = Form(None),
    current_price: float = Form(...),
    installments: Optional[str] = Form(None),
    badge: Optional[str] = Form(None),
    affiliate_url: str = Form(...),
    description: Optional[str] = Form(None),
    is_active: bool = Form(False),
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Atualiza as informações de um produto existente."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    final_slug = slugify(slug) if slug.strip() else slugify(title)
    conflict = db.query(Product).filter(Product.slug == final_slug, Product.id != product_id).first()
    if conflict:
        final_slug = f"{final_slug}-{product_id}"

    product.title = title.strip()
    product.slug = final_slug
    product.category = category.strip()
    product.image_url = image_url.strip()
    product.old_price = old_price if (old_price and old_price > 0) else None
    product.current_price = current_price
    product.installments = installments.strip() if installments else None
    product.badge = badge.strip() if badge else None
    product.affiliate_url = affiliate_url.strip()
    product.description = description.strip() if description else None
    product.is_active = is_active
    
    db.commit()
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/produtos/toggle/{product_id}")
async def toggle_product_active(
    product_id: int,
    request: Request,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Alterna o status do produto entre ativo e inativo com 1 clique."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    product.is_active = not product.is_active
    db.commit()
    
    if request.headers.get("accept") == "application/json":
        return JSONResponse({"success": True, "is_active": product.is_active})
    
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/produtos/deletar/{product_id}")
async def delete_product(
    product_id: int,
    admin_user: str = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Remove um produto do catálogo."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    
    return RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
