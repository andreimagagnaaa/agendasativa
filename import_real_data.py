"""
Script para importar os dados reais do arquivo GERAL_25052025.txt
"""
import os
import sys
import re
from datetime import datetime
from supabase import create_client, Client

# Ler credenciais do arquivo secrets.toml
import toml

secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
secrets = toml.load(secrets_path)

SUPABASE_URL = secrets["SUPABASE_URL"]
SUPABASE_KEY = secrets["SUPABASE_KEY"]

print(f"🔑 Conectando ao Supabase...")
print(f"🔑 URL: {SUPABASE_URL}\n")

# Criar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def parse_date_range(date_str):
    """
    Converte string de data para formato YYYY-MM-DD
    Exemplos: '03/02 à 07/02', '10/03 à 14/03', '12/03'
    """
    # Extrair datas
    match = re.search(r'(\d{2})/(\d{2})\s*à?\s*(\d{2})?/(\d{2})?', date_str)
    if not match:
        # Tentar formato de data única
        match_single = re.search(r'(\d{2})/(\d{2})', date_str)
        if match_single:
            dia = match_single.group(1)
            mes = match_single.group(2)
            # Determinar ano baseado no mês
            ano = "2025" if int(mes) >= 2 else "2026"
            data = f"{ano}-{mes}-{dia}"
            return data, data
        return None, None
    
    dia_inicio = match.group(1)
    mes_inicio = match.group(2)
    dia_fim = match.group(3) if match.group(3) else dia_inicio
    mes_fim = match.group(4) if match.group(4) else mes_inicio
    
    # Determinar ano baseado no mês
    ano_inicio = "2025" if int(mes_inicio) >= 2 else "2026"
    ano_fim = "2025" if int(mes_fim) >= 2 else "2026"
    
    # Se mês de fim é menor que mês de início, provavelmente mudou de ano
    if int(mes_fim) < int(mes_inicio):
        ano_fim = "2026"
    
    data_inicio = f"{ano_inicio}-{mes_inicio}-{dia_inicio}"
    data_fim = f"{ano_fim}-{mes_fim}-{dia_fim}"
    
    return data_inicio, data_fim

def extract_project_info(texto):
    """
    Extrai informação do projeto do formato: (PROJETO - GERENTE) ou (PROJETO)
    """
    match = re.search(r'\((.*?)\)', texto)
    if not match:
        return None, None, None
    
    conteudo = match.group(1).strip()
    
    # Verificar se é VAGO
    if conteudo.upper() == "VAGO":
        return "VAGO", None, None
    
    # Verificar se tem gerente (formato: PROJETO - GERENTE)
    if ' - ' in conteudo:
        partes = conteudo.split(' - ')
        projeto = partes[0].strip()
        gerente = partes[1].strip()
        return projeto, gerente, False
    else:
        # Apenas projeto
        return conteudo, None, False

def parse_file(filepath):
    """
    Faz o parsing do arquivo GERAL_25052025.txt e retorna lista de agendas
    """
    agendas = []
    consultor_atual = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    for linha in linhas:
        linha = linha.strip()
        
        # Pular linhas vazias
        if not linha:
            continue
        
        # Verificar se é nome de consultor
        if linha and not linha.startswith('-') and not linha.startswith('='):
            # Remover espaços e verificar se não tem números
            if not any(char.isdigit() for char in linha[:20]):
                consultor_atual = linha
                print(f"\n📋 Processando consultor: {consultor_atual}")
                continue
        
        # Processar linha de agenda
        if linha.startswith('-') and consultor_atual:
            # Extrair informações
            data_inicio, data_fim = parse_date_range(linha)
            if not data_inicio:
                continue
            
            projeto, gerente, is_vago = extract_project_info(linha)
            if not projeto:
                continue
            
            is_vago = projeto.upper() == "VAGO"
            
            agenda = {
                "consultor": consultor_atual,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "projeto": projeto,
                "is_vago": is_vago
            }
            
            # Adicionar campos opcionais
            if gerente:
                agenda["gerente"] = gerente
            
            # Para projetos não-VAGO, podemos deixar OS vazio (será opcional)
            
            agendas.append(agenda)
            
            status = "🟢 VAGO" if is_vago else f"📁 {projeto}"
            print(f"  ✓ {data_inicio} a {data_fim}: {status}")
    
    return agendas

def limpar_banco():
    """
    Remove TODAS as agendas do banco (use com cuidado!)
    """
    print("\n⚠️  LIMPANDO BANCO DE DADOS...")
    try:
        # Buscar todas as agendas
        response = supabase.table("agendas").select("id").execute()
        
        if response.data:
            print(f"   Encontradas {len(response.data)} agendas para remover")
            
            # Deletar todas
            for agenda in response.data:
                supabase.table("agendas").delete().eq("id", agenda["id"]).execute()
            
            print(f"   ✓ Banco limpo!\n")
        else:
            print("   ✓ Banco já estava vazio\n")
    except Exception as e:
        print(f"   ❌ Erro ao limpar banco: {e}\n")

def importar_agendas(agendas):
    """
    Importa agendas para o Supabase
    """
    print(f"\n📤 Importando {len(agendas)} agendas...")
    sucesso = 0
    erros = 0
    
    for agenda in agendas:
        try:
            # Adicionar timestamp
            agenda["created_at"] = datetime.now().isoformat()
            
            response = supabase.table("agendas").insert(agenda).execute()
            
            if response.data:
                sucesso += 1
            else:
                erros += 1
                print(f"   ❌ Erro ao inserir: {agenda['consultor']} - {agenda['projeto']}")
        except Exception as e:
            erros += 1
            print(f"   ❌ Erro: {e}")
    
    print(f"\n✅ Importação concluída!")
    print(f"   Sucesso: {sucesso}")
    print(f"   Erros: {erros}")

if __name__ == "__main__":
    # Caminho do arquivo
    arquivo_path = r"c:\Users\andre\OneDrive\Área de Trabalho\Ativa\agendasativa\agendas_atualizadas.txt"
    
    if not os.path.exists(arquivo_path):
        print(f"❌ Arquivo não encontrado: {arquivo_path}")
        sys.exit(1)
    
    print("🚀 Iniciando importação de dados reais...\n")
    
    # Perguntar se deve limpar o banco
    # limpar = input("⚠️  Deseja LIMPAR o banco antes de importar? (s/N): ").strip().lower()
    # if limpar == 's':
    limpar_banco()
    
    # Fazer parsing do arquivo
    print("📖 Lendo arquivo...")
    agendas = parse_file(arquivo_path)
    
    print(f"\n📊 Resumo:")
    print(f"   Total de agendas: {len(agendas)}")
    
    # Contar por consultor
    consultores = {}
    for a in agendas:
        cons = a['consultor']
        consultores[cons] = consultores.get(cons, 0) + 1
    
    for cons, count in sorted(consultores.items()):
        print(f"   - {cons}: {count} agendas")
    
    # Confirmar importação
    # confirmar = input(f"\n✅ Confirma importação de {len(agendas)} agendas? (S/n): ").strip().lower()
    # if confirmar != 'n':
    importar_agendas(agendas)
    # else:
    #     print("❌ Importação cancelada")
