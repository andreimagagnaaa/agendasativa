"""
Script de teste da integração IA
"""
from ai_assistant import AIAssistant
from database import Database

print("🤖 Testando integração com IA...")
print("-" * 50)

# Inicializar
db = Database()
ai = AIAssistant()

# Obter agendas
agendas = db.get_all_agendas()
print(f"📊 {len(agendas)} agendas carregadas do banco")

print("\n🔍 Testando consultas:")
print("-" * 50)

# Teste 1: Consulta de disponibilidade
print("\n1️⃣ Teste: Disponibilidade")
query1 = "André está livre amanhã?"
print(f"   Pergunta: {query1}")
response1 = ai.process_query(query1, agendas)
print(f"   Resposta: {response1[:100]}...")

# Teste 2: Listar agendas
print("\n2️⃣ Teste: Listar agendas")
query2 = "Quais agendas do André?"
print(f"   Pergunta: {query2}")
response2 = ai.process_query(query2, agendas)
print(f"   Resposta: {response2[:100]}...")

# Teste 3: Buscar por projeto
print("\n3️⃣ Teste: Buscar projeto")
query3 = "Agendas do projeto MV"
print(f"   Pergunta: {query3}")
response3 = ai.process_query(query3, agendas)
print(f"   Resposta: {response3[:100]}...")

print("\n" + "-" * 50)
print("✅ Testes de IA concluídos!")
