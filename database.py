import os
from supabase import create_client, Client
from datetime import datetime
from typing import List, Dict, Optional
import streamlit as st

class Database:
    """Classe para gerenciar operações com Supabase"""
    
    def __init__(self):
        """Inicializa conexão com Supabase"""
        # Obter credenciais das variáveis de ambiente ou secrets do Streamlit
        self.supabase_url = None
        self.supabase_key = None
        self.client = None
        
        try:
            # Tentar secrets do Streamlit primeiro
            if hasattr(st, 'secrets') and 'SUPABASE_URL' in st.secrets:
                self.supabase_url = st.secrets["SUPABASE_URL"]
                self.supabase_key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_ANON_KEY")
        except:
            pass
        
        # Fallback para variáveis de ambiente
        if not self.supabase_url:
            self.supabase_url = os.getenv("SUPABASE_URL")
            self.supabase_key = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            print("⚠️ Credenciais do Supabase não configuradas.")
            return
        
        try:
            self.client = create_client(self.supabase_url, self.supabase_key)
        except Exception as e:
            print(f"Erro ao conectar: {str(e)}")
            self.client = None
        
        self.table_name = "agendas"
    
    def _ensure_connection(self) -> bool:
        """Verifica se há conexão com o banco"""
        if self.client is None:
            st.error("❌ Sem conexão com o banco de dados")
            return False
        return True
    
    def create_agenda(self, consultor: str, data_inicio: str, data_fim: str, 
                     projeto: str, os: Optional[str] = None, gerente: Optional[str] = None) -> bool:
        """
        Cria uma nova agenda
        
        Args:
            consultor: Nome do consultor
            data_inicio: Data de início (YYYY-MM-DD)
            data_fim: Data de fim (YYYY-MM-DD)
            projeto: Nome do projeto
            os: Número da OS (opcional)
            gerente: Nome do gerente (opcional)
        
        Returns:
            bool: True se sucesso, False caso contrário
        """
        if not self._ensure_connection():
            return False
        
        try:
            # Verificar se é uma agenda vaga
            is_vago = projeto.upper() == "VAGO" or projeto.upper() == "LIVRE"
            
            # Se não é VAGO, verificar conflito de agendas
            if not is_vago:
                conflito = self._check_conflito(consultor, data_inicio, data_fim)
                if conflito:
                    st.warning(f"⚠️ Atenção: O consultor {consultor} já possui agendas no período:\n\n{conflito}")
            
            data = {
                "consultor": consultor,
                "data_inicio": data_inicio,
                "data_fim": data_fim,
                "projeto": projeto,
                "is_vago": is_vago,
                "created_at": datetime.now().isoformat()
            }
            
            # Adicionar campos opcionais apenas se fornecidos
            if os:
                data["os"] = os
            if gerente:
                data["gerente"] = gerente
            
            response = self.client.table(self.table_name).insert(data).execute()
            
            if response.data:
                return True
            return False
            
        except Exception as e:
            st.error(f"❌ Erro ao criar agenda: {str(e)}")
            return False
    
    def _check_conflito(self, consultor: str, data_inicio: str, data_fim: str) -> Optional[str]:
        """
        Verifica se há conflito de agendas para o consultor
        
        Returns:
            String com detalhes do conflito ou None
        """
        try:
            # Buscar agendas que se sobrepõem
            response = self.client.table(self.table_name)\
                .select("*")\
                .eq("consultor", consultor)\
                .execute()
            
            if not response.data:
                return None
            
            conflitos = []
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d").date()
            
            for agenda in response.data:
                agenda_inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").date()
                agenda_fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").date()
                
                # Verificar sobreposição
                # Ignorar agendas VAGO ao verificar conflitos
                if agenda.get('is_vago', False):
                    continue
                    
                if not (data_fim_dt < agenda_inicio or data_inicio_dt > agenda_fim):
                    os_info = f" (OS {agenda['os']})" if agenda.get('os') else ""
                    conflitos.append(
                        f"• {agenda['projeto']}{os_info}: "
                        f"{agenda_inicio.strftime('%d/%m/%Y')} a {agenda_fim.strftime('%d/%m/%Y')}"
                    )
            
            if conflitos:
                return "\n".join(conflitos)
            
            return None
            
        except Exception as e:
            return None
    
    def get_all_agendas(self) -> List[Dict]:
        """
        Retorna todas as agendas
        
        Returns:
            Lista de dicionários com as agendas
        """
        if not self._ensure_connection():
            return []
        
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .order("data_inicio", desc=True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            st.error(f"❌ Erro ao buscar agendas: {str(e)}")
            return []
    
    def get_agendas_by_consultor(self, consultor: str) -> List[Dict]:
        """
        Retorna agendas de um consultor específico
        
        Args:
            consultor: Nome do consultor
        
        Returns:
            Lista de dicionários com as agendas
        """
        if not self._ensure_connection():
            return []
        
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .ilike("consultor", f"%{consultor}%")\
                .order("data_inicio", desc=True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            st.error(f"❌ Erro ao buscar agendas: {str(e)}")
            return []
    
    def get_agendas_by_projeto(self, projeto: str) -> List[Dict]:
        """
        Retorna agendas de um projeto específico
        
        Args:
            projeto: Nome do projeto
        
        Returns:
            Lista de dicionários com as agendas
        """
        if not self._ensure_connection():
            return []
        
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .ilike("projeto", f"%{projeto}%")\
                .order("data_inicio", desc=True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            st.error(f"❌ Erro ao buscar agendas: {str(e)}")
            return []
    
    def get_agendas_by_date_range(self, data_inicio: str, data_fim: str) -> List[Dict]:
        """
        Retorna agendas em um período específico
        
        Args:
            data_inicio: Data de início (YYYY-MM-DD)
            data_fim: Data de fim (YYYY-MM-DD)
        
        Returns:
            Lista de dicionários com as agendas
        """
        if not self._ensure_connection():
            return []
        
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .gte("data_fim", data_inicio)\
                .lte("data_inicio", data_fim)\
                .order("data_inicio", desc=True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            st.error(f"❌ Erro ao buscar agendas: {str(e)}")
            return []
    
    def check_disponibilidade(self, consultor: str, data_inicio: str, data_fim: str) -> Dict:
        """
        Verifica disponibilidade de um consultor em um período
        
        Args:
            consultor: Nome do consultor
            data_inicio: Data de início (YYYY-MM-DD)
            data_fim: Data de fim (YYYY-MM-DD)
        
        Returns:
            Dict com status e agendas conflitantes
        """
        if not self._ensure_connection():
            return {"disponivel": False, "agendas": [], "mensagem": "Erro de conexão"}
        
        try:
            response = self.client.table(self.table_name)\
                .select("*")\
                .ilike("consultor", f"%{consultor}%")\
                .execute()
            
            if not response.data:
                return {
                    "disponivel": True,
                    "agendas": [],
                    "mensagem": f"✅ {consultor} está livre no período solicitado."
                }
            
            conflitos = []
            data_inicio_dt = datetime.strptime(data_inicio, "%Y-%m-%d").date()
            data_fim_dt = datetime.strptime(data_fim, "%Y-%m-%d").date()
            
            for agenda in response.data:
                agenda_inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").date()
                agenda_fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").date()
                
                # Verificar sobreposição
                if not (data_fim_dt < agenda_inicio or data_inicio_dt > agenda_fim):
                    conflitos.append(agenda)
            
            if conflitos:
                mensagem = f"❌ {consultor} está ocupado(a) no período. Agendas conflitantes:\n\n"
                for c in conflitos:
                    inicio = datetime.strptime(c['data_inicio'], "%Y-%m-%d").strftime("%d/%m/%Y")
                    fim = datetime.strptime(c['data_fim'], "%Y-%m-%d").strftime("%d/%m/%Y")
                    mensagem += f"• {c['projeto']} (OS {c['os']}): {inicio} a {fim}\n"
                
                return {
                    "disponivel": False,
                    "agendas": conflitos,
                    "mensagem": mensagem
                }
            
            return {
                "disponivel": True,
                "agendas": [],
                "mensagem": f"✅ {consultor} está livre no período solicitado."
            }
            
        except Exception as e:
            return {
                "disponivel": False,
                "agendas": [],
                "mensagem": f"❌ Erro ao verificar disponibilidade: {str(e)}"
            }
    
    def update_agenda(self, agenda_id: int, **kwargs) -> bool:
        """
        Atualiza uma agenda existente
        
        Args:
            agenda_id: ID da agenda
            **kwargs: Campos a atualizar
        
        Returns:
            bool: True se sucesso, False caso contrário
        """
        if not self._ensure_connection():
            return False
        
        try:
            response = self.client.table(self.table_name)\
                .update(kwargs)\
                .eq("id", agenda_id)\
                .execute()
            
            return bool(response.data)
            
        except Exception as e:
            st.error(f"❌ Erro ao atualizar agenda: {str(e)}")
            return False
    
    def delete_agenda(self, agenda_id: int) -> bool:
        """
        Deleta uma agenda
        
        Args:
            agenda_id: ID da agenda
        
        Returns:
            bool: True se sucesso, False caso contrário
        """
        if not self._ensure_connection():
            return False
        
        try:
            response = self.client.table(self.table_name)\
                .delete()\
                .eq("id", agenda_id)\
                .execute()
            
            return True
            
        except Exception as e:
            st.error(f"❌ Erro ao deletar agenda: {str(e)}")
            return False
    
    def get_consultores_livres(self, data_inicio: str, data_fim: str, 
                               todos_consultores: List[str]) -> List[str]:
        """
        Retorna lista de consultores livres em um período
        
        Args:
            data_inicio: Data de início (YYYY-MM-DD)
            data_fim: Data de fim (YYYY-MM-DD)
            todos_consultores: Lista com todos os consultores
        
        Returns:
            Lista de consultores livres
        """
        if not self._ensure_connection():
            return []
        
        try:
            agendas = self.get_agendas_by_date_range(data_inicio, data_fim)
            consultores_ocupados = set([a['consultor'] for a in agendas])
            consultores_livres = [c for c in todos_consultores if c not in consultores_ocupados]
            
            return consultores_livres
            
        except Exception as e:
            return []
    
    def atualizar_detalhes_agenda(self, agenda_id: int, horas_cliente: Optional[float] = None, 
                                  descricao_entrega: Optional[str] = None) -> bool:
        """
        Atualiza os detalhes de horas e descrição de uma agenda
        
        Args:
            agenda_id: ID da agenda
            horas_cliente: Horas trabalhadas no cliente
            descricao_entrega: Descrição da entrega realizada
        
        Returns:
            bool: True se sucesso, False caso contrário
        """
        if not self._ensure_connection():
            return False
        
        try:
            data = {}
            
            if horas_cliente is not None:
                data["horas_cliente"] = horas_cliente
            
            if descricao_entrega is not None:
                data["descricao_entrega"] = descricao_entrega
            
            if not data:
                return True  # Nada para atualizar
            
            response = self.client.table(self.table_name)\
                .update(data)\
                .eq("id", agenda_id)\
                .execute()
            
            return bool(response.data)
            
        except Exception as e:
            st.error(f"❌ Erro ao atualizar detalhes: {str(e)}")
            return False
