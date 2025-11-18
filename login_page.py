"""
Página de Login
"""
import streamlit as st
from auth import AuthManager
from database import Database

def show_login_page(db: Database):
    """Exibe página de login"""
    auth = AuthManager(db)
    
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 2rem;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("# 🔐 Login")
        st.markdown("### Sistema de Agendas Ativa")
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="seu@email.com")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Sua senha")
            
            submit = st.form_submit_button("Entrar", use_container_width=True)
            
            if submit:
                if not email or not senha:
                    st.error("⚠️ Preencha email e senha")
                else:
                    usuario = auth.login(email, senha)
                    
                    if usuario:
                        # Salvar dados do usuário na sessão
                        st.session_state.usuario = usuario
                        st.session_state.authenticated = True
                        st.success(f"✅ Bem-vindo(a), {usuario['nome']}!")
                        st.rerun()
                    else:
                        st.error("❌ Email ou senha incorretos")
        
        st.markdown("---")
        st.caption("Usuário padrão: admin@ativa.com | Senha: admin123")

def show_user_menu():
    """Exibe menu do usuário logado"""
    if 'usuario' not in st.session_state:
        return
    
    usuario = st.session_state.usuario
    
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"### 👤 {usuario['nome']}")
        st.caption(f"📧 {usuario['email']}")
        
        # Badge do tipo de usuário
        tipo_badges = {
            "ADM": "🔑 Administrador",
            "CL_MV": "👁️ Visualização MV",
            "CONSULTOR": "👤 Consultor"
        }
        st.info(tipo_badges.get(usuario['tipo_usuario'], usuario['tipo_usuario']))
        
        if usuario.get('consultor_vinculado'):
            st.caption(f"Vinculado a: {usuario['consultor_vinculado']}")
        
        st.markdown("---")
        
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.clear()
            st.rerun()

def require_auth():
    """Decorator para páginas que requerem autenticação"""
    if 'authenticated' not in st.session_state or not st.session_state.authenticated:
        return False
    return True

def require_permission(action: str) -> bool:
    """Verifica se usuário tem permissão para ação"""
    if not require_auth():
        return False
    
    usuario = st.session_state.usuario
    return AuthManager.check_permission(usuario['tipo_usuario'], action)
