# ==============================================================
# DOCKERFILE - PINHATECH & VARIEDADES
# Otimizado para Python 3.11 Slim (Leve e Seguro)
# ==============================================================

FROM python:3.11-slim

# Evita que o Python grave arquivos bytecode (.pyc) e garante logs imediatos
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Cria diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para compilação se houver
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependências Python primeiro (aproveita cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o código-fonte da aplicação
COPY . .

# Expõe a porta padrão
EXPOSE 8000

# Comando para iniciar o servidor Uvicorn em modo produção
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
