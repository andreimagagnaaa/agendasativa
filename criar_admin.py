"""
Script para criar usuário admin diretamente no Supabase
"""
import os
import bcrypt
from supabase import create_client, Client
import toml

# Ler credenciais
secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

SUPABASE_URL = secrets["SUPABASE_URL"]
SUPABASE_KEY = secrets["SUPABASE_KEY"]

print(f"🔑 Conectando ao Supabase...")

# Criar cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Gerar hash da senha
senha = "admin123"
senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"🔐 Hash gerado: {senha_hash}")

# Verificar se usuário já existe
try:
    response = supabase.table("usuarios").select("*").eq("email", "admin@ativa.com").execute()
    
    if response.data and len(response.data) > 0:
        print(f"\n⚠️  Usuário admin@ativa.com já existe!")
        print(f"Atualizando senha...")
        
        # Atualizar senha
        update_response = supabase.table("usuarios")\
            .update({"senha_hash": senha_hash, "ativo": True})\
            .eq("email", "admin@ativa.com")\
            .execute()
        
        if update_response.data:
            print(f"✅ Senha atualizada com sucesso!")
        else:
            print(f"❌ Erro ao atualizar senha")
    else:
        print(f"\n📝 Criando novo usuário admin...")
        
        # Criar usuário
        insert_response = supabase.table("usuarios").insert({
            "email": "admin@ativa.com",
            "senha_hash": senha_hash,
            "nome": "Administrador",
            "tipo_usuario": "ADM",
            "ativo": True
        }).execute()
        
        if insert_response.data:
            print(f"✅ Usuário criado com sucesso!")
        else:
            print(f"❌ Erro ao criar usuário")

except Exception as e:
    print(f"❌ Erro: {e}")

print(f"\n📋 Credenciais:")
print(f"   Email: admin@ativa.com")
print(f"   Senha: admin123")
