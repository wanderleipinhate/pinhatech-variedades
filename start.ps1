# ==============================================================
# SCRIPT DE INICIALIZAÇÃO LOCAL - PINHATECH & VARIEDADES
# Windows PowerShell
# ==============================================================

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  PINHATECH & VARIEDADES - INICIALIZADOR AUTOMATICO  " -ForegroundColor Yellow
Write-Host "======================================================" -ForegroundColor Cyan

# 1. Configura arquivo .env se ainda não existir
if (-not (Test-Path ".env")) {
    Write-Host "[INFO] Criando arquivo .env a partir de .env.example..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
}

# 2. Cria o ambiente virtual (.venv) se não existir
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[INFO] Criando ambiente virtual Python (.venv)..." -ForegroundColor Cyan
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3.11 -m venv .venv
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        python -m venv .venv
    } else {
        Write-Host "[ERRO] Python nao encontrado." -ForegroundColor Red
        Exit 1
    }

    Write-Host "[INFO] Instalando dependencias do requirements.txt..." -ForegroundColor Cyan
    & ".\.venv\Scripts\pip.exe" install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --quiet
}

Write-Host "------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "[SUCESSO] Servidor pronto para inicializacao!" -ForegroundColor Green
Write-Host "Vitrine Publica:   http://localhost:8000" -ForegroundColor Yellow
Write-Host "Painel Admin:      http://localhost:8000/admin" -ForegroundColor Yellow
Write-Host "Usuario Padrao:    admin" -ForegroundColor White
Write-Host "Senha Padrao:      PinhatechAdmin2025!" -ForegroundColor White
Write-Host "------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "Pressione CTRL+C para encerrar o servidor a qualquer momento.`n" -ForegroundColor DarkYellow

# 3. Inicia o servidor com o uvicorn do ambiente virtual
& ".\.venv\Scripts\uvicorn.exe" main:app --reload --host 127.0.0.1 --port 8000
