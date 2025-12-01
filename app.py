import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from database import Database
from ai_assistant import AIAssistant
from auth import AuthManager
from login_page import show_login_page, show_user_menu, require_auth, require_permission
from timeline_view import render_timeline_view, render_compact_timeline
import plotly.express as px

st.set_page_config(
    page_title="Agendas Ativa",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def load_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {
            --primary: #002B49;
            --primary-dark: #001a2e;
            --primary-light: #004870;
            --secondary: #0066A1;
            --accent: #4A90E2;
            --success: #28a745;
            --warning: #ffc107;
            --danger: #dc3545;
            --info: #17a2b8;
            --light: #f8f9fa;
            --dark: #343a40;
            --gray-100: #f8f9fa;
            --gray-200: #e9ecef;
            --gray-300: #dee2e6;
            --gray-600: #6c757d;
        }
        
        * { 
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            transition: all 0.2s ease;
        }
        
        .block-container { 
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }
        
        /* Typography */
        h1 {
            font-size: 2.25rem !important;
            font-weight: 800 !important;
            color: var(--primary) !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: -0.02em;
        }
        
        h2 {
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: var(--primary) !important;
            margin-top: 1.5rem !important;
        }
        
        h3 {
            font-size: 1.25rem !important;
            font-weight: 600 !important;
            color: var(--primary) !important;
        }
        
        /* Stat Cards - Modern Glassmorphism */
        .stat-card {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            padding: 1.75rem;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 43, 73, 0.12);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }
        
        .stat-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--accent) 0%, var(--secondary) 100%);
        }
        
        .stat-card h3 {
            color: rgba(255, 255, 255, 0.85) !important;
            margin: 0 0 0.75rem 0 !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
        
        .stat-card p {
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 800;
            line-height: 1;
        }
        
        .stat-card .stat-subtitle {
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }
        
        /* Chat Messages - Enhanced */
        .user-message {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            padding: 1.25rem 1.5rem;
            border-radius: 16px 16px 4px 16px;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0, 43, 73, 0.15);
            max-width: 85%;
            margin-left: auto;
        }
        
        .ai-message {
            background: white;
            color: var(--dark);
            padding: 1.25rem 1.5rem;
            border-radius: 16px 16px 16px 4px;
            margin: 1rem 0;
            border: 1px solid var(--gray-200);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            max-width: 85%;
        }
        
        .ai-message h3, .ai-message h4 {
            color: var(--primary) !important;
            margin-top: 1rem !important;
        }
        
        /* Buttons - Modern & Polished */
        .stButton>button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 12px;
            font-weight: 600;
            border: none;
            box-shadow: 0 4px 12px rgba(0, 43, 73, 0.2);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-transform: none;
            letter-spacing: 0.02em;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 43, 73, 0.3);
        }
        
        .stButton>button:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(0, 43, 73, 0.2);
        }
        
        /* Secondary Buttons */
        .stButton>button[kind="secondary"] {
            background: white;
            color: var(--primary);
            border: 2px solid var(--primary);
        }
        
        .stButton>button[kind="secondary"]:hover {
            background: var(--primary);
            color: white;
        }
        
        /* Input Fields - Refined */
        .stTextInput>div>div>input,
        .stTextArea>div>div>textarea,
        .stSelectbox>div>div>select,
        .stNumberInput>div>div>input {
            border-radius: 12px;
            border: 2px solid var(--gray-200);
            padding: 0.75rem 1rem;
            font-size: 0.95rem;
            transition: all 0.3s;
        }
        
        .stTextInput>div>div>input:focus,
        .stTextArea>div>div>textarea:focus,
        .stSelectbox>div>div>select:focus,
        .stNumberInput>div>div>input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(0, 43, 73, 0.1);
        }
        
        /* Agenda Cards - Premium Design */
        .agenda-card {
            background: white;
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid var(--gray-200);
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .agenda-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: linear-gradient(180deg, var(--primary) 0%, var(--accent) 100%);
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        .agenda-card:hover {
            border-color: var(--primary);
            box-shadow: 0 8px 24px rgba(0, 43, 73, 0.12);
            transform: translateY(-4px);
        }
        
        .agenda-card:hover::before {
            opacity: 1;
        }
        
        .agenda-card-header {
            color: var(--primary);
            font-weight: 700;
            font-size: 1.15rem;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .agenda-card-info {
            color: var(--gray-600);
            font-size: 0.9rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Status Badges - Enhanced */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.35rem 0.85rem;
            border-radius: 24px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .status-andamento { 
            background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
            color: white;
        }
        .status-agendado { 
            background: linear-gradient(135deg, #28a745 0%, #218838 100%);
            color: white;
        }
        .status-concluido { 
            background: linear-gradient(135deg, #6c757d 0%, #545b62 100%);
            color: white;
        }
        .status-livre {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
        }
        .status-ocupado {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            color: white;
        }
        
        /* Tabs - Modern Design */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background-color: var(--gray-100);
            padding: 0.5rem;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: auto;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            background-color: transparent;
            font-weight: 600;
            color: var(--gray-600);
        }
        
        .stTabs [aria-selected="true"] {
            background: white !important;
            color: var(--primary) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }
        
        /* Expander - Refined */
        .streamlit-expanderHeader {
            background-color: var(--gray-100);
            border-radius: 12px;
            padding: 1rem 1.25rem;
            font-weight: 600;
            border: 1px solid var(--gray-200);
        }
        
        .streamlit-expanderHeader:hover {
            background-color: white;
            border-color: var(--primary);
        }
        
        /* DataFrames - Clean */
        .dataframe {
            border: none !important;
            font-size: 0.9rem;
        }
        
        .dataframe thead tr th {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 1rem !important;
            border: none !important;
        }
        
        .dataframe tbody tr:hover {
            background-color: var(--gray-100) !important;
        }
        
        /* Loading Animation */
        .stSpinner>div {
            border-top-color: var(--primary) !important;
        }
        
        /* Success/Error/Warning Messages */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 12px;
            padding: 1rem 1.25rem;
            border: none;
        }
        
        /* Metric Cards */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 800;
            color: var(--primary);
        }
        
        /* Sidebar - Modern */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--gray-100) 0%, white 100%);
        }
        
        /* Remove anchor links */
        .stMarkdown a[href^="#"] {
            display: none !important;
        }
        
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
            display: none !important;
        }
        
        /* Tooltip */
        [data-testid="stTooltipIcon"] {
            color: var(--primary);
        }
        
        /* Form */
        [data-testid="stForm"] {
            background: var(--gray-100);
            padding: 1.5rem;
            border-radius: 16px;
            border: 1px solid var(--gray-200);
        }
        
        /* Quick Actions Grid */
        .quick-action {
            background: white;
            padding: 1.25rem;
            border-radius: 12px;
            border: 2px solid var(--gray-200);
            text-align: center;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .quick-action:hover {
            border-color: var(--primary);
            box-shadow: 0 4px 12px rgba(0, 43, 73, 0.12);
            transform: translateY(-2px);
        }
        
        .quick-action-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        /* Progress Bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
            border-radius: 8px;
        }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: var(--gray-100);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--gray-300);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--gray-600);
        }
        </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def init_database():
    return Database()

@st.cache_resource
def init_ai():
    return AIAssistant()

def main():
    load_custom_css()
    
    db = init_database()
    ai = init_ai()
    
    # Verificar autenticação
    if not require_auth():
        show_login_page(db)
        return
    
    # Menu do usuário
    show_user_menu()
    
    # Obter dados do usuário logado
    usuario = st.session_state.usuario
    tipo_usuario = usuario['tipo_usuario']
    
    # Header com informações do usuário
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown("# 📅 Agendas Ativa")
        st.caption(f"👋 Olá, **{usuario['nome']}** - Acesso: {tipo_usuario}")
    with col2:
        hoje = datetime.now()
        st.metric("📅 Data", hoje.strftime("%d/%m/%Y"), delta=hoje.strftime("%A"))
    with col3:
        agendas_hoje = len([a for a in db.get_all_agendas() if 
                           datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() <= hoje.date() <= 
                           datetime.strptime(a['data_fim'], '%Y-%m-%d').date()])
        st.metric("🔥 Ativas Hoje", agendas_hoje)
    
    st.markdown("---")
    
    # Criar tabs baseadas nas permissões
    if tipo_usuario == "CL_MV":
        # Visualização MV - apenas timeline
        tab1 = st.tabs(["📅 Visualização MV (Timeline)"])[0]
        with tab1:
            timeline_mv_page(db)
    elif tipo_usuario == "CONSULTOR":
        # Consultor - apenas sua agenda
        tab1, tab2 = st.tabs(["📋 Minha Agenda", "💬 Assistente IA"])
        with tab1:
            consultor_agenda_page(db, usuario)
        with tab2:
            chat_page(db, ai, usuario)
    else:  # ADM
        # Admin - acesso completo
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💬 Assistente IA", 
            "📊 Dashboard", 
            "📅 Timeline MV", 
            "👥 Usuários",
            "⚙️ Configurações"
        ])
        with tab1:
            chat_page(db, ai, usuario)
        with tab2:
            dashboard_page(db)
        with tab3:
            timeline_mv_page(db)
        with tab4:
            usuarios_page(db)
        with tab5:
            config_page(db)

def chat_page(db, ai, usuario=None):
    """Página de chat com assistente IA - Interface Melhorada"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Header do Chat
    st.markdown("### 🤖 Assistente Inteligente de Agendas")
    st.caption("Pergunte sobre disponibilidade, agendas, conflitos e muito mais!")
    
    # Obter agendas para usar no formulário e consultas
    agendas = db.get_all_agendas()
    
    # Cards de Estatísticas Rápidas
    col1, col2, col3, col4 = st.columns(4)
    hoje = datetime.now().date()
    
    ativas = [a for a in agendas if datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() <= hoje <= datetime.strptime(a['data_fim'], '%Y-%m-%d').date()]
    proximas = [a for a in agendas if datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() > hoje]
    consultores_ativos = len(set([a['consultor'] for a in ativas]))
    
    with col1:
        st.markdown(f'<div class="stat-card"><h3>Total</h3><p>{len(agendas)}</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><h3>Ativas</h3><p>{len(ativas)}</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><h3>Próximas</h3><p>{len(proximas)}</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="stat-card"><h3>Consultores</h3><p>{consultores_ativos}</p></div>', unsafe_allow_html=True)
    
    st.markdown("##")
    
    # Formulário rápido para nova agenda - Melhorado
    with st.expander("➕ Nova Agenda Rápida", expanded=False):
        st.markdown("##### Criar nova agenda de forma rápida")
        
        consultores_existentes = sorted(set([a['consultor'] for a in agendas])) if agendas else []
        projetos_existentes = sorted(set([a['projeto'] for a in agendas])) if agendas else []
        gerentes_existentes = sorted(set([a.get('gerente', '') for a in agendas if a.get('gerente')])) if agendas else []
        
        with st.form("quick_agenda_form"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                consultor_opcao = st.selectbox(
                    "👤 Consultor",
                    ['📝 Novo consultor...'] + consultores_existentes,
                    key="quick_consultor_select"
                )
                
                if consultor_opcao == '📝 Novo consultor...':
                    consultor = st.text_input("Nome do Consultor", key="quick_consultor_new", placeholder="Digite o nome...")
                else:
                    consultor = consultor_opcao
                
                projeto_opcao = st.selectbox(
                    "📁 Projeto",
                    ['📝 Novo projeto...'] + projetos_existentes,
                    key="quick_projeto_select"
                )
                
                if projeto_opcao == '📝 Novo projeto...':
                    projeto = st.text_input("Nome do Projeto", key="quick_projeto_new", placeholder="Digite o projeto...")
                else:
                    projeto = projeto_opcao
            
            with col2:
                os_num = st.text_input("📋 OS (opcional)", key="quick_os", placeholder="Número da OS")
                
                gerente_opcao = st.selectbox(
                    "👔 Gerente (opcional)",
                    ['Nenhum'] + ['📝 Novo gerente...'] + gerentes_existentes,
                    key="quick_gerente_select"
                )
                
                if gerente_opcao == '📝 Novo gerente...':
                    gerente = st.text_input("Nome do Gerente", key="quick_gerente_new", placeholder="Digite o nome...")
                elif gerente_opcao == 'Nenhum':
                    gerente = None
                else:
                    gerente = gerente_opcao
            
            with col3:
                data_inicio = st.date_input("📅 Data Início", key="quick_inicio", value=datetime.now().date())
                data_fim = st.date_input("📅 Data Fim", key="quick_fim", value=datetime.now().date() + timedelta(days=7))
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
            with col_btn2:
                submit_agenda = st.form_submit_button("💾 Criar Agenda", use_container_width=True)
            
            if submit_agenda:
                if consultor and projeto:
                    if data_fim < data_inicio:
                        st.error("❌ Data fim deve ser posterior à data início")
                    else:
                        # Verificar conflitos
                        conflito = db._check_conflito(consultor, data_inicio.strftime('%Y-%m-%d'), data_fim.strftime('%Y-%m-%d'))
                        
                        if conflito:
                            st.warning(f"⚠️ Atenção: {consultor} já possui agenda neste período - {conflito['projeto']}")
                        
                        if db.create_agenda(
                            consultor=consultor,
                            data_inicio=data_inicio.strftime('%Y-%m-%d'),
                            data_fim=data_fim.strftime('%Y-%m-%d'),
                            projeto=projeto,
                            os=os_num if os_num else None,
                            gerente=gerente
                        ):
                            st.success(f"✅ Agenda criada com sucesso: **{consultor}** → **{projeto}**")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Erro ao criar agenda")
                else:
                    st.warning("⚠️ Preencha pelo menos Consultor e Projeto")
    
    st.markdown("##")
    
    # Templates de Perguntas Rápidas - Melhorado
    st.markdown("### ⚡ Perguntas Rápidas")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Ver Resumo Geral", use_container_width=True, help="Resumo completo de todas as agendas"):
            hoje = datetime.now().date()
            ativas = [a for a in agendas if datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() <= hoje <= datetime.strptime(a['data_fim'], '%Y-%m-%d').date()]
            futuras = [a for a in agendas if datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() > hoje]
            passadas = [a for a in agendas if datetime.strptime(a['data_fim'], '%Y-%m-%d').date() < hoje]
            
            response = f"### 📊 Resumo Geral de Agendas\n\n"
            response += f"📈 **Total de Agendas:** {len(agendas)}\n\n"
            response += f"🟢 **Em Andamento:** {len(ativas)}\n\n"
            response += f"🔵 **Futuras:** {len(futuras)}\n\n"
            response += f"⚫ **Concluídas:** {len(passadas)}\n\n"
            response += f"---\n\n"
            response += f"👥 **Consultores Ativos:** {len(set([a['consultor'] for a in ativas]))}\n\n"
            response += f"📁 **Projetos Cadastrados:** {len(set([a['projeto'] for a in agendas]))}\n\n"
            
            st.session_state.chat_history.append({'role': 'user', 'content': '📊 Ver Resumo Geral'})
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col2:
        if st.button("📅 Agendas de Hoje", use_container_width=True, help="Ver todas as agendas ativas hoje"):
            query = f"Quais agendas estão ativas hoje {hoje.strftime('%d/%m/%Y')}?"
            st.session_state.chat_history.append({'role': 'user', 'content': query})
            
            with st.spinner("🤖 Processando..."):
                response_data = ai.process_query(query, agendas)
            
            if isinstance(response_data, dict):
                response = response_data.get("text", "")
            else:
                response = str(response_data)
            
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col3:
        if st.button("🔜 Próximos 7 Dias", use_container_width=True, help="Agendas dos próximos 7 dias"):
            fim_periodo = hoje + timedelta(days=7)
            query = f"Quais agendas começam entre {hoje.strftime('%d/%m/%Y')} e {fim_periodo.strftime('%d/%m/%Y')}?"
            st.session_state.chat_history.append({'role': 'user', 'content': query})
            
            with st.spinner("🤖 Processando..."):
                response_data = ai.process_query(query, agendas)
            
            if isinstance(response_data, dict):
                response = response_data.get("text", "")
            else:
                response = str(response_data)
            
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col4:
        if st.button("🔍 Buscar Consultor", use_container_width=True, help="Buscar agendas por consultor"):
            st.session_state.show_search_form = not st.session_state.get('show_search_form', False)
            st.rerun()
    
    # Formulário de busca avançada
    if st.session_state.get('show_search_form', False):
        with st.container():
            st.markdown("##### 🔍 Busca Avançada")
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                consultores_list = ['Todos'] + sorted(list(set([a['consultor'] for a in agendas])))
                busca_consultor = st.selectbox("👤 Consultor", consultores_list, key="busca_cons")
            
            with col2:
                projetos_list = ['Todos'] + sorted(list(set([a['projeto'] for a in agendas])))
                busca_projeto = st.selectbox("📁 Projeto", projetos_list, key="busca_proj")
            
            with col3:
                st.markdown("##")
                if st.button("🔍 Buscar", use_container_width=True):
                    query = f"Buscar agendas"
                    if busca_consultor != 'Todos':
                        query += f" do consultor {busca_consultor}"
                    if busca_projeto != 'Todos':
                        query += f" do projeto {busca_projeto}"
                    
                    st.session_state.chat_history.append({'role': 'user', 'content': query})
                    
                    with st.spinner("🤖 Processando..."):
                        response_data = ai.process_query(query, agendas)
                    
                    if isinstance(response_data, dict):
                        response = response_data.get("text", "")
                    else:
                        response = str(response_data)
                    
                    st.session_state.chat_history.append({'role': 'assistant', 'content': response})
                    st.session_state.show_search_form = False
                    st.rerun()
    
    st.markdown("---")
    
    # Templates rápidos
    st.markdown("### ⚡ Ações Rápidas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Ver Todas", use_container_width=True, help="Ver resumo de todas as agendas"):
            hoje = datetime.now().date()
            ativas = [a for a in agendas if datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() <= hoje <= datetime.strptime(a['data_fim'], '%Y-%m-%d').date()]
            futuras = [a for a in agendas if datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() > hoje]
            passadas = [a for a in agendas if datetime.strptime(a['data_fim'], '%Y-%m-%d').date() < hoje]
            
            response = f"### 📊 Resumo Geral de Agendas\n\n"
            response += f"---\n\n"
            response += f"📈 **Total de Agendas:** {len(agendas)}\n\n"
            response += f"🟢 **Em Andamento:** {len(ativas)}\n\n"
            response += f"🔵 **Agendadas:** {len(futuras)}\n\n"
            response += f"⚫ **Concluídas:** {len(passadas)}\n\n"
            response += f"---\n\n"
            response += f"👥 **Consultores Ativos:** {len(set([a['consultor'] for a in agendas]))}\n\n"
            response += f"📁 **Projetos Cadastrados:** {len(set([a['projeto'] for a in agendas]))}\n\n"
            response += f"---\n\n"
            response += "💡 _Para visualizar detalhes completos, filtros avançados e gráficos, acesse a aba **Dashboard**._"
            
            st.session_state.chat_history.append({'role': 'user', 'content': '📊 Ver Todas'})
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col2:
        if st.button("📅 Agendas Ativas", use_container_width=True, help="Ver agendas em andamento hoje"):
            hoje = datetime.now().date()
            ativas = [a for a in agendas if datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() <= hoje <= datetime.strptime(a['data_fim'], '%Y-%m-%d').date()]
            
            if not ativas:
                response = "📭 Não há agendas ativas hoje."
            else:
                response = f"### 📅 Agendas Ativas Hoje\n\n"
                response += f"📆 **Data:** {hoje.strftime('%d/%m/%Y')}\n\n"
                response += f"---\n\n"
                response += f"🟢 **Total:** {len(ativas)} em andamento\n\n"
                response += f"---\n\n"
                
                # Agrupar por consultor
                consultores = {}
                for a in ativas:
                    cons = a['consultor']
                    if cons not in consultores:
                        consultores[cons] = []
                    consultores[cons].append(a)
                
                for cons, ags in sorted(consultores.items()):
                    response += f"#### 👤 {cons}\n\n"
                    response += f"**Total ativo:** {len(ags)}\n\n"
                    for ag in ags[:5]:  # Limitar a 5 por consultor
                        inicio = datetime.strptime(ag['data_inicio'], '%Y-%m-%d').strftime('%d/%m/%Y')
                        fim = datetime.strptime(ag['data_fim'], '%Y-%m-%d').strftime('%d/%m/%Y')
                        dias_restantes = (datetime.strptime(ag['data_fim'], '%Y-%m-%d').date() - hoje).days
                        response += f"• **Projeto:** {ag['projeto']}\n"
                        response += f"  **OS:** {ag['os']}\n"
                        response += f"  📅 **Período:** {inicio} até {fim}\n"
                        response += f"  ⏱️ **Restam:** {dias_restantes} dia(s)\n\n"
                    response += "---\n\n"
                
                response += "💡 _Acesse o **Dashboard** para ver todos os detalhes._"
            
            st.session_state.chat_history.append({'role': 'user', 'content': '📅 Agendas Ativas'})
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    with col3:
        if st.button("🔜 Próximas Agendas", use_container_width=True, help="Ver agendas dos próximos 7 dias"):
            hoje = datetime.now().date()
            fim_periodo = hoje + timedelta(days=7)
            proximas = [a for a in agendas if hoje < datetime.strptime(a['data_inicio'], '%Y-%m-%d').date() <= fim_periodo]
            
            if not proximas:
                response = "📭 Não há agendas programadas para os próximos 7 dias."
            else:
                response = f"### 🔜 Próximas Agendas (7 dias)\n\n"
                response += f"📅 **Período:** {hoje.strftime('%d/%m/%Y')} a {fim_periodo.strftime('%d/%m/%Y')}\n\n"
                response += f"---\n\n"
                response += f"🔵 **Total programado:** {len(proximas)}\n\n"
                response += f"---\n\n"
                
                # Ordenar por data de início
                proximas_sorted = sorted(proximas, key=lambda x: x['data_inicio'])
                
                # Agrupar por consultor
                consultores = {}
                for a in proximas_sorted:
                    cons = a['consultor']
                    if cons not in consultores:
                        consultores[cons] = []
                    consultores[cons].append(a)
                
                for cons, ags in sorted(consultores.items()):
                    response += f"#### 👤 {cons}\n\n"
                    response += f"**Total programado:** {len(ags)}\n\n"
                    for ag in ags[:5]:  # Limitar a 5 por consultor
                        inicio = datetime.strptime(ag['data_inicio'], '%Y-%m-%d')
                        fim = datetime.strptime(ag['data_fim'], '%Y-%m-%d')
                        dias_ate = (inicio.date() - hoje).days
                        response += f"• **Projeto:** {ag['projeto']}\n"
                        response += f"  **OS:** {ag['os']}\n"
                        response += f"  📅 **Período:** {inicio.strftime('%d/%m/%Y')} até {fim.strftime('%d/%m/%Y')}\n"
                        response += f"  ⏰ **Começa em:** {dias_ate} dia(s)\n\n"
                    response += "---\n\n"
                
                response += "💡 _Acesse o **Dashboard** para ver todos os detalhes._"
            
            st.session_state.chat_history.append({'role': 'user', 'content': '🔜 Próximas Agendas'})
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    st.markdown("---")
    
    # Histórico de chat
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history[-10:]:  # Mostrar últimas 10 mensagens
            if message['role'] == 'user':
                st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Input de mensagem
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Mensagem",
            key="chat_input",
            placeholder="Digite sua pergunta (ex: João está livre amanhã?)",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Enviar", use_container_width=True)
    
    with col3:
        if st.button("🗑️", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    if send_button and user_input:
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        
        with st.spinner("..."):
            response_data = ai.process_query(user_input, agendas)
        
        # Extrair texto e ação
        if isinstance(response_data, dict):
            response_text = response_data.get("text", "")
            action = response_data.get("action")
        else:
            response_text = str(response_data)
            action = None
        
        st.session_state.chat_history.append({'role': 'assistant', 'content': response_text})
        
        if action:
            st.session_state.pending_action = action
        else:
            if 'pending_action' in st.session_state:
                del st.session_state.pending_action
                
        st.rerun()

    # Renderizar botão de ação se houver
    if 'pending_action' in st.session_state:
        action = st.session_state.pending_action
        if action['type'] == 'create_agenda':
            data = action['data']
            st.info("👇 Confirme a criação da agenda abaixo:")
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("✅ Confirmar Agendamento", use_container_width=True, type="primary"):
                    if db.create_agenda(
                        consultor=data['consultor'],
                        data_inicio=data['data_inicio'],
                        data_fim=data['data_fim'],
                        projeto=data['projeto'],
                        os=data['os']
                    ):
                        st.success("✅ Agenda criada com sucesso!")
                        st.session_state.chat_history.append({'role': 'assistant', 'content': "✅ Agenda criada com sucesso!"})
                        del st.session_state.pending_action
                        st.rerun()
            with col_act2:
                if st.button("❌ Cancelar", use_container_width=True):
                    st.warning("Operação cancelada.")
                    del st.session_state.pending_action
                    st.rerun()

def dashboard_page(db):
    agendas = db.get_all_agendas()
    
    if not agendas:
        st.info("Nenhuma agenda cadastrada")
        
        # Botão para ir ao chat
        if st.button("➕ Criar Primeira Agenda"):
            st.session_state.active_tab = "chat"
            st.rerun()
        return
    
    df = pd.DataFrame(agendas)
    df['data_inicio'] = pd.to_datetime(df['data_inicio'])
    df['data_fim'] = pd.to_datetime(df['data_fim'])
    
    hoje = datetime.now().date()
    
    # KPIs principais
    col1, col2, col3, col4 = st.columns(4)
    
    ativas = df[(df['data_inicio'].dt.date <= hoje) & (df['data_fim'].dt.date >= hoje)]
    proximas = df[df['data_inicio'].dt.date > hoje]
    
    with col1:
        st.markdown(f'<div class="stat-card"><h3>Total</h3><p>{len(df)}</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="stat-card"><h3>Ativas</h3><p>{len(ativas)}</p></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="stat-card"><h3>Próximas</h3><p>{len(proximas)}</p></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'<div class="stat-card"><h3>Consultores</h3><p>{df["consultor"].nunique()}</p></div>', unsafe_allow_html=True)
    
    st.markdown("##")
    
    # Filtros rápidos
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    
    with col1:
        consultores = ['Todos'] + sorted(df['consultor'].unique().tolist())
        selected_consultor = st.selectbox("👤 Consultor", consultores, key="dash_consultor")
    
    with col2:
        projetos = ['Todos'] + sorted(df['projeto'].unique().tolist())
        selected_projeto = st.selectbox("📁 Projeto", projetos, key="dash_projeto")
    
    with col3:
        status_opcoes = ["Todas", "Próximas", "Em Andamento", "Concluídas"]
        selected_status = st.selectbox("🟢 Status", status_opcoes, key="dash_status")
    
    with col4:
        periodo = st.selectbox(
            "📅 Período",
            ["Todos", "Hoje", "Esta Semana", "Este Mês", "Próximos 7 Dias", "Próximos 30 Dias", "📅 Período Personalizado"],
            key="dash_periodo"
        )
    
    with col5:
        st.markdown("##")
        if st.button("🔄", use_container_width=True, help="Atualizar dados"):
            st.rerun()
    
    # Se período personalizado, mostrar seletores de data
    data_inicio_filtro = None
    data_fim_filtro = None
    
    if periodo == "📅 Período Personalizado":
        col_data1, col_data2 = st.columns(2)
        with col_data1:
            data_inicio_filtro = st.date_input(
                "Data Início",
                value=hoje,
                key="filtro_data_inicio"
            )
        with col_data2:
            data_fim_filtro = st.date_input(
                "Data Fim",
                value=hoje + timedelta(days=30),
                key="filtro_data_fim"
            )
    
    df_filtered = df.copy()
    
    if selected_consultor != 'Todos':
        df_filtered = df_filtered[df_filtered['consultor'] == selected_consultor]
    
    if selected_projeto != 'Todos':
        df_filtered = df_filtered[df_filtered['projeto'] == selected_projeto]
    
    # Aplicar filtro de status
    if selected_status == "Próximas":
        df_filtered = df_filtered[df_filtered['data_inicio'].dt.date > hoje]
    elif selected_status == "Em Andamento":
        df_filtered = df_filtered[
            (df_filtered['data_inicio'].dt.date <= hoje) & 
            (df_filtered['data_fim'].dt.date >= hoje)
        ]
    elif selected_status == "Concluídas":
        df_filtered = df_filtered[df_filtered['data_fim'].dt.date < hoje]
    
    # Aplicar filtros de período (corrigidos para puxar apenas datas corretas)
    if periodo == "Hoje":
        df_filtered = df_filtered[
            (df_filtered['data_inicio'].dt.date <= hoje) & 
            (df_filtered['data_fim'].dt.date >= hoje)
        ]
    elif periodo == "Esta Semana":
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        fim_semana = inicio_semana + timedelta(days=6)
        df_filtered = df_filtered[
            (df_filtered['data_fim'].dt.date >= inicio_semana) & 
            (df_filtered['data_inicio'].dt.date <= fim_semana)
        ]
    elif periodo == "Este Mês":
        inicio_mes = hoje.replace(day=1)
        if hoje.month == 12:
            fim_mes = hoje.replace(day=31)
        else:
            fim_mes = (hoje.replace(month=hoje.month + 1, day=1) - timedelta(days=1))
        df_filtered = df_filtered[
            (df_filtered['data_fim'].dt.date >= inicio_mes) & 
            (df_filtered['data_inicio'].dt.date <= fim_mes)
        ]
    elif periodo == "Próximos 7 Dias":
        fim_7_dias = hoje + timedelta(days=7)
        df_filtered = df_filtered[
            (df_filtered['data_inicio'].dt.date >= hoje) & 
            (df_filtered['data_inicio'].dt.date <= fim_7_dias)
        ]
    elif periodo == "Próximos 30 Dias":
        fim_30_dias = hoje + timedelta(days=30)
        df_filtered = df_filtered[
            (df_filtered['data_inicio'].dt.date >= hoje) & 
            (df_filtered['data_inicio'].dt.date <= fim_30_dias)
        ]
    elif periodo == "📅 Período Personalizado" and data_inicio_filtro and data_fim_filtro:
        df_filtered = df_filtered[
            (df_filtered['data_fim'].dt.date >= data_inicio_filtro) & 
            (df_filtered['data_inicio'].dt.date <= data_fim_filtro)
        ]
    
    st.markdown("##")
    
    if len(df_filtered) == 0:
        st.warning("⚠️ Nenhuma agenda encontrada com os filtros aplicados")
        return
    
    st.markdown(f"**{len(df_filtered)}** agenda(s) • **{df_filtered['consultor'].nunique()}** consultor(es) • **{df_filtered['projeto'].nunique()}** projeto(s)")
    
    tabs = st.tabs(["📇 Cards", "📊 Tabela", "📈 Gráficos"])
    
    with tabs[0]:
        df_display = df_filtered.sort_values('data_inicio', ascending=False)
        
        # Agrupar por status
        hoje = datetime.now().date()
        em_andamento = []
        agendados = []
        concluidos = []
        
        for idx, row in df_display.iterrows():
            data_inicio = row['data_inicio'].date()
            data_fim = row['data_fim'].date()
            
            if data_inicio <= hoje <= data_fim:
                em_andamento.append((idx, row))
            elif data_inicio > hoje:
                agendados.append((idx, row))
            else:
                concluidos.append((idx, row))
        
        # Mostrar em andamento primeiro
        if em_andamento:
            st.markdown("### 🔵 Em Andamento")
            for idx, row in em_andamento:
                col1, col2 = st.columns([5, 1])
                with col1:
                    dias_restantes = (row['data_fim'].date() - hoje).days
                    st.markdown(f"""
                        <div class="agenda-card">
                            <div class="agenda-card-header">
                                👤 {row['consultor']}
                                <span class="status-andamento status-badge">ATIVO • {dias_restantes}d restantes</span>
                            </div>
                            <div class="agenda-card-info">
                                📁 {row['projeto']} • 📋 OS: {row['os']}
                            </div>
                            <div class="agenda-card-info">
                                📅 {row['data_inicio'].date().strftime('%d/%m/%Y')} → {row['data_fim'].date().strftime('%d/%m/%Y')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("🗑️", key=f"del_{idx}", help="Excluir agenda"):
                        if db.delete_agenda(row['id']):
                            st.rerun()
        
        # Agendados
        if agendados:
            st.markdown("### 🟢 Agendados")
            for idx, row in agendados[:5]:  # Limitar a 5 para não poluir
                col1, col2 = st.columns([5, 1])
                with col1:
                    dias_ate = (row['data_inicio'].date() - hoje).days
                    st.markdown(f"""
                        <div class="agenda-card">
                            <div class="agenda-card-header">
                                👤 {row['consultor']}
                                <span class="status-agendado status-badge">Em {dias_ate}d</span>
                            </div>
                            <div class="agenda-card-info">
                                📁 {row['projeto']} • 📋 OS: {row['os']}
                            </div>
                            <div class="agenda-card-info">
                                📅 {row['data_inicio'].date().strftime('%d/%m/%Y')} → {row['data_fim'].date().strftime('%d/%m/%Y')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("🗑️", key=f"del_{idx}", help="Excluir agenda"):
                        if db.delete_agenda(row['id']):
                            st.rerun()
            
            if len(agendados) > 5:
                st.info(f"+ {len(agendados) - 5} agendas futuras. Use os filtros para ver mais.")
        
        # Concluídos (opcional, colapsado)
        if concluidos and st.checkbox(f"Mostrar {len(concluidos)} agendas concluídas"):
            st.markdown("### ⚫ Concluídos")
            for idx, row in concluidos[:10]:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"""
                        <div class="agenda-card">
                            <div class="agenda-card-header">
                                👤 {row['consultor']}
                                <span class="status-concluido status-badge">CONCLUÍDO</span>
                            </div>
                            <div class="agenda-card-info">
                                📁 {row['projeto']} • 📋 OS: {row['os']}
                            </div>
                            <div class="agenda-card-info">
                                📅 {row['data_inicio'].date().strftime('%d/%m/%Y')} → {row['data_fim'].date().strftime('%d/%m/%Y')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button("🗑️", key=f"del_{idx}", help="Excluir agenda"):
                        if db.delete_agenda(row['id']):
                            st.rerun()
    
    with tabs[1]:
        if len(df_filtered) == 0:
            st.warning("Nenhuma agenda encontrada")
        else:
            # Preparar tabela
            df_table = df_filtered.copy()
            df_table['Data Início'] = df_table['data_inicio'].dt.strftime('%d/%m/%Y')
            df_table['Data Fim'] = df_table['data_fim'].dt.strftime('%d/%m/%Y')
            df_table['Dias'] = (df_table['data_fim'] - df_table['data_inicio']).dt.days + 1
            
            # Calcular status
            def get_status(row):
                data_inicio = row['data_inicio'].date()
                data_fim = row['data_fim'].date()
                if data_inicio <= hoje <= data_fim:
                    return "🔵 Em Andamento"
                elif data_inicio > hoje:
                    return "🟢 Agendado"
                else:
                    return "⚫ Concluído"
            
            df_table['Status'] = df_table.apply(get_status, axis=1)
            
            # Adicionar colunas de detalhes
            df_table['Horas'] = df_table.apply(lambda x: f"{x.get('horas_cliente', 0) or 0}h" if x.get('horas_cliente') else "-", axis=1)
            df_table['Entrega'] = df_table.apply(lambda x: (x.get('descricao_entrega', '') or '')[:50] + '...' if len(x.get('descricao_entrega', '') or '') > 50 else (x.get('descricao_entrega', '') or '-'), axis=1)
            
            # Selecionar e ordenar colunas
            df_display = df_table[['Status', 'consultor', 'projeto', 'os', 'Data Início', 'Data Fim', 'Dias', 'Horas', 'Entrega']]
            df_display.columns = ['Status', 'Consultor', 'Projeto', 'OS', 'Início', 'Fim', 'Dias', 'Horas', 'Entrega']
            df_display = df_display.sort_values('Início', ascending=False)
            
            st.dataframe(
                df_display,
                use_container_width=True,
                hide_index=True,
                height=500
            )
            
            # Botão de exportação
            csv = df_display.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Exportar CSV",
                data=csv,
                file_name=f"agendas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with tabs[2]:
        if len(df_filtered) == 0:
            st.warning("Nenhuma agenda encontrada")
        else:
            col1, col2 = st.columns(2)
            
            with col1:
                consultor_count = df_filtered['consultor'].value_counts().head(10)
                fig1 = px.bar(
                    x=consultor_count.values,
                    y=consultor_count.index,
                    orientation='h',
                    title="Top 10 Consultores",
                    labels={'x': 'Agendas', 'y': 'Consultor'},
                    color_discrete_sequence=['#002B49']
                )
                fig1.update_layout(
                    showlegend=False,
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                projeto_count = df_filtered['projeto'].value_counts()
                fig2 = px.pie(
                    values=projeto_count.values,
                    names=projeto_count.index,
                    title="Distribuição por Projeto",
                    color_discrete_sequence=['#002B49', '#004870', '#0066A1', '#4A90E2', '#7AABDB']
                )
                fig2.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            # Gráfico de timeline
            st.markdown("#### 📅 Timeline")
            
            # Preparar dados para timeline
            df_timeline = df_filtered.copy()
            df_timeline = df_timeline.sort_values('data_inicio')
            
            fig3 = px.timeline(
                df_timeline,
                x_start='data_inicio',
                x_end='data_fim',
                y='consultor',
                color='projeto',
                hover_data=['os'],
                title="Timeline de Agendas",
                color_discrete_sequence=['#002B49', '#004870', '#0066A1', '#4A90E2', '#7AABDB']
            )
            
            fig3.update_layout(
                height=max(400, len(df_timeline['consultor'].unique()) * 40),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="",
                yaxis_title=""
            )
            
            st.plotly_chart(fig3, use_container_width=True)
            
            # Estatísticas adicionais
            col1, col2, col3 = st.columns(3)
            
            with col1:
                dias_total = (df_filtered['data_fim'] - df_filtered['data_inicio']).dt.days.sum() + len(df_filtered)
                st.metric("Total de Dias", f"{dias_total}")
            
            with col2:
                media_dias = ((df_filtered['data_fim'] - df_filtered['data_inicio']).dt.days + 1).mean()
                st.metric("Média de Dias/Agenda", f"{media_dias:.1f}")
            
            with col3:
                os_unicas = df_filtered['os'].nunique()
                st.metric("OS Únicas", f"{os_unicas}")

def timeline_mv_page(db):
    """Página de visualização Timeline MV"""
    st.markdown("## 📅 Visualização Timeline MV")
    st.markdown("Visualização em calendário estilo MV Sistemas")
    
    render_timeline_view(db)

def consultor_agenda_page(db, usuario):
    """Página de agenda do consultor"""
    consultor_nome = usuario.get('consultor_vinculado') or usuario['nome']
    
    st.markdown(f"## 📋 Minha Agenda - {consultor_nome}")
    
    # Buscar agendas do consultor
    agendas = db.get_agendas_by_consultor(consultor_nome)
    
    if not agendas:
        st.info("📭 Você ainda não possui agendas cadastradas.")
        return
    
    # Exibir timeline compacta
    render_compact_timeline(db, dias=60)
    
    st.markdown("---")
    st.markdown("### 📊 Minhas Agendas")
    
    for agenda in sorted(agendas, key=lambda x: x['data_inicio'], reverse=True)[:20]:
        inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").strftime("%d/%m/%Y")
        fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").strftime("%d/%m/%Y")
        is_vago = agenda.get('is_vago', False)
        
        with st.expander(f"📅 {inicio} - {fim} | {agenda['projeto']}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Projeto:** {agenda['projeto']}")
                if agenda.get('os'):
                    st.write(f"**OS:** {agenda['os']}")
                if agenda.get('gerente'):
                    st.write(f"**Gerente:** {agenda['gerente']}")
            
            with col2:
                st.write(f"**Status:** {'🟢 Disponível' if is_vago else '🔴 Ocupado'}")
                st.write(f"**Data Início:** {inicio}")
                st.write(f"**Data Fim:** {fim}")
            
            # Formulário para editar detalhes
            if not is_vago:
                st.markdown("---")
                st.markdown("### 📝 Detalhes da Agenda")
                
                with st.form(key=f"detalhes_{agenda['id']}"):
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        horas = st.number_input(
                            "⏱️ Horas no Cliente",
                            min_value=0.0,
                            max_value=999.99,
                            value=float(agenda.get('horas_cliente', 0.0)) if agenda.get('horas_cliente') else 0.0,
                            step=0.5,
                            help="Quantidade de horas trabalhadas"
                        )
                    
                    with col_b:
                        st.markdown("##")  # Espaçamento
                    
                    descricao = st.text_area(
                        "📋 Descrição da Entrega",
                        value=agenda.get('descricao_entrega', '') or '',
                        height=100,
                        help="Descreva as entregas realizadas nesta agenda"
                    )
                    
                    salvar = st.form_submit_button("💾 Salvar Detalhes", use_container_width=True)
                    
                    if salvar:
                        if db.atualizar_detalhes_agenda(agenda['id'], horas, descricao):
                            st.success("✅ Detalhes salvos com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao salvar detalhes")
                
                # Exibir detalhes atuais se existirem
                if agenda.get('horas_cliente') or agenda.get('descricao_entrega'):
                    st.markdown("---")
                    st.markdown("**📊 Informações Atuais:**")
                    if agenda.get('horas_cliente'):
                        st.info(f"⏱️ Horas: {agenda['horas_cliente']}h")
                    if agenda.get('descricao_entrega'):
                        st.info(f"📋 Entrega: {agenda['descricao_entrega']}")

def usuarios_page(db):
    """Página de gerenciamento de usuários (apenas ADM)"""
    auth = AuthManager(db)
    
    st.markdown("## 👥 Gerenciamento de Usuários")
    
    # Criar novo usuário
    with st.expander("➕ Criar Novo Usuário", expanded=False):
        with st.form("criar_usuario"):
            col1, col2 = st.columns(2)
            
            with col1:
                email = st.text_input("Email")
                nome = st.text_input("Nome Completo")
                senha = st.text_input("Senha", type="password")
            
            with col2:
                tipo = st.selectbox("Tipo de Usuário", ["ADM", "CL_MV", "CONSULTOR"])
                
                consultor_vinc = None
                if tipo == "CONSULTOR":
                    # Buscar consultores existentes
                    agendas = db.get_all_agendas()
                    consultores = sorted(list(set([a['consultor'] for a in agendas])))
                    consultor_vinc = st.selectbox("Consultor Vinculado", consultores)
            
            submit = st.form_submit_button("Criar Usuário", use_container_width=True)
            
            if submit:
                if not email or not nome or not senha:
                    st.error("⚠️ Preencha todos os campos")
                elif tipo == "CONSULTOR" and not consultor_vinc:
                    st.error("⚠️ Selecione o consultor vinculado")
                else:
                    if auth.criar_usuario(email, senha, nome, tipo, consultor_vinc):
                        st.success(f"✅ Usuário {nome} criado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao criar usuário")
    
    # Listar usuários existentes
    st.markdown("### 📋 Usuários Cadastrados")
    
    usuarios = auth.listar_usuarios()
    
    if usuarios:
        for user in usuarios:
            with st.expander(f"{'✅' if user['ativo'] else '❌'} {user['nome']} - {user['email']}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.write(f"**Tipo:** {user['tipo_usuario']}")
                    if user.get('consultor_vinculado'):
                        st.write(f"**Vinculado a:** {user['consultor_vinculado']}")
                
                with col2:
                    st.write(f"**Status:** {'🟢 Ativo' if user['ativo'] else '🔴 Inativo'}")
                
                with col3:
                    if user['ativo']:
                        if st.button("Desativar", key=f"desativar_{user['id']}"):
                            if auth.desativar_usuario(user['id']):
                                st.success("Usuário desativado!")
                                st.rerun()
    else:
        st.info("Nenhum usuário cadastrado")

def config_page(db):
    """Página de configurações do sistema"""
    st.markdown("## ⚙️ Configurações do Sistema")
    
    tab1, tab2, tab3 = st.tabs(["📊 Estatísticas", "🗑️ Limpeza", "📥 Importação/Exportação"])
    
    with tab1:
        st.markdown("### 📊 Estatísticas do Sistema")
        
        agendas = db.get_all_agendas()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="stat-card"><h3>Total Agendas</h3><p>{len(agendas)}</p><div class="stat-subtitle">Cadastradas no sistema</div></div>', unsafe_allow_html=True)
        
        with col2:
            consultores = len(set([a['consultor'] for a in agendas]))
            st.markdown(f'<div class="stat-card"><h3>Consultores</h3><p>{consultores}</p><div class="stat-subtitle">Diferentes consultores</div></div>', unsafe_allow_html=True)
        
        with col3:
            projetos = len(set([a['projeto'] for a in agendas]))
            st.markdown(f'<div class="stat-card"><h3>Projetos</h3><p>{projetos}</p><div class="stat-subtitle">Projetos únicos</div></div>', unsafe_allow_html=True)
        
        with col4:
            os_total = len(set([a['os'] for a in agendas if a.get('os')]))
            st.markdown(f'<div class="stat-card"><h3>OS</h3><p>{os_total}</p><div class="stat-subtitle">Ordens de serviço</div></div>', unsafe_allow_html=True)
        
        st.markdown("##")
        
        # Gráfico de agendas por consultor
        if agendas:
            df_consultores = pd.DataFrame([{'Consultor': k, 'Agendas': len(list(v))} 
                                          for k, v in pd.DataFrame(agendas).groupby('consultor')])
            
            fig = px.bar(df_consultores.sort_values('Agendas', ascending=False), 
                        x='Consultor', y='Agendas',
                        title='Distribuição de Agendas por Consultor',
                        color='Agendas',
                        color_continuous_scale='Blues')
            
            fig.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("##")
        
        # Top 10 projetos mais frequentes
        if agendas:
            st.markdown("#### 📁 Top 10 Projetos Mais Frequentes")
            df_projetos = pd.DataFrame(agendas)
            top_projetos = df_projetos['projeto'].value_counts().head(10)
            
            for idx, (projeto, count) in enumerate(top_projetos.items(), 1):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{idx}. {projeto}**")
                with col2:
                    st.write(f"🔢 {count} agendas")
    
    with tab2:
        st.markdown("### 🗑️ Limpeza e Manutenção")
        st.warning("⚠️ **Atenção:** Operações de limpeza são irreversíveis!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Limpar Agendas Antigas")
            st.info("Remove agendas concluídas há mais de X dias")
            
            dias_antigas = st.number_input("Dias atrás", min_value=30, max_value=365, value=90, step=30)
            
            if st.button("🗑️ Limpar Agendas Antigas", type="secondary"):
                data_limite = (datetime.now() - timedelta(days=dias_antigas)).date()
                agendas_antigas = [a for a in agendas if datetime.strptime(a['data_fim'], '%Y-%m-%d').date() < data_limite]
                
                if agendas_antigas:
                    st.warning(f"📋 {len(agendas_antigas)} agendas serão removidas")
                    
                    if st.button("✅ Confirmar Remoção"):
                        removidas = 0
                        for agenda in agendas_antigas:
                            if db.delete_agenda(agenda['id']):
                                removidas += 1
                        
                        st.success(f"✅ {removidas} agendas removidas com sucesso!")
                        st.rerun()
                else:
                    st.info(f"✅ Não há agendas antigas (>{dias_antigas} dias)")
        
        with col2:
            st.markdown("#### Limpar Agendas Vazias")
            st.info("Remove agendas marcadas como 'Vago'")
            
            if st.button("🗑️ Limpar Agendas Vazias", type="secondary"):
                agendas_vazias = [a for a in agendas if a.get('is_vago', False)]
                
                if agendas_vazias:
                    st.warning(f"📋 {len(agendas_vazias)} agendas vazias encontradas")
                    
                    if st.button("✅ Confirmar Limpeza"):
                        removidas = 0
                        for agenda in agendas_vazias:
                            if db.delete_agenda(agenda['id']):
                                removidas += 1
                        
                        st.success(f"✅ {removidas} agendas vazias removidas!")
                        st.rerun()
                else:
                    st.info("✅ Não há agendas vazias no sistema")
    
    with tab3:
        st.markdown("### 📥 Importação e Exportação")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📤 Exportar Dados")
            st.info("Baixe todos os dados em formato CSV")
            
            formato = st.selectbox("Formato", ["CSV", "Excel (XLSX)", "JSON"])
            
            if st.button("📥 Exportar Agendas", use_container_width=True):
                if agendas:
                    df = pd.DataFrame(agendas)
                    
                    # Formatar datas
                    df['data_inicio'] = pd.to_datetime(df['data_inicio']).dt.strftime('%d/%m/%Y')
                    df['data_fim'] = pd.to_datetime(df['data_fim']).dt.strftime('%d/%m/%Y')
                    
                    # Selecionar colunas
                    colunas = ['id', 'consultor', 'projeto', 'os', 'gerente', 'data_inicio', 'data_fim', 
                              'horas_cliente', 'descricao_entrega', 'is_vago']
                    df_export = df[[c for c in colunas if c in df.columns]]
                    
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    
                    if formato == "CSV":
                        csv = df_export.to_csv(index=False).encode('utf-8-sig')
                        st.download_button(
                            label="📥 Download CSV",
                            data=csv,
                            file_name=f"agendas_ativa_{timestamp}.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
                    elif formato == "Excel (XLSX)":
                        # Criar arquivo Excel em memória
                        from io import BytesIO
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            df_export.to_excel(writer, index=False, sheet_name='Agendas')
                        
                        st.download_button(
                            label="📥 Download Excel",
                            data=output.getvalue(),
                            file_name=f"agendas_ativa_{timestamp}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True
                        )
                    else:  # JSON
                        import json
                        json_data = df_export.to_json(orient='records', force_ascii=False, indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_data,
                            file_name=f"agendas_ativa_{timestamp}.json",
                            mime="application/json",
                            use_container_width=True
                        )
                else:
                    st.warning("Não há dados para exportar")
        
        with col2:
            st.markdown("#### 📤 Importar Dados")
            st.info("Importar agendas de arquivo CSV")
            
            uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])
            
            if uploaded_file is not None:
                try:
                    df_import = pd.read_csv(uploaded_file)
                    
                    st.write(f"**{len(df_import)}** agendas encontradas no arquivo")
                    st.dataframe(df_import.head(5), use_container_width=True)
                    
                    if st.button("✅ Importar Agendas", use_container_width=True):
                        importadas = 0
                        erros = 0
                        
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, row in df_import.iterrows():
                            try:
                                # Converter datas se necessário
                                data_inicio = pd.to_datetime(row['data_inicio']).strftime('%Y-%m-%d')
                                data_fim = pd.to_datetime(row['data_fim']).strftime('%Y-%m-%d')
                                
                                if db.create_agenda(
                                    consultor=row['consultor'],
                                    data_inicio=data_inicio,
                                    data_fim=data_fim,
                                    projeto=row['projeto'],
                                    os=row.get('os'),
                                    gerente=row.get('gerente')
                                ):
                                    importadas += 1
                                else:
                                    erros += 1
                            except Exception as e:
                                erros += 1
                                st.error(f"Erro na linha {idx + 1}: {str(e)}")
                            
                            progress_bar.progress((idx + 1) / len(df_import))
                            status_text.text(f"Processando: {idx + 1}/{len(df_import)}")
                        
                        st.success(f"✅ Importação concluída: {importadas} sucesso, {erros} erros")
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {str(e)}")

if __name__ == "__main__":
    main()
