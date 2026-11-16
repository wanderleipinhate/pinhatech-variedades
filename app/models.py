from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=False, index=True)
    image_url = Column(String(1000), nullable=False)
    
    # Preços e Condições de Pagamento
    old_price = Column(Float, nullable=True)
    current_price = Column(Float, nullable=False)
    installments = Column(String(150), nullable=True)
    
    # Selos e Destaques
    badge = Column(String(100), nullable=True)  # ex: "ENVIO FULL", "-35% OFF", "MAIS VENDIDO"
    
    # Afiliado e Rastreamento
    affiliate_url = Column(String(1000), nullable=False)
    clicks_count = Column(Integer, default=0, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @property
    def formatted_current_price(self) -> str:
        """Formata o preço atual no padrão brasileiro (R$ 1.234,56)."""
        if self.current_price is None:
            return "R$ 0,00"
        return f"R$ {self.current_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @property
    def formatted_old_price(self) -> str:
        """Formata o preço antigo no padrão brasileiro."""
        if not self.old_price:
            return ""
        return f"R$ {self.old_price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    @property
    def discount_percent(self) -> int:
        """Calcula o percentual de desconto se houver preço antigo."""
        if self.old_price and self.old_price > self.current_price:
            discount = ((self.old_price - self.current_price) / self.old_price) * 100
            return int(round(discount))
        return 0

    def __repr__(self):
        return f"<Product(id={self.id}, title='{self.title[:30]}...', slug='{self.slug}', clicks={self.clicks_count})>"
