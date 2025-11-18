@echo off
echo ============================================
echo  INSTALACAO DO PYTHON - Agendas Ativa
echo ============================================
echo.
echo Python nao encontrado no sistema!
echo.
echo Por favor, instale o Python 3.10 ou superior:
echo.
echo 1. Acesse: https://www.python.org/downloads/
echo 2. Baixe Python 3.10 ou superior
echo 3. IMPORTANTE: Marque a opcao "Add Python to PATH"
echo 4. Execute a instalacao
echo 5. Reinicie o PowerShell
echo 6. Execute este script novamente
echo.
echo ============================================
echo.
pause

REM Abrindo navegador para download
start https://www.python.org/downloads/

echo.
echo Apos instalar o Python, execute:
echo     .\install_complete.ps1
echo.
pause
