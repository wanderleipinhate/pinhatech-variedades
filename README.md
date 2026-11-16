# ⚡ Pinhatech & Variedades

> **Vitrine Profissional de Produtos Afiliados (Mercado Livre)**  
> Nicho: **Ferramentas Manuais/Elétricas & Produtos Eletrônicos**  
> Identidade Visual: **Tema Dark / Industrial de Alto Contraste** (`#0F0F0F` e `#FF6B00`)

---

## 📋 Sumário
1. [Visão Geral e Arquitetura](#-visão-geral-e-arquitetura)
2. [Estrutura de Diretórios](#-estrutura-de-diretórios)
3. [Tecnologias Utilizadas](#-tecnologias-utilizadas)
4. [Funcionalidades Principais](#-funcionalidades-principais)
5. [Como Rodar Localmente no Windows](#-como-rodar-localmente-no-windows)
6. [Como Rodar com Docker & Docker Compose](#-como-rodar-com-docker--docker-compose)
7. [Como Colocar no Ar (Deploy Gratuito ou VPS)](#-como-colocar-no-ar-deploy-gratuito-ou-vps)
8. [Gerador de Copy para Redes Sociais](#-gerador-de-copy-para-redes-sociais)
9. [Segurança e Compliance](#-segurança-e-compliance)

---

## 🚀 Visão Geral e Arquitetura

O **Pinhatech & Variedades** foi desenvolvido por um Arquiteto de Software Full-Stack Sênior para proporcionar a mais alta taxa de conversão em vendas de afiliados do Mercado Livre.

A arquitetura adota o padrão **Server-Side Rendering (SSR)** moderno com **FastAPI + Jinja2 Templates**, entregando páginas HTML puras, ultrarrápidas no carregamento móvel (vital para usuários vindos de redes sociais como Telegram, WhatsApp, TikTok e Facebook), sem o peso de frameworks SPA pesados.

### Principais Pilares:
- **Zero Custo Inicial:** Banco de dados **SQLite** com criação automática de tabelas e **seed de 6 produtos iniciais realistas**.
- **Links Curtos e Rastreamento:** Redirecionamento 302 via `/ir/{slug}` com contador de cliques atômico no banco de dados.
- **Painel Administrativo Protegido:** Autenticação via cookies assinados criptograficamente (`itsdangerous`), dashboard com métricas de cliques, CRUD completo e gerador de copy promocional.
- **Compliance com o Mercado Livre:** Avisos claros e ostensivos de afiliado, garantindo conformidade com os termos do programa e total transparência com o cliente.

---

## 📂 Estrutura de Diretórios

```
Pinhatech & Variedades/
│
├── app/
│   ├── __init__.py               # Pacote principal
│   ├── config.py                 # Configurações e variáveis de ambiente (Pydantic Settings)
│   ├── database.py               # Engine SQLAlchemy, SessionLocal e init_db
│   ├── models.py                 # Modelo Product com cálculo de descontos e formatações
│   ├── seed.py                   # Seed automático com 6 produtos campeões de vendas
│   ├── auth.py                   # Autenticação de sessão por cookie seguro (itsdangerous)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── public.py             # Rotas públicas: Vitrine (/), Redirecionador (/ir/{slug}), Legal
│   │   └── admin.py              # Rotas do Admin: Login, Dashboard, CRUD e Toggle
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css        # Estilos industriais, scrollbar, brilhos e efeitos
│   │   ├── js/
│   │   │   ├── main.js           # Busca em tempo real e fallbacks de imagem
│   │   │   └── admin.js          # Gerador de copy, cópia de link curto e auto-slug
│   │   └── img/
│   │       ├── favicon.svg       # Favicon vetorial (raio + engrenagem laranja)
│   │       └── logo.svg          # Logo estilizada da marca
│   │
│   └── templates/
│       ├── base.html             # Layout base com Tailwind CDN e Rodapé de Compliance
│       ├── index.html            # Vitrine com filtro por categorias e cards de ofertas
│       ├── 404.html              # Página 404 amigável para ofertas expiradas
│       ├── legal.html            # Termos de Uso e Política de Privacidade (LGPD)
│       └── admin/
│           ├── base_admin.html   # Layout base do painel admin + modal de copy
│           ├── login.html        # Página de login administrativo dark/industrial
│           ├── dashboard.html    # Tabela com métricas, cliques e ações rápidas
│           └── product_form.html # Formulário completo de cadastro e edição
│
├── .env                          # Variáveis de ambiente locais
├── .env.example                  # Modelo de variáveis de ambiente
├── requirements.txt              # Dependências Python
├── Dockerfile                    # Container Docker para produção (Python 3.11 Slim)
├── docker-compose.yml            # Orquestração do container com volume persistente
├── start.ps1                     # Script de inicialização automática no Windows PowerShell
├── start.bat                     # Inicializador com 2 cliques no Windows
└── README.md                     # Documentação completa
```

---

## 🛠 Tecnologias Utilizadas

- **Linguagem:** Python 3.11+
- **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/) (Alta performance assíncrona)
- **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)
- **Template Engine:** [Jinja2](https://jinja.palletsprojects.com/)
- **ORM / Banco de Dados:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/) + **SQLite**
- **Estilização:** [Tailwind CSS](https://tailwindcss.com/) (CDN) com paleta personalizada Dark/Industrial
- **Ícones:** [Lucide Icons](https://lucide.dev/)
- **Segurança:** `itsdangerous` para cookies de sessão assinados e `pydantic-settings`

---

## 💡 Funcionalidades Principais

### 1. Vitrine Pública (`/`)
- **Tema Dark/Industrial:** Fundo Preto Profundo (`#0F0F0F`), cards em Cinza Chumbo (`#1A1A1A`), detalhes e botões CTA em Laranja Vivo (`#FF6B00`) e preços promocionais em Verde Esmeralda (`#10B981`).
- **Filtros por Categoria Rápidos:** Botões estilizados para alternar entre "Todos", "Ferramentas", "Eletrônicos", "Casa Inteligente" e "Ofertas Relâmpago".
- **Busca em Tempo Real:** Filtra instantaneamente as ofertas na tela conforme o usuário digita no campo de busca (sem recarregar a página), além de busca completa via query string.
- **Card de Oferta de Alta Conversão:**
  - Imagem do produto em alta definição com fallback automático.
  - Selos chamativos: `"ENVIO FULL"`, `"-35% OFF"`, `"MAIS VENDIDO"`.
  - Título técnico em destaque.
  - Preço riscado (`De: R$ 549,90`), preço promocional (`Por: R$ 349,90`) e parcelamento (`em até 10x sem juros`).
  - Botão CTA pulsante: **"VER OFERTA NO MERCADO LIVRE"**.
- **Canal VIP do Telegram:** Barra superior e botão destacado na barra de navegação para capturar leads para o seu canal de ofertas.

### 2. Rastreamento e Links Amigáveis (`/ir/{slug}`)
Em vez de divulgar links feios ou genéricos nas redes sociais, você divulga links com a sua própria marca:
```
https://seusite.com/ir/parafusadeira-impacto-brushless-20v
```
Ao ser acessado:
1. O backend busca o produto pelo `slug`.
2. Incrementa o contador `clicks_count` em +1 no banco de dados.
3. Retorna um **HTTP 302 Redirect** enviando o comprador direto para o link oficial de afiliado do Mercado Livre.
4. Se o produto estiver inativo ou com estoque esgotado, exibe uma tela amigável sugerindo outras ofertas e convidando o usuário para o grupo VIP do Telegram.

### 3. Painel Administrativo Protegido (`/admin`)
- **Autenticação:** Login protegido em `/admin/login` com credenciais definidas no arquivo `.env`.
- **Métricas em Tempo Real:** Total de produtos cadastrados, quantidade de ofertas ativas, total de cliques acumulados e média de cliques por oferta.
- **Gerenciamento Completo de Ofertas:**
  - **Adicionar:** Cadastro com gerador automático de slug e pré-visualização de imagem.
  - **Editar:** Alteração de preços e condições de pagamento em segundos.
  - **Toggle Rápido:** Ative ou desative uma oferta com 1 clique.
  - **Excluir:** Remoção com confirmação de segurança.
- **Botão "Copiar Link Curto":** Copia a URL amigável `/ir/{slug}` pronta para colar onde quiser.
- **Botão "Gerar Texto para Redes Sociais":** Gera instantaneamente uma copy profissional formatada com emojis para Telegram, WhatsApp ou grupos de Facebook.

---

## 💻 Como Rodar Localmente no Windows

### Pré-requisito
Certifique-se de ter o **Python 3.11+** instalado em seu sistema:
> Se ainda não tiver o Python instalado, você pode instalar pelo comando do Windows:
> ```powershell
> winget install Python.Python.3.11
> ```
> *(Marque a opção "Add Python to PATH" durante a instalação).*

---

### Opção 1: Inicialização Automática (Recomendada)
Basta dar um duplo clique no arquivo **`start.bat`** ou executar o script no PowerShell:

```powershell
.\start.ps1
```

O script cuidará de tudo:
1. Cria o arquivo `.env` (se não existir).
2. Cria o ambiente virtual `.venv`.
3. Instala as dependências do `requirements.txt`.
4. Inicia o servidor com recarga automática (*Live Reload*).

---

### Opção 2: Passo a Passo Manual no PowerShell

1. Abra o PowerShell na pasta do projeto:
```powershell
cd "c:\Users\wande\Documents\Pinhatech & Variedades"
```

2. Crie e ative o ambiente virtual:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instale as dependências:
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Inicie o servidor com Uvicorn:
```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

5. Acesse no seu navegador:
- **Vitrine Pública:** [http://localhost:8000](http://localhost:8000)
- **Painel Administrativo:** [http://localhost:8000/admin](http://localhost:8000/admin)
  - **Usuário:** `admin`
  - **Senha:** `PinhatechAdmin2025!` *(alterável no `.env`)*

---

## 🐳 Como Rodar com Docker & Docker Compose

Se você prefere rodar tudo isolado via Docker:

1. Suba o container com o comando:
```bash
docker-compose up -d --build
```

2. Verifique o status do container:
```bash
docker-compose ps
```

3. O banco de dados SQLite (`pinhatech.db`) é mantido salvo na raiz da sua máquina através do volume montado, preservando todos os seus produtos e estatísticas de cliques mesmo se o container for recriado.

4. Para parar o container:
```bash
docker-compose down
```

---

## ☁️ Como Colocar no Ar (Deploy Gratuito ou VPS)

### Opção A: Deploy Gratuito no Render ou Railway

1. Suba seu código para um repositório no **GitHub** (privado ou público).
2. Acesse [Render.com](https://render.com/) ou [Railway.app](https://railway.app/).
3. Crie um novo **Web Service** conectado ao seu repositório.
4. Preencha as configurações:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Na aba **Environment Variables**, adicione as mesmas variáveis do arquivo `.env`:
   - `ADMIN_USERNAME`: Seu usuário desejado
   - `ADMIN_PASSWORD`: Uma senha forte
   - `SECRET_KEY`: Uma sequência de caracteres aleatórios
   - `APP_URL`: O domínio final fornecido pela plataforma (ex: `https://pinhatech.onrender.com`)
   - `TELEGRAM_VIP_URL`: O link do seu grupo/canal
6. Clique em **Deploy**. O FastAPI criará o banco de dados e os 6 produtos automaticamente no primeiro boot!

---

### Opção B: Deploy em VPS Linux (Ubuntu + Nginx + Systemd)

1. Conecte-se na sua VPS via SSH e clone o projeto:
```bash
git clone <url-do-seu-repositorio> /var/www/pinhatech
cd /var/www/pinhatech
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env # configure sua senha e URLs
```

2. Crie o serviço Systemd `/etc/systemd/system/pinhatech.service`:
```ini
[Unit]
Description=Pinhatech & Variedades FastAPI App
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/pinhatech
ExecStart=/var/www/pinhatech/.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Ative e inicie o serviço:
```bash
sudo systemctl daemon-reload
sudo systemctl enable pinhatech
sudo systemctl start pinhatech
```

4. Configure o proxy reverso no Nginx com certificado SSL gratuito via Let's Encrypt (`certbot --nginx -d seudominio.com.br`).

---

## 📱 Gerador de Copy para Redes Sociais

No Painel Administrativo (`/admin`), em qualquer produto, clique no ícone **Compartilhar (Share)**. O sistema abre uma janela com a copy já formatada:

```text
🔥 *SUPER OFERTA PINHATECH & VARIEDADES!* 🔥

⚡ *Parafusadeira e Furadeira de Impacto Brushless 20V com 2 Baterias e Maleta*
🏷️ ~De: R$ 549,90~
💰 *Por apenas: R$ 349,90*
💳 em 10x de R$ 34,99 sem juros
📦 Selo: ENVIO FULL

👇 *Garanta o seu no link oficial do Mercado Livre:*
👉 https://pinhatech.com.br/ir/parafusadeira-impacto-brushless-20v

⚠️ _Preço e estoque sujeitos a alteração a qualquer momento!_
```

Basta clicar em **"Copiar Mensagem"** e colar direto no Telegram, WhatsApp ou Facebook!

---

## 🔒 Segurança e Compliance

1. **Afiliados Mercado Livre:** O site inclui um aviso oficial no rodapé informando a participação no programa de afiliados, deixando explícito que as compras são concluídas na plataforma do Mercado Livre e sem custo adicional ao usuário.
2. **Sessões Protegidas:** As sessões de administração utilizam cookies seguros assinados digitalmente com `itsdangerous`, impedindo qualquer tentativa de falsificação de credenciais no cliente.
3. **Privacidade (LGPD):** O sistema não rastreia dados pessoais dos compradores, coletando unicamente a quantidade total de cliques para análise de interesse do catálogo.

---

**Pinhatech & Variedades** — *Tecnologia, Ferramentas e Ofertas que Funcionam.*
