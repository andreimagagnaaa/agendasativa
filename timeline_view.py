"""
Visualização Timeline/Calendário MV - Estilo da imagem
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import Database
from typing import List, Dict

def render_timeline_view(db: Database, mes_selecionado: int = None, ano_selecionado: int = None):
    """
    Renderiza visualização em timeline/calendário estilo MV
    """
    
    # Usar mês/ano atual se não especificado
    hoje = datetime.now()
    mes = mes_selecionado or hoje.month
    ano = ano_selecionado or hoje.year
    
    # Calcular primeiro e último dia do mês
    primeiro_dia = datetime(ano, mes, 1)
    if mes == 12:
        ultimo_dia = datetime(ano, 12, 31)
    else:
        ultimo_dia = datetime(ano, mes + 1, 1) - timedelta(days=1)
    
    # Buscar todas as agendas do período
    agendas = db.get_all_agendas()
    
    # Filtrar agendas que se sobrepõem ao mês selecionado
    agendas_mes = [
        a for a in agendas
        if not (datetime.strptime(a['data_fim'], "%Y-%m-%d").date() < primeiro_dia.date() or
               datetime.strptime(a['data_inicio'], "%Y-%m-%d").date() > ultimo_dia.date())
    ]
    
    # Obter lista de consultores únicos
    consultores = sorted(list(set([a['consultor'] for a in agendas_mes])))
    
    if not consultores:
        st.info("📭 Não há agendas cadastradas para este período.")
        return
    
    # Criar estrutura de dados para o calendário
    dias_mes = (ultimo_dia - primeiro_dia).days + 1
    
    # Criar DataFrame para visualização
    data = []
    
    for consultor in consultores:
        linha = {"Consultor": consultor}
        
        # Para cada dia do mês
        for dia_offset in range(dias_mes):
            dia_atual = primeiro_dia + timedelta(days=dia_offset)
            dia_str = dia_atual.strftime("%d/%m")
            dia_semana = ["SEG", "TER", "QUA", "QUI", "SEX", "SÁB", "DOM"][dia_atual.weekday()]
            
            # Buscar agenda do consultor para este dia
            agenda_dia = None
            for agenda in agendas_mes:
                if agenda['consultor'] == consultor:
                    a_inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").date()
                    a_fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").date()
                    
                    if a_inicio <= dia_atual.date() <= a_fim:
                        agenda_dia = agenda
                        break
            
            # Definir status do dia
            if agenda_dia:
                is_vago = agenda_dia.get('is_vago', False) or agenda_dia.get('projeto', '').upper() in ['VAGO', 'LIVRE']
                
                if is_vago:
                    linha[f"{dia_str}\n{dia_semana}"] = "🟢 LIVRE"
                else:
                    projeto = agenda_dia['projeto']
                    os_info = f" - {agenda_dia['os']}" if agenda_dia.get('os') else ""
                    linha[f"{dia_str}\n{dia_semana}"] = f"🔴 {projeto}{os_info}"
            else:
                linha[f"{dia_str}\n{dia_semana}"] = ""
        
        data.append(linha)
    
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Estilizar e exibir
    st.markdown("### 📅 Visualização Timeline - Estilo MV")
    
    # Controles de navegação
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    
    meses = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    with col1:
        mes_select = st.selectbox(
            "Mês",
            options=list(meses.keys()),
            format_func=lambda x: meses[x],
            index=mes - 1,
            key="timeline_mes"
        )
    
    with col2:
        ano_select = st.selectbox(
            "Ano",
            options=[2024, 2025, 2026, 2027],
            index=1 if ano == 2025 else 0,
            key="timeline_ano"
        )
    
    with col3:
        if st.button("⬅️ Anterior"):
            if mes == 1:
                mes_select = 12
                ano_select = ano - 1
            else:
                mes_select = mes - 1
            st.rerun()
    
    with col4:
        if st.button("Próximo ➡️"):
            if mes == 12:
                mes_select = 1
                ano_select = ano + 1
            else:
                mes_select = mes + 1
            st.rerun()
    
    # Exibir legenda
    st.markdown("**Legenda:** 🟢 Livre/Disponível | 🔴 Ocupado")
    
    # Aplicar estilos CSS personalizados
    st.markdown("""
        <style>
        .timeline-table {
            font-size: 0.8rem;
            border-collapse: collapse;
        }
        .timeline-table th {
            background-color: #002B49;
            color: white;
            padding: 8px;
            text-align: center;
            font-size: 0.7rem;
            border: 1px solid #ddd;
        }
        .timeline-table td {
            padding: 8px;
            border: 1px solid #ddd;
            text-align: center;
            font-size: 0.7rem;
            min-width: 80px;
            max-width: 150px;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .timeline-table td:first-child {
            font-weight: bold;
            text-align: left;
            background-color: #f8f9fa;
            position: sticky;
            left: 0;
            z-index: 1;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Exibir tabela com scroll horizontal
    st.dataframe(
        df,
        use_container_width=True,
        height=600,
        hide_index=True
    )
    
    # Estatísticas
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_dias = dias_mes * len(consultores)
        st.metric("📊 Total Dias", total_dias)
    
    with col2:
        dias_ocupados = sum(1 for a in agendas_mes if not a.get('is_vago', False))
        st.metric("🔴 Dias Ocupados", dias_ocupados)
    
    with col3:
        dias_livres = sum(1 for a in agendas_mes if a.get('is_vago', False))
        st.metric("🟢 Dias Livres", dias_livres)

def render_compact_timeline(db: Database, dias: int = 30):
    """
    Renderiza timeline compacta para próximos X dias
    """
    hoje = datetime.now().date()
    fim = hoje + timedelta(days=dias)
    
    agendas = db.get_all_agendas()
    
    # Filtrar agendas do período
    agendas_periodo = [
        a for a in agendas
        if not (datetime.strptime(a['data_fim'], "%Y-%m-%d").date() < hoje or
               datetime.strptime(a['data_inicio'], "%Y-%m-%d").date() > fim)
    ]
    
    consultores = sorted(list(set([a['consultor'] for a in agendas_periodo])))
    
    st.markdown(f"### 📅 Próximos {dias} dias")
    
    for consultor in consultores:
        with st.expander(f"👤 {consultor}", expanded=False):
            agendas_consultor = [a for a in agendas_periodo if a['consultor'] == consultor]
            
            for agenda in sorted(agendas_consultor, key=lambda x: x['data_inicio']):
                inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").strftime("%d/%m")
                fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").strftime("%d/%m")
                
                is_vago = agenda.get('is_vago', False) or agenda.get('projeto', '').upper() in ['VAGO', 'LIVRE']
                
                if is_vago:
                    st.success(f"🟢 **LIVRE**: {inicio} a {fim}")
                else:
                    os_info = f" (OS: {agenda['os']})" if agenda.get('os') else ""
                    st.error(f"🔴 **{agenda['projeto']}**{os_info}: {inicio} a {fim}")
