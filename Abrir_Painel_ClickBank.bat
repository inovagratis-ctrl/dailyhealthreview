@echo off
title ClickBank Live Sales Dashboard - Daily Health Review
color 0A
echo ============================================================
echo   INICIANDO PAINEL DE VENDAS E METRICAS CLICKBANK
echo   Conta: eusimar72 ^| Portal: dailyhealthreview.vercel.app
echo ============================================================
echo.
echo Conectando aos servidores da ClickBank...
cd /d "C:\Users\Eusimar\.gemini\antigravity\scratch\Projeto_ClickBank_DailyHealthReview"
python dashboard.py
pause
