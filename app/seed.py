"""
Seed inicial para o banco de dados da Pinhatech & Variedades.
Insere 6 produtos de exemplo bem estruturados (3 ferramentas e 3 eletrônicos)
caso o banco de dados esteja vazio.
"""
from sqlalchemy.orm import Session
from app.models import Product


SEED_PRODUCTS = [
    # --- FERRAMENTAS ---
    {
        "title": "Parafusadeira e Furadeira de Impacto Brushless 20V com 2 Baterias e Maleta",
        "slug": "parafusadeira-impacto-brushless-20v",
        "category": "Ferramentas",
        "image_url": "https://images.unsplash.com/photo-1504148455328-c376907d081c?auto=format&fit=crop&w=800&q=80",
        "old_price": 549.90,
        "current_price": 349.90,
        "installments": "em 10x de R$ 34,99 sem juros",
        "badge": "ENVIO FULL",
        "affiliate_url": "https://mercadolivre.com/sec/exemplo-parafusadeira",
        "is_active": True,
        "clicks_count": 42,
        "description": "Motor Brushless sem escovas de alto rendimento. Acompanha 2 baterias de lítio 20V, carregador bivolt rápido, jogo de brocas, bits e maleta reforçada para transporte."
    },
    {
        "title": "Jogo Kit de Ferramentas Manuais em Aço Cromo Vanádio com Maleta 142 Peças",
        "slug": "kit-ferramentas-maleta-142-pecas",
        "category": "Ferramentas",
        "image_url": "https://images.unsplash.com/photo-1581783342308-f792dbdd27c5?auto=format&fit=crop&w=800&q=80",
        "old_price": 289.00,
        "current_price": 189.90,
        "installments": "em 6x de R$ 31,65 sem juros",
        "badge": "-34% OFF",
        "affiliate_url": "https://mercadolivre.com/sec/exemplo-kit-ferramentas",
        "is_active": True,
        "clicks_count": 28,
        "description": "Kit profissional completo com chaves combinadas, catraca reversível, soquetes estriados, alicates de precisão e estojo organizador termoplástico rígido."
    },
    {
        "title": "Nível Laser 12 Linhas 3D Feixe Verde Autonivelante com Tripé e Controle Remoto",
        "slug": "nivel-laser-12-linhas-3d-verde",
        "category": "Ferramentas",
        "image_url": "https://images.unsplash.com/photo-1572981779307-38b8cabb2407?auto=format&fit=crop&w=800&q=80",
        "old_price": 420.00,
        "current_price": 279.00,
        "installments": "em 9x de R$ 31,00 sem juros",
        "badge": "MAIS VENDIDO",
        "affiliate_url": "https://mercadolivre.com/sec/exemplo-nivel-laser",
        "is_active": True,
        "clicks_count": 35,
        "description": "Feixe verde de altíssima visibilidade para interiores e exteriores. Alinhamento 360 graus em 3 planos, base magnética giratória, bateria recarregável e bolsa protetora."
    },

    # --- PRODUTOS ELETRÔNICOS & CASA INTELIGENTE ---
    {
        "title": "Smartwatch Pro AMOLED Tela Infinita Bluetooth Chamada e Monitor Cardíaco IP68",
        "slug": "smartwatch-pro-amoled-bluetooth",
        "category": "Eletrônicos",
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80",
        "old_price": 399.00,
        "current_price": 219.90,
        "installments": "em 10x de R$ 21,99 sem juros",
        "badge": "ENVIO FULL",
        "affiliate_url": "https://mercadolivre.com/sec/exemplo-smartwatch",
        "is_active": True,
        "clicks_count": 67,
        "description": "Tela AMOLED de alta resolução com Always-On Display. Atende e faz ligações via Bluetooth, mais de 100 modos de treino, monitoramento de sono e oxigenação no sangue."
    },
    {
        "title": "Fone de Ouvido Sem Fio TWS Bluetooth 5.3 com Cancelamento Ativo de Ruído (ANC)",
        "slug": "fone-tws-bluetooth-53-anc",
        "category": "Eletrônicos",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80",
        "old_price": 249.90,
        "current_price": 139.90,
        "installments": "em 4x de R$ 34,98 sem juros",
        "badge": "-44% OFF",
        "affiliate_url": "https://mercadolivre.com/sec/exemplo-fone-tws",
        "is_active": True,
        "clicks_count": 53,
        "description": "Áudio Hi-Fi estéreo com graves potentes e cancelamento ativo de ruído ambiente. Bateria para até 32h de reprodução com o estojo de recarga USB-C."
    },
    {
        "title": "Câmera de Segurança Wi-Fi 360° Externa Full HD Visão Noturna Colorida IP66",
        "slug": "camera-seguranca-wifi-360-externa",
        "category": "Casa Inteligente",
        "image_url": "https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=800&q=80",
        "old_price": 299.90,
        "current_price": 179.90,
        "installments": "em 5x de R$ 35,98 sem juros",
        "badge": "OFERTA RELÂMPAGO",
        "affiliate_url": "https://mercadolivre.com/sec/exemplo-camera-wifi",
        "is_active": True,
        "clicks_count": 19,
        "description": "Monitoramento em tempo real direto pelo celular (Android e iOS). Rastreamento automático de movimento humano, áudio bidirecional e holofote LED integrado."
    }
]


def seed_database(db: Session):
    """Verifica se há produtos no banco; se estiver vazio, popula com os 6 produtos padrão."""
    count = db.query(Product).count()
    if count == 0:
        for item in SEED_PRODUCTS:
            product = Product(**item)
            db.add(product)
        db.commit()
        print(" [SEED] 6 produtos iniciais cadastrados com sucesso no banco de dados!")
    else:
        print(f" [SEED] Banco de dados já contém {count} produtos. Pulando seed.")
