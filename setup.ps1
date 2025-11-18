# Script de Setup Inicial - Agendas Ativa
# Execute este script para configurar o ambiente automaticamente

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AGENDAS ATIVA - SETUP INICIAL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "1. Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "   ERRO: Python nao encontrado" -ForegroundColor Red
    Write-Host "   Instale Python 3.10+ de python.org" -ForegroundColor Red
    exit 1
}

# Instalar dependências
Write-Host ""
Write-Host "2. Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "   OK: Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "   ERRO: Falha ao instalar dependencias" -ForegroundColor Red
    exit 1
}

# Criar pasta .streamlit se não existir
Write-Host ""
Write-Host "3. Configurando estrutura..." -ForegroundColor Yellow
if (-not (Test-Path ".streamlit")) {
    New-Item -ItemType Directory -Path ".streamlit" | Out-Null
    Write-Host "   OK: Pasta .streamlit criada" -ForegroundColor Green
} else {
    Write-Host "   OK: Pasta .streamlit ja existe" -ForegroundColor Green
}

# Verificar se secrets.toml existe
Write-Host ""
Write-Host "4. Verificando configuracao de secrets..." -ForegroundColor Yellow
if (-not (Test-Path ".streamlit\secrets.toml")) {
    Write-Host "   ATENCAO: secrets.toml nao encontrado" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "   Voce precisa configurar suas credenciais!" -ForegroundColor Yellow
    Write-Host ""
    
    # Perguntar se quer criar agora
    $resposta = Read-Host "   Deseja criar o arquivo secrets.toml agora? (s/n)"
    
    if ($resposta -eq "s" -or $resposta -eq "S") {
        Write-Host ""
        Write-Host "   Configure suas credenciais:" -ForegroundColor Cyan
        Write-Host ""
        
        $supabaseUrl = Read-Host "   SUPABASE_URL"
        $supabaseKey = Read-Host "   SUPABASE_KEY"
        $cohereKey = Read-Host "   COHERE_API_KEY"
        
        $secretsContent = @"
# Configuracao - Agendas Ativa
SUPABASE_URL = "$supabaseUrl"
SUPABASE_KEY = "$supabaseKey"
COHERE_API_KEY = "$cohereKey"
"@
        
        $secretsContent | Out-File -FilePath ".streamlit\secrets.toml" -Encoding utf8
        Write-Host ""
        Write-Host "   OK: secrets.toml criado!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "   Copie .streamlit\secrets.toml.example para .streamlit\secrets.toml" -ForegroundColor Yellow
        Write-Host "   e preencha com suas credenciais" -ForegroundColor Yellow
    }
} else {
    Write-Host "   OK: secrets.toml encontrado" -ForegroundColor Green
}

# Executar testes
Write-Host ""
Write-Host "5. Executando testes de configuracao..." -ForegroundColor Yellow
Write-Host ""
python test_config.py

# Mensagem final
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   SETUP CONCLUIDO!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Yellow
Write-Host "1. Configure o banco de dados no Supabase (use setup_database.sql)" -ForegroundColor White
Write-Host "2. Verifique o arquivo secrets.toml" -ForegroundColor White
Write-Host "3. Execute: streamlit run app.py" -ForegroundColor White
Write-Host ""
Write-Host "Para ajuda detalhada, consulte INSTALL.md" -ForegroundColor Cyan
Write-Host ""
