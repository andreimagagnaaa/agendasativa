"""
Script de Teste - Agendas Ativa
Execute este script para verificar se tudo está configurado corretamente
"""

import sys
import os

def test_python_version():
    """Verifica versão do Python"""
    print("🐍 Verificando versão do Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} - Requer Python 3.10+")
        return False

def test_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("\n📦 Verificando dependências...")
    
    dependencies = {
        'streamlit': 'Streamlit',
        'supabase': 'Supabase Client',
        'cohere': 'Cohere AI',
        'pandas': 'Pandas',
        'plotly': 'Plotly',
    }
    
    all_ok = True
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"   ✅ {name} - Instalado")
        except ImportError:
            print(f"   ❌ {name} - NÃO instalado")
            all_ok = False
    
    return all_ok

def test_secrets_file():
    """Verifica se o arquivo de secrets existe"""
    print("\n🔐 Verificando arquivo de secrets...")
    
    secrets_path = os.path.join('.streamlit', 'secrets.toml')
    
    if os.path.exists(secrets_path):
        print(f"   ✅ Arquivo {secrets_path} encontrado")
        
        # Verificar se tem conteúdo
        with open(secrets_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if 'SUPABASE_URL' in content and 'SUPABASE_KEY' in content and 'COHERE_API_KEY' in content:
                print("   ✅ Arquivo contém todas as chaves necessárias")
                
                # Verificar se não são valores de exemplo
                if 'sua-chave' not in content.lower() and 'your' not in content.lower():
                    print("   ✅ Chaves parecem estar configuradas")
                    return True
                else:
                    print("   ⚠️  Chaves ainda não foram configuradas (valores de exemplo)")
                    return False
            else:
                print("   ❌ Arquivo não contém todas as chaves necessárias")
                return False
    else:
        print(f"   ❌ Arquivo {secrets_path} NÃO encontrado")
        print(f"   💡 Crie o arquivo copiando .streamlit/secrets.toml.example")
        return False

def test_database_connection():
    """Verifica conexão com o Supabase"""
    print("\n🗄️  Testando conexão com Supabase...")
    
    try:
        from database import Database
        db = Database()
        
        if db.client is None:
            print("   ❌ Falha ao conectar com Supabase")
            print("   💡 Verifique suas credenciais no arquivo secrets.toml")
            return False
        
        # Tentar buscar agendas
        agendas = db.get_all_agendas()
        print(f"   ✅ Conexão estabelecida - {len(agendas)} agenda(s) encontrada(s)")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao conectar: {str(e)}")
        return False

def test_ai_connection():
    """Verifica conexão com Cohere"""
    print("\n🤖 Testando conexão com Cohere AI...")
    
    try:
        from ai_assistant import AIAssistant
        ai = AIAssistant()
        
        if ai.client is None:
            print("   ❌ Falha ao conectar com Cohere")
            print("   💡 Verifique sua API Key no arquivo secrets.toml")
            return False
        
        print("   ✅ Cliente Cohere inicializado com sucesso")
        return True
        
    except Exception as e:
        print(f"   ❌ Erro ao conectar: {str(e)}")
        return False

def test_files_structure():
    """Verifica se todos os arquivos necessários existem"""
    print("\n📁 Verificando estrutura de arquivos...")
    
    required_files = [
        'app.py',
        'database.py',
        'ai_assistant.py',
        'requirements.txt',
        'README.md',
        'setup_database.sql'
    ]
    
    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NÃO encontrado")
            all_ok = False
    
    return all_ok

def main():
    """Executa todos os testes"""
    print("=" * 60)
    print("🔍 TESTE DE CONFIGURAÇÃO - AGENDAS ATIVA")
    print("=" * 60)
    
    results = []
    
    # Executar testes
    results.append(("Python Version", test_python_version()))
    results.append(("Estrutura de Arquivos", test_files_structure()))
    results.append(("Dependências", test_dependencies()))
    results.append(("Arquivo de Secrets", test_secrets_file()))
    results.append(("Conexão Supabase", test_database_connection()))
    results.append(("Conexão Cohere", test_ai_connection()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name:.<40} {status}")
    
    print("\n" + "=" * 60)
    print(f"Resultado: {passed}/{total} testes passaram")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 TUDO CONFIGURADO CORRETAMENTE!")
        print("Execute: streamlit run app.py")
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("Siga as instruções acima para corrigir os problemas")
        print("Consulte INSTALL.md para ajuda detalhada")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
