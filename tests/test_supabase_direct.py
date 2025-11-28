"""
Teste Direto de Conexão - Supabase
"""
from supabase import create_client

# Credenciais
SUPABASE_URL = "https://cepxgbpmvohkvyisrqlo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNlcHhnYnBtdm9oa3Z5aXNycWxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5Nzg1ODUsImV4cCI6MjA3ODU1NDU4NX0.qcLCQ6XbMKzyulbce0ytW9dDRRsni881exRd8sb0LNY"

print("🔍 Testando conexão direta com Supabase...")
print(f"URL: {SUPABASE_URL}")
print(f"Key: {SUPABASE_KEY[:20]}...")

try:
    # Criar cliente
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Cliente Supabase criado com sucesso!")
    
    # Testar query
    print("\n🔍 Tentando buscar agendas...")
    response = supabase.table("agendas").select("*").execute()
    
    print(f"✅ Conexão bem-sucedida!")
    print(f"📊 Total de agendas: {len(response.data)}")
    
    if response.data:
        print("\n📋 Primeiras agendas:")
        for agenda in response.data[:3]:
            print(f"  • {agenda.get('consultor')} - {agenda.get('projeto')}")
    else:
        print("📭 Nenhuma agenda cadastrada ainda")
    
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    print(f"Tipo do erro: {type(e).__name__}")
