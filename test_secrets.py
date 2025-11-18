"""
Teste de leitura do secrets.toml
"""
import sys
import os

# Adicionar path
sys.path.insert(0, r'C:\Users\andre\OneDrive\Área de Trabalho\Ativa')
os.chdir(r'C:\Users\andre\OneDrive\Área de Trabalho\Ativa')

print("🔍 Testando leitura de secrets.toml...")
print(f"📁 Diretório atual: {os.getcwd()}")

# Verificar se arquivo existe
secrets_path = ".streamlit/secrets.toml"
if os.path.exists(secrets_path):
    print(f"✅ Arquivo {secrets_path} existe")
    
    # Ler conteúdo
    with open(secrets_path, 'r') as f:
        content = f.read()
        print(f"\n📄 Conteúdo do arquivo:\n{content}")
else:
    print(f"❌ Arquivo {secrets_path} NÃO existe")

# Tentar importar streamlit e ler secrets
print("\n🔍 Tentando importar Streamlit e ler secrets...")
try:
    import streamlit as st
    
    # Tentar acessar secrets
    print("Tentando acessar st.secrets...")
    url = st.secrets["SUPABASE_URL"]
    print(f"✅ SUPABASE_URL: {url}")
    
    key = st.secrets["SUPABASE_KEY"]
    print(f"✅ SUPABASE_KEY: {key[:30]}...")
    
except Exception as e:
    print(f"❌ Erro ao ler secrets: {e}")
    import traceback
    traceback.print_exc()

print("\n🔍 Testando Database...")
try:
    from database import Database
    db = Database()
    
    print(f"URL: {db.supabase_url}")
    print(f"Key: {db.supabase_key[:30] if db.supabase_key else 'None'}...")
    print(f"Client: {db.client}")
    
    if db.client:
        print("✅ Database conectado!")
    else:
        print("❌ Database NÃO conectado")
        
except Exception as e:
    print(f"❌ Erro: {e}")
    import traceback
    traceback.print_exc()
