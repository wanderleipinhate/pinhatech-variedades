from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models import Product
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Categorias predefinidas para os filtros rápidos
PRESET_CATEGORIES = [
    "Todos",
    "Ferramentas",
    "Eletrônicos",
    "Casa Inteligente",
    "Ofertas Relâmpago"
]


@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    q: Optional[str] = None,
    categoria: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Vitrine Principal de Produtos Afiliados.
    Suporta busca em tempo real e filtro por categoria.
    """
    query = db.query(Product).filter(Product.is_active.is_(True))
    
    # Filtro por busca textual (título ou categoria)
    if q and q.strip():
        search_term = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Product.title.ilike(search_term),
                Product.category.ilike(search_term),
                Product.description.ilike(search_term)
            )
        )
    
    # Filtro por categoria
    selected_category = "Todos"
    if categoria and categoria.strip() and categoria.strip().lower() != "todos":
        selected_category = categoria.strip()
        if selected_category == "Ofertas Relâmpago":
            query = query.filter(
                or_(
                    Product.badge.ilike("%relâmpago%"),
                    Product.badge.ilike("%relampago%"),
                    Product.badge.ilike("%off%")
                )
            )
        else:
            query = query.filter(Product.category.ilike(f"%{selected_category}%"))
    
    # Ordenar pelos produtos mais recentes
    products = query.order_by(Product.created_at.desc()).all()
    
    # Contagem de produtos totais ativos
    total_active = db.query(Product).filter(Product.is_active.is_(True)).count()
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "products": products,
            "categories": PRESET_CATEGORIES,
            "selected_category": selected_category,
            "search_query": q or "",
            "total_active": total_active,
            "telegram_url": settings.TELEGRAM_VIP_URL,
            "whatsapp_url": settings.WHATSAPP_VIP_URL,
            "app_name": settings.APP_NAME,
            "app_url": settings.APP_URL
        }
    )


@router.get("/ir/{slug}")
async def redirect_affiliate(
    slug: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Rota de redirecionamento HTTP 302 para links de afiliados.
    1. Localiza o produto pelo slug único.
    2. Incrementa o contador de cliques.
    3. Redireciona o usuário para a URL de afiliado do Mercado Livre.
    """
    product = db.query(Product).filter(Product.slug == slug).first()
    
    if not product or not product.is_active:
        # Se o produto não existir ou estiver desativado, exibe página amigável de oferta expirada
        return templates.TemplateResponse(
            request=request,
            name="404.html",
            context={
                "app_name": settings.APP_NAME,
                "telegram_url": settings.TELEGRAM_VIP_URL,
                "slug": slug
            },
            status_code=404
        )
    
    # Incrementa o contador de cliques
    product.clicks_count += 1
    db.commit()
    
    # Redirecionamento 302 (Found) direto para o link de afiliado oficial
    return RedirectResponse(
        url=product.affiliate_url,
        status_code=status.HTTP_302_FOUND
    )


@router.get("/politica-de-privacidade", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    """Página de Política de Privacidade e Isenção de Responsabilidade (Compliance)."""
    return templates.TemplateResponse(
        request=request,
        name="legal.html",
        context={
            "app_name": settings.APP_NAME,
            "title": "Política de Privacidade & Termos de Uso",
            "telegram_url": settings.TELEGRAM_VIP_URL,
            "whatsapp_url": settings.WHATSAPP_VIP_URL
        }
    )
