@echo off
title Pinhatech & Variedades - Servidor Local
chcp 65001 >nul
echo ======================================================
echo   PINHATECH & VARIEDADES - SERVIDOR LOCAL
echo ======================================================

cd /d "%~dp0"

if not exist .env (
    echo [INFO] Criando arquivo .env a partir de .env.example...
    copy .env.example .env >nul
)

if not exist .venv\Scripts\python.exe (
    echo [INFO] Criando ambiente virtual Python (.venv)...
    py -3.11 -m venv .venv 2>nul || py -m venv .venv 2>nul || python -m venv .venv
    echo [INFO] Instalando dependencias (aguarde)...
    ".venv\Scripts\pip.exe" install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --quiet
)

echo.
echo ------------------------------------------------------
echo Servidor iniciando em: http://localhost:8000
echo Painel Administrativo:  http://localhost:8000/admin
echo Usuario: admin  ^|  Senha: PinhatechAdmin2025!
echo ------------------------------------------------------
echo Pressione CTRL+C para encerrar.
echo.

".venv\Scripts\uvicorn.exe" main:app --reload --host 127.0.0.1 --port 8000
pause
