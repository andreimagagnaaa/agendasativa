import re
import os

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
        return None, None
    
    conteudo = match.group(1).strip()
    return conteudo, None

def parse_file(filepath):
    agendas = []
    consultor_atual = None
    
    with open(filepath, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    for linha in linhas:
        linha = linha.strip()
        
        if not linha:
            continue
        
        # Verificar se é nome de consultor
        if linha and not linha.startswith('-') and not linha.startswith('='):
            if not any(char.isdigit() for char in linha[:20]):
                consultor_atual = linha
                continue
        
        # Processar linha de agenda
        if linha.startswith('-') and consultor_atual:
            data_inicio, data_fim = parse_date_range(linha)
            if not data_inicio:
                continue
            
            projeto, _ = extract_project_info(linha)
            if not projeto:
                continue
            
            agenda = {
                "consultor": consultor_atual,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "projeto": projeto,
                "os": "-" # Valor padrão para OS já que é NOT NULL
            }
            
            agendas.append(agenda)
    
    return agendas

def generate_sql(agendas, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Script gerado automaticamente a partir de GERAL_25112025.txt\n")
        f.write("-- Data de geração: 2025-12-01\n\n")
        
        f.write("-- Limpar tabela (descomente se quiser limpar tudo antes)\n")
        f.write("TRUNCATE TABLE agendas;\n\n")
        
        f.write("INSERT INTO agendas (consultor, data_inicio, data_fim, projeto, os) VALUES\n")
        
        values = []
        for agenda in agendas:
            # Escapar aspas simples no nome do projeto ou consultor
            consultor = agenda['consultor'].replace("'", "''")
            projeto = agenda['projeto'].replace("'", "''")
            os_val = agenda['os'].replace("'", "''")
            
            val = f"('{consultor}', '{agenda['data_inicio']}', '{agenda['data_fim']}', '{projeto}', '{os_val}')"
            values.append(val)
        
        f.write(",\n".join(values))
        f.write(";\n")

if __name__ == "__main__":
    input_path = r"c:\Users\andre\OneDrive\Área de Trabalho\Ativa\agendasativa\agendas_atualizadas.txt"
    output_path = r"c:\Users\andre\OneDrive\Área de Trabalho\Ativa\agendasativa\update_agendas.sql"
    
    if os.path.exists(input_path):
        print(f"Lendo arquivo: {input_path}")
        agendas = parse_file(input_path)
        print(f"Encontradas {len(agendas)} agendas.")
        generate_sql(agendas, output_path)
        print(f"SQL gerado em: {output_path}")

        print("\n--- Agendas da Gerente ou Natália ---")
        for agenda in agendas:
            projeto_upper = agenda['projeto'].upper()
            if "NATALIA" in projeto_upper or "NATÁLIA" in projeto_upper or "GERENTE" in projeto_upper:
                print(f"{agenda['consultor']} | {agenda['data_inicio']} a {agenda['data_fim']} | {agenda['projeto']}")
    else:
        print(f"Arquivo não encontrado: {input_path}")
