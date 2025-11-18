"""
Módulo de autenticação e gerenciamento de usuários
"""
import bcrypt
import streamlit as st
from database import Database
from typing import Optional, Dict

class AuthManager:
    """Gerencia autenticação e permissões de usuários"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def hash_password(self, password: str) -> str:
        """Gera hash da senha"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def login(self, email: str, password: str) -> Optional[Dict]:
        """
        Autentica usuário
        Returns: Dicionário com dados do usuário ou None
        """
        if not self.db._ensure_connection():
            return None
        
        try:
            response = self.db.client.table("usuarios")\
                .select("*")\
                .eq("email", email)\
                .eq("ativo", True)\
                .execute()
            
            if not response.data or len(response.data) == 0:
                return None
            
            usuario = response.data[0]
            
            if self.verify_password(password, usuario['senha_hash']):
                # Registrar log de acesso
                self._log_acesso(usuario['id'], "LOGIN", {"email": email})
                return usuario
            
            return None
        except Exception as e:
            st.error(f"Erro ao fazer login: {str(e)}")
            return None
    
    def criar_usuario(self, email: str, senha: str, nome: str, 
                     tipo_usuario: str, consultor_vinculado: Optional[str] = None) -> bool:
        """
        Cria novo usuário
        
        Args:
            email: Email do usuário
            senha: Senha em texto plano
            nome: Nome completo
            tipo_usuario: CONSULTOR, CL_MV ou ADM
            consultor_vinculado: Nome do consultor (apenas para tipo CONSULTOR)
        """
        if not self.db._ensure_connection():
            return False
        
        try:
            senha_hash = self.hash_password(senha)
            
            data = {
                "email": email,
                "senha_hash": senha_hash,
                "nome": nome,
                "tipo_usuario": tipo_usuario,
                "ativo": True
            }
            
            if consultor_vinculado:
                data["consultor_vinculado"] = consultor_vinculado
            
            response = self.db.client.table("usuarios").insert(data).execute()
            
            return bool(response.data)
        except Exception as e:
            st.error(f"Erro ao criar usuário: {str(e)}")
            return False
    
    def listar_usuarios(self):
        """Lista todos os usuários"""
        if not self.db._ensure_connection():
            return []
        
        try:
            response = self.db.client.table("usuarios")\
                .select("id, email, nome, tipo_usuario, consultor_vinculado, ativo")\
                .order("created_at", desc=True)\
                .execute()
            
            return response.data if response.data else []
        except Exception as e:
            st.error(f"Erro ao listar usuários: {str(e)}")
            return []
    
    def alterar_senha(self, usuario_id: int, senha_nova: str) -> bool:
        """Altera senha do usuário"""
        if not self.db._ensure_connection():
            return False
        
        try:
            senha_hash = self.hash_password(senha_nova)
            
            response = self.db.client.table("usuarios")\
                .update({"senha_hash": senha_hash})\
                .eq("id", usuario_id)\
                .execute()
            
            return bool(response.data)
        except Exception as e:
            st.error(f"Erro ao alterar senha: {str(e)}")
            return False
    
    def desativar_usuario(self, usuario_id: int) -> bool:
        """Desativa usuário"""
        if not self.db._ensure_connection():
            return False
        
        try:
            response = self.db.client.table("usuarios")\
                .update({"ativo": False})\
                .eq("id", usuario_id)\
                .execute()
            
            return bool(response.data)
        except Exception as e:
            st.error(f"Erro ao desativar usuário: {str(e)}")
            return False
    
    def _log_acesso(self, usuario_id: int, acao: str, detalhes: Dict = None):
        """Registra log de acesso"""
        try:
            data = {
                "usuario_id": usuario_id,
                "acao": acao,
                "detalhes": detalhes or {}
            }
            self.db.client.table("logs_acesso").insert(data).execute()
        except:
            pass  # Não quebrar se log falhar
    
    @staticmethod
    def check_permission(tipo_usuario: str, action: str) -> bool:
        """
        Verifica se o tipo de usuário tem permissão para a ação
        
        Permissões:
        - CONSULTOR: ver apenas própria agenda, editar própria agenda
        - CL_MV: ver todas agendas (visualização MV), não pode editar
        - ADM: todas permissões
        """
        permissions = {
            "CONSULTOR": ["ver_propria_agenda", "editar_propria_agenda"],
            "CL_MV": ["ver_todas_agendas", "visualizacao_mv"],
            "ADM": ["ver_todas_agendas", "editar_todas_agendas", "gerenciar_usuarios", "visualizacao_mv"]
        }
        
        return action in permissions.get(tipo_usuario, [])
