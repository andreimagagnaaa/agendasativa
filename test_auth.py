"""
Script de teste de autenticação
"""
from auth import AuthManager
from database import Database

db = Database()
auth = AuthManager(db)

print("🔐 Testando autenticação...")
print("-" * 50)

# Testar login
usuario = auth.login('admin@ativa.com', 'admin123')

if usuario:
    print("✅ Login SUCESSO!")
    print(f"   Nome: {usuario['nome']}")
    print(f"   Email: {usuario['email']}")
    print(f"   Tipo: {usuario['tipo_usuario']}")
    print(f"   Ativo: {usuario['ativo']}")
else:
    print("❌ Login FALHOU!")

print("-" * 50)

# Testar métodos do AuthManager
print("\n🔍 Verificando métodos disponíveis:")
print(f"✅ hash_password: {hasattr(auth, 'hash_password')}")
print(f"✅ verify_password: {hasattr(auth, 'verify_password')}")
print(f"✅ login: {hasattr(auth, 'login')}")
print(f"✅ criar_usuario: {hasattr(auth, 'criar_usuario')}")
print(f"✅ check_permission: {hasattr(AuthManager, 'check_permission')}")
