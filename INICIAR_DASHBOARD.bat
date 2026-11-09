@echo off
title Daily Health Review Command Center (Port 8080)
color 0A
echo ========================================================
echo    DAILY HEALTH REVIEW - COMMAND CENTER 8080
echo ========================================================
echo.

cd /d "C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"

netstat -ano | findstr ":8080" | findstr "LISTENING" >nul
if %errorlevel% == 0 (
    echo [OK] O servidor ja esta rodando na porta 8080!
) else (
    echo Iniciando o servidor Python na porta 8080...
    start /b py -3.12 dashboard.py
    timeout /t 2 /nobreak >nul
)

echo Abrindo painel no seu navegador...
start "" "http://localhost:8080/"
echo.
echo [SUCESSO] Painel aberto! Voce ja pode ver as 36 ofertas e 108 ativos.
timeout /t 4 >nul
