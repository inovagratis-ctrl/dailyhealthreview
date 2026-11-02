@echo off
chcp 65001 >nul
title Daily Health Review - Diagnóstico Periódico de Links e Comissões
color 0A

echo =======================================================================
echo     DAILY HEALTH REVIEW - AUDITORIA DE INTEGRIDADE DE LINKS
echo =======================================================================
echo.
echo Executando auditoria profunda nos 36 produtos, Showcases e HopLinks...
echo.

cd /d "%~dp0"
python audit_healthcheck.py

echo.
echo =======================================================================
echo Auditoria concluida! Abrindo relatorio em tela...
echo =======================================================================
echo.

type DIAGNOSTICO_LINKS_STATUS.txt
echo.
pause
