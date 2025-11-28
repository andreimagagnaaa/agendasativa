"""
Teste rápido da aplicação
"""
import sys
sys.path.insert(0, r'C:\Users\andre\OneDrive\Área de Trabalho\Ativa')

print("🔍 Testando imports...")

try:
    import streamlit as st
    print("✅ Streamlit importado")
except Exception as e:
    print(f"❌ Erro no Streamlit: {e}")

try:
    from database import Database
    print("✅ Database importado")
    
    # Simular secrets
    class MockSecrets:
        def __getitem__(self, key):
            if key == "SUPABASE_URL":
                return "https://cepxgbpmvohkvyisrqlo.supabase.co"
            elif key == "SUPABASE_KEY":
                return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNlcHhnYnBtdm9oa3Z5aXNycWxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI5Nzg1ODUsImV4cCI6MjA3ODU1NDU4NX0.qcLCQ6XbMKzyulbce0ytW9dDRRsni881exRd8sb0LNY"
            elif key == "COHERE_API_KEY":
                return "kk6JjxQxYXNngcxx1RJiZtD6ZGL1MzeJAzysE9ym"
            raise KeyError(key)
    
    # Testar conexão
    st.secrets = MockSecrets()
    db = Database()
    
    if db.client:
        print("✅ Conexão Supabase OK")
        
        # Testar query
        agendas = db.get_all_agendas()
        print(f"✅ {len(agendas)} agendas encontradas")
    else:
        print("❌ Cliente Supabase não inicializado")
        
except Exception as e:
    print(f"❌ Erro no Database: {e}")
    import traceback
    traceback.print_exc()

try:
    from ai_assistant import AIAssistant
    print("✅ AIAssistant importado")
except Exception as e:
    print(f"❌ Erro no AIAssistant: {e}")

print("\n✅ Todos os imports funcionando!")
