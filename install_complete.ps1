# Script de Instalacao Completa - Agendas Ativa
# Execute APOS instalar o Python

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   INSTALACAO AUTOMATICA - AGENDAS ATIVA" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python nao encontrado"
    }
} catch {
    Write-Host "   ERRO: Python nao encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Execute: .\install_python.bat" -ForegroundColor Yellow
    Write-Host "   Ou baixe em: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 1
}

# Atualizar pip
Write-Host ""
Write-Host "2. Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "   OK: pip atualizado" -ForegroundColor Green

# Instalar dependencias
Write-Host ""
Write-Host "3. Instalando dependencias (pode demorar 2-3 min)..." -ForegroundColor Yellow
Write-Host ""

$packages = @(
    "streamlit==1.31.0",
    "supabase==2.3.4",
    "cohere==4.47",
    "pandas==2.1.4",
    "plotly==5.18.0",
    "python-dateutil==2.8.2"
)

foreach ($package in $packages) {
    $packageName = $package.Split("==")[0]
    Write-Host "   Instalando $packageName..." -ForegroundColor Cyan
    python -m pip install $package --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   OK: $packageName instalado" -ForegroundColor Green
    } else {
        Write-Host "   AVISO: Problema ao instalar $packageName" -ForegroundColor Yellow
    }
}

# Criar estrutura .streamlit
Write-Host ""
Write-Host "4. Configurando estrutura..." -ForegroundColor Yellow
if (-not (Test-Path ".streamlit")) {
    New-Item -ItemType Directory -Path ".streamlit" | Out-Null
    Write-Host "   OK: Pasta .streamlit criada" -ForegroundColor Green
} else {
    Write-Host "   OK: Pasta .streamlit ja existe" -ForegroundColor Green
}

# Criar arquivo secrets vazio se nao existir
if (-not (Test-Path ".streamlit\secrets.toml")) {
    $secretsTemplate = @"
# Configure suas credenciais aqui
# Obtenha em:
# - Supabase: https://supabase.com > Seu Projeto > Settings > API
# - Cohere: https://cohere.com > Dashboard > API Keys

SUPABASE_URL = "COLE_SUA_URL_AQUI"
SUPABASE_KEY = "COLE_SUA_KEY_AQUI"
COHERE_API_KEY = "COLE_SUA_KEY_AQUI"

# IMPORTANTE: Depois de configurar, execute:
# python test_config.py
"@
    $secretsTemplate | Out-File -FilePath ".streamlit\secrets.toml" -Encoding utf8
    Write-Host "   OK: secrets.toml criado (CONFIGURE AS CREDENCIAIS!)" -ForegroundColor Yellow
} else {
    Write-Host "   OK: secrets.toml ja existe" -ForegroundColor Green
}

# Executar teste
Write-Host ""
Write-Host "5. Testando instalacao..." -ForegroundColor Yellow
Write-Host ""
python test_config.py

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   INSTALACAO CONCLUIDA!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PROXIMOS PASSOS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. CONFIGURE O SUPABASE:" -ForegroundColor White
Write-Host "   - Acesse: https://supabase.com" -ForegroundColor Cyan
Write-Host "   - Crie um projeto gratuito" -ForegroundColor Cyan
Write-Host "   - Execute o script: setup_database.sql (no SQL Editor)" -ForegroundColor Cyan
Write-Host "   - Copie URL e Key (Settings > API)" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. CONFIGURE O COHERE:" -ForegroundColor White
Write-Host "   - Acesse: https://cohere.com" -ForegroundColor Cyan
Write-Host "   - Crie conta gratuita" -ForegroundColor Cyan
Write-Host "   - Copie sua API Key" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. EDITE O ARQUIVO:" -ForegroundColor White
Write-Host "   .streamlit\secrets.toml" -ForegroundColor Cyan
Write-Host "   (Cole suas credenciais)" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. TESTE NOVAMENTE:" -ForegroundColor White
Write-Host "   python test_config.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. EXECUTE A APLICACAO:" -ForegroundColor White
Write-Host "   streamlit run app.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Duvidas? Consulte INSTALL.md" -ForegroundColor Yellow
Write-Host ""
