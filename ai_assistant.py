import os
import cohere
import streamlit as st
from datetime import datetime, timedelta
import re
import unicodedata
from typing import List, Dict, Union

class AIAssistant:
    """Assistente de IA usando Cohere para processamento de linguagem natural"""
    
    def __init__(self):
        """Inicializa o cliente Cohere"""
        self.client = None
        
        # Tentar obter API key de secrets ou variável de ambiente
        self.api_key = None
        try:
            if hasattr(st, 'secrets') and 'COHERE_API_KEY' in st.secrets:
                self.api_key = st.secrets["COHERE_API_KEY"]
        except:
            pass
        
        if not self.api_key:
            self.api_key = os.getenv("COHERE_API_KEY", "kk6JjxQxYXNngcxx1RJiZtD6ZGL1MzeJAzysE9ym")
        
        try:
            self.client = cohere.Client(self.api_key)
        except Exception as e:
            print(f"❌ Erro ao inicializar Cohere: {str(e)}")
            self.client = None
    
    def normalize_text(self, text: str) -> str:
        """Normaliza texto removendo acentos e convertendo para minúsculo"""
        if not text: return ""
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

    def process_query(self, query: str, agendas: List[Dict]) -> Dict:
        """
        Processa uma query do usuário e retorna resposta estruturada
        
        Args:
            query: Pergunta ou comando do usuário
            agendas: Lista de agendas para contexto
        
        Returns:
            Dict com 'text' e opcionalmente 'action'
        """
        if not self.client:
            return {"text": "❌ Assistente de IA não disponível. Configure a COHERE_API_KEY.", "action": None}
        
        try:
            # Identificar a intenção do usuário
            intent = self._identify_intent(query)
            print(f"[DEBUG] Intent final: {intent}")
            
            response = None
            
            # Processar baseado na intenção
            if intent == "disponibilidade":
                response = self._handle_disponibilidade(query, agendas)
            elif intent == "consulta":
                response = self._handle_consulta(query, agendas)
            elif intent == "listar":
                response = self._handle_listar(query, agendas)
            elif intent == "criar":
                response = self._handle_criar_agenda(query)
            elif intent == "verificar_vaga":
                response = self._handle_verificar_vaga(query, agendas)
            else:
                # Fallback para Cohere se não identificar a intenção
                response = self._interpret_query_with_cohere(query, agendas)
            
            # Normalizar resposta para formato Dict
            if isinstance(response, str):
                return {"text": response, "action": None}
            return response
                
        except Exception as e:
            return {"text": f"❌ Erro ao processar pergunta: {str(e)}\n\nTente reformular sua pergunta.", "action": None}

    def _handle_verificar_vaga(self, query: str, agendas: List[Dict]) -> str:
        """
        Verifica se há vaga para uma demanda específica.
        Ex: "Preciso de um consultor para o projeto X de 10/01 a 20/01"
        """
        # Extrair datas da demanda
        datas = self._extract_dates(query)
        if not datas:
            return "❓ Para verificar vagas, preciso saber o período desejado.\n\n**Exemplo:** _'Preciso de consultor de 10/01 a 20/01'_"
        
        data_inicio, data_fim = datas
        
        # Buscar consultores disponíveis no período
        consultores_disponiveis = []
        
        # Obter lista única de todos os consultores cadastrados
        todos_consultores = sorted(list(set([a['consultor'] for a in agendas])))
        
        for consultor in todos_consultores:
            # Verificar se o consultor tem conflito no período
            tem_conflito = False
            agendas_consultor = [a for a in agendas if a['consultor'] == consultor]
            
            for agenda in agendas_consultor:
                # Ignorar agendas vagas
                is_vago = agenda.get('is_vago', False) or agenda.get('projeto', '').upper() in ['VAGO', 'LIVRE']
                if is_vago:
                    continue
                
                ag_inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").date()
                ag_fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").date()
                
                # Se houver sobreposição, tem conflito
                if not (data_fim < ag_inicio or data_inicio > ag_fim):
                    tem_conflito = True
                    break
            
            if not tem_conflito:
                consultores_disponiveis.append(consultor)
        
        # Formatar resposta
        if data_inicio == data_fim:
            periodo_str = data_inicio.strftime('%d/%m/%Y')
        else:
            periodo_str = f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
        
        if not consultores_disponiveis:
            return f"❌ **Não há consultores disponíveis** para o período de {periodo_str}."
        
        resposta = f"✅ **Encontrei {len(consultores_disponiveis)} consultores disponíveis** para {periodo_str}:\n\n"
        
        for cons in consultores_disponiveis:
            resposta += f"• 👤 **{cons}**\n"
            
        resposta += "\n💡 _Dica: Use o comando 'Agende [Nome] para [Projeto]...' para realizar a alocação._"
        
        return resposta
    
    def _prepare_context(self, agendas: List[Dict]) -> str:
        """Prepara contexto das agendas para a IA"""
        if not agendas:
            return "Não há agendas cadastradas no momento."
        
        context = "Agendas cadastradas:\n\n"
        context += "IMPORTANTE: Agendas com projeto 'VAGO' ou 'LIVRE' significam que o consultor está DISPONÍVEL nesse período.\n\n"
        
        for agenda in agendas[:50]:  # Limitar para não exceder tokens
            inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").strftime("%d/%m/%Y")
            fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").strftime("%d/%m/%Y")
            is_vago = agenda.get('is_vago', False) or agenda.get('projeto', '').upper() in ['VAGO', 'LIVRE']
            
            if is_vago:
                context += f"- Consultor: {agenda['consultor']}, DISPONÍVEL (agenda vaga), Período: {inicio} a {fim}\n"
            else:
                os_info = f", OS: {agenda['os']}" if agenda.get('os') else ""
                gerente_info = f", Gerente: {agenda['gerente']}" if agenda.get('gerente') else ""
                context += f"- Consultor: {agenda['consultor']}, Projeto: {agenda['projeto']}{os_info}{gerente_info}, Período: {inicio} a {fim}\n"
        
        return context
    
    def _identify_intent(self, query: str) -> str:
        """Identifica a intenção do usuário com maior precisão"""
        query_lower = query.lower()
        
        # Palavras-chave para criar agenda
        criar_keywords = ['agende', 'criar', 'adicionar', 'adicione', 'registrar', 'registre', 'alocar', 'aloque', 'reserve']
        if any(keyword in query_lower for keyword in criar_keywords):
            return "criar"
            
        # Palavras-chave para verificar vaga (demanda do CEO)
        vaga_keywords = ['vaga', 'preciso de', 'tem alguem', 'tem alguém', 'quem pode', 'quem está livre', 'quem esta livre', 'sugira', 'sugestão']
        if any(keyword in query_lower for keyword in vaga_keywords):
            return "verificar_vaga"
        
        # PRIORIDADE 1: Verificar disponibilidade (livre/ocupado/pode) - ANTES de qualquer outra coisa
        disp_keywords = ['livre', 'ocupado', 'disponível', 'disponivel', 'pode', 'está livre', 'esta livre', 'tem vaga', 'tem agenda livre']
        if any(keyword in query_lower for keyword in disp_keywords):
            consultor_encontrado = self._extract_consultor(query)
            datas_encontradas = self._extract_dates(query)
            # Se tem consultor OU data, é definitivamente uma pergunta de disponibilidade
            if consultor_encontrado or datas_encontradas:
                print(f"[DEBUG] Intenção identificada: disponibilidade (palavra-chave prioritária)")
                return "disponibilidade"
        
        # Verificar se tem consultor + data
        consultor_encontrado = self._extract_consultor(query)
        datas_encontradas = self._extract_dates(query)
        
        # DEBUG
        print(f"[DEBUG] Query: {query}")
        print(f"[DEBUG] Consultor encontrado: {consultor_encontrado}")
        print(f"[DEBUG] Datas encontradas: {datas_encontradas}")
        
        # Palavras-chave para listar (devem incluir plural ou "todas")
        listar_keywords = ['liste', 'listar', 'mostre todas', 'exiba todas', 'todas as agendas', 'todos os', 'lista de']
        if any(keyword in query_lower for keyword in listar_keywords):
            print(f"[DEBUG] Intenção identificada: listar")
            return "listar"
        
        # Palavras que indicam consulta (sem livre/ocupado)
        consulta_keywords = ['mostre', 'exiba', 'ver', 'veja', 'consultar', 'qual', 'quais', 'quem', 'onde', 'quando']
        tem_palavra_consulta = any(keyword in query_lower for keyword in consulta_keywords)
        
        # Se tem consultor E data + palavra de consulta, é consulta
        if consultor_encontrado and datas_encontradas and tem_palavra_consulta:
            print(f"[DEBUG] Intenção identificada: consulta (consultor+data+palavra)")
            return "consulta"
        
        # Se tem consultor OU data + palavra de consulta, é consulta
        if (consultor_encontrado or datas_encontradas) and tem_palavra_consulta:
            print(f"[DEBUG] Intenção identificada: consulta (filtro+palavra)")
            return "consulta"
        
        # Se tem apenas consultor ou data sem palavra específica, é consulta
        if consultor_encontrado or datas_encontradas:
            print(f"[DEBUG] Intenção identificada: consulta (apenas filtros)")
            return "consulta"
        
        # Padrão: consulta (melhor do que listar tudo)
        print(f"[DEBUG] Intenção identificada: consulta (padrão)")
        return "consulta"
    
    def _handle_consulta(self, query: str, agendas: List[Dict]) -> str:
        """Trata consultas sobre agendas específicas com filtragem inteligente"""
        consultor = self._extract_consultor(query)
        datas = self._extract_dates(query)
        projeto = self._extract_projeto(query)
        os_num = self._extract_os(query)
        
        # DEBUG: Remover após testes
        print(f"[CONSULTA DEBUG] Consultor: {consultor}, Datas: {datas}, Projeto: {projeto}, OS: {os_num}")
        
        # Se não encontrou nenhum filtro específico, listar resumo
        if not consultor and not datas and not projeto and not os_num:
            # Agrupar por consultor e mostrar resumo
            consultores_stats = {}
            for agenda in agendas:
                cons = agenda['consultor']
                consultores_stats[cons] = consultores_stats.get(cons, 0) + 1
            
            resposta = f"### 📊 Resumo Geral\n\n"
            resposta += f"**Total:** {len(agendas)} agendas cadastradas\n\n"
            for cons, count in sorted(consultores_stats.items()):
                resposta += f"• **{cons}:** {count} agendas\n"
            resposta += f"\n💡 Para consultas específicas, mencione o consultor ou data.\n"
            resposta += f"**Exemplos:** _Sirlene dia 20/12_, _André em março_"
            return resposta
        
        # Função auxiliar de filtragem
        def aplicar_filtros(c, d, p, o):
            res = agendas
            if c:
                res = [a for a in res if self.normalize_text(c) in self.normalize_text(a['consultor'])]
            if d:
                data_inicio, data_fim = d
                res = [
                    a for a in res
                    if not (datetime.strptime(a['data_fim'], "%Y-%m-%d").date() < data_inicio or
                           datetime.strptime(a['data_inicio'], "%Y-%m-%d").date() > data_fim)
                ]
            if p:
                res = [a for a in res if self.normalize_text(p) in self.normalize_text(a['projeto'])]
            if o:
                res = [a for a in res if o in str(a['os'])]
            return res

        # Tentar filtragem inicial
        agendas_filtradas = aplicar_filtros(consultor, datas, projeto, os_num)
        
        # FALLBACK INTELIGENTE:
        # Se filtrou por consultor e não achou nada, mas o nome pode ser um projeto
        # Ex: "Agendas da Natália" (Natália é projeto, não consultora)
        if not agendas_filtradas and consultor and not projeto:
            print(f"[DEBUG] Tentando fallback: Consultor '{consultor}' como Projeto")
            agendas_fallback = aplicar_filtros(None, datas, consultor, os_num)
            if agendas_fallback:
                agendas_filtradas = agendas_fallback
                projeto = consultor # Atualiza para exibir corretamente na resposta
                consultor = None # Remove consultor pois era projeto

        # Formatar resposta
        if not agendas_filtradas:
            filtros = []
            if consultor:
                filtros.append(f"consultor **{consultor}**")
            if datas:
                data_inicio_fmt = data_inicio.strftime("%d/%m/%Y")
                data_fim_fmt = data_fim.strftime("%d/%m/%Y")
                if data_inicio == data_fim:
                    filtros.append(f"data **{data_inicio_fmt}**")
                else:
                    filtros.append(f"período **{data_inicio_fmt} a {data_fim_fmt}**")
            if projeto:
                filtros.append(f"projeto **{projeto}**")
            if os_num:
                filtros.append(f"OS **{os_num}**")
            
            filtros_txt = ", ".join(filtros)
            return f"📭 Não encontrei agendas para {filtros_txt}."
        
        # Criar cabeçalho da resposta
        resposta = f"### 📋 Resultado da Consulta\n\n"
        
        # Mostrar filtros aplicados
        if consultor:
            resposta += f"👤 **Consultor:** {consultor}\n"
        if datas:
            data_inicio_fmt = data_inicio.strftime("%d/%m/%Y")
            data_fim_fmt = data_fim.strftime("%d/%m/%Y")
            if data_inicio == data_fim:
                resposta += f"📅 **Data:** {data_inicio_fmt}\n"
            else:
                resposta += f"📅 **Período:** {data_inicio_fmt} a {data_fim_fmt}\n"
        if projeto:
            resposta += f"📁 **Projeto:** {projeto}\n"
        if os_num:
            resposta += f"📋 **OS:** {os_num}\n"
        
        resposta += f"\n---\n\n"
        
        # Usar singular/plural correto
        qtd_text = "1 agenda" if len(agendas_filtradas) == 1 else f"{len(agendas_filtradas)} agendas"
        resposta += f"✅ **Encontrado:** {qtd_text}\n\n"
        resposta += f"---\n\n"
        
        for agenda in agendas_filtradas[:10]:  # Limitar a 10
            inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").strftime("%d/%m/%Y")
            fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").strftime("%d/%m/%Y")
            is_vago = agenda.get('is_vago', False) or agenda.get('projeto', '').upper() in ['VAGO', 'LIVRE']
            
            resposta += f"• **Consultor:** {agenda['consultor']}\n"
            
            if is_vago:
                resposta += f"  **Status:** 🟢 DISPONÍVEL (agenda vaga)\n"
            else:
                resposta += f"  **Projeto:** {agenda['projeto']}\n"
                if agenda.get('os'):
                    resposta += f"  **OS:** {agenda['os']}\n"
                if agenda.get('gerente'):
                    resposta += f"  **Gerente:** {agenda['gerente']}\n"
            
            resposta += f"  📅 **Período:** {inicio} até {fim}\n\n"
        
        if len(agendas_filtradas) > 10:
            qtd_mais = len(agendas_filtradas) - 10
            mais_text = "1 agenda" if qtd_mais == 1 else f"{qtd_mais} agendas"
            resposta += f"---\n\n_... e mais {mais_text}. Use o Dashboard para ver todas._"
        
        return resposta
    
    def _handle_disponibilidade(self, query: str, agendas: List[Dict]) -> str:
        """Verifica disponibilidade de consultores com maior precisão"""
        consultor = self._extract_consultor(query)
        datas = self._extract_dates(query)
        
        if not consultor:
            return ("❓ Para verificar disponibilidade, mencione o nome do consultor.\n\n"
                   "**Exemplos:**\n"
                   "- _André está livre amanhã?_\n"
                   "- _Sirlene pode dia 15?_\n"
                   "- _Miguel disponível próxima semana?_")
        
        if not datas:
            # Se não especificou data, usar hoje como padrão
            hoje = datetime.now().date()
            data_inicio = hoje
            data_fim = hoje
        else:
            data_inicio, data_fim = datas
        
        # Buscar agendas do consultor
        agendas_consultor = [
            a for a in agendas
            if consultor.lower() in a['consultor'].lower()
        ]
        
        # Se não encontrou o consultor
        if not agendas_consultor:
            return f"❓ Não encontrei agendas para o consultor **{consultor}**. Verifique o nome."
        
        # Buscar conflitos no período específico (ignorando agendas VAGO)
        conflitos = []
        for agenda in agendas_consultor:
            # Ignorar agendas vagas
            is_vago = agenda.get('is_vago', False) or agenda.get('projeto', '').upper() in ['VAGO', 'LIVRE']
            if is_vago:
                continue
                
            agenda_inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").date()
            agenda_fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").date()
            
            # Verificar sobreposição
            if not (data_fim < agenda_inicio or data_inicio > agenda_fim):
                conflitos.append(agenda)
        
        # Formatar período
        if data_inicio == data_fim:
            periodo_str = data_inicio.strftime('%d/%m/%Y')
            periodo_label = f"dia {periodo_str}"
        else:
            periodo_str = f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
            periodo_label = f"período de {periodo_str}"
        
        # Resposta direta e objetiva
        if not conflitos:
            return f"✅ **SIM, {consultor} está livre no {periodo_label}!** 🟢"
        
        # Se tem conflitos, mostrar quantos
        qtd_conflitos = len(conflitos)
        conflito_text = "1 agenda" if qtd_conflitos == 1 else f"{qtd_conflitos} agendas"
        
        resposta = f"❌ **NÃO, {consultor} está ocupado(a) no {periodo_label}.**\n\n"
        resposta += f"🔴 {conflito_text} neste período:\n\n"
        
        for c in conflitos:
            inicio = datetime.strptime(c['data_inicio'], "%Y-%m-%d").strftime("%d/%m/%Y")
            fim = datetime.strptime(c['data_fim'], "%Y-%m-%d").strftime("%d/%m/%Y")
            os_info = f" (OS: {c['os']})" if c.get('os') else ""
            gerente_info = f" - Gerente: {c['gerente']}" if c.get('gerente') else ""
            resposta += f"• **{c['projeto']}**{os_info}{gerente_info}\n"
            resposta += f"  📅 {inicio} até {fim}\n\n"
        
        return resposta
    
    def _handle_criar_agenda(self, query: str) -> Dict:
        """Auxilia na criação de uma nova agenda"""
        consultor = self._extract_consultor(query)
        projeto = self._extract_projeto(query)
        os = self._extract_os(query)
        datas = self._extract_dates(query)
        
        # Montar resposta com instruções
        resposta = "📝 Para criar uma agenda, preciso das seguintes informações:\n\n"
        
        info_faltando = []
        
        if consultor:
            resposta += f"✅ **Consultor:** {consultor}\n"
        else:
            info_faltando.append("Nome do consultor")
        
        if projeto:
            resposta += f"✅ **Projeto:** {projeto}\n"
        else:
            info_faltando.append("Nome do projeto")
        
        if os:
            resposta += f"✅ **OS:** {os}\n"
        else:
            info_faltando.append("Número da OS")
        
        if datas:
            resposta += f"✅ **Período:** {datas[0].strftime('%d/%m/%Y')} a {datas[1].strftime('%d/%m/%Y')}\n"
        else:
            info_faltando.append("Datas (início e fim)")
        
        if info_faltando:
            resposta += f"\n❌ **Informações faltando:** {', '.join(info_faltando)}\n\n"
            resposta += "**Exemplo de comando completo:**\n"
            resposta += "_Agende o consultor João Silva para o Projeto Alpha, OS 12345, de 15/01/2025 a 20/01/2025_"
            return {"text": resposta, "action": None}
        else:
            # Criar comando para inserção manual
            resposta += f"\n✨ **Todas as informações foram coletadas!**\n\n"
            resposta += f"Confirme os dados abaixo para criar a agenda:\n"
            resposta += f"- **Consultor:** {consultor}\n"
            resposta += f"- **Projeto:** {projeto}\n"
            resposta += f"- **OS:** {os}\n"
            resposta += f"- **Período:** {datas[0].strftime('%d/%m/%Y')} a {datas[1].strftime('%d/%m/%Y')}\n"
            
            return {
                "text": resposta,
                "action": {
                    "type": "create_agenda",
                    "data": {
                        "consultor": consultor,
                        "projeto": projeto,
                        "os": os,
                        "data_inicio": datas[0].strftime('%Y-%m-%d'),
                        "data_fim": datas[1].strftime('%Y-%m-%d')
                    }
                }
            }
    
    def _handle_listar(self, query: str, agendas: List[Dict]) -> str:
        """Lista agendas com filtros"""
        if not agendas:
            return "📭 Não há agendas cadastradas no momento."
        
        query_lower = query.lower()
        
        # Verificar filtros
        consultor = self._extract_consultor(query)
        projeto = self._extract_projeto(query)
        
        agendas_filtradas = agendas
        
        if consultor:
            agendas_filtradas = [
                a for a in agendas_filtradas
                if consultor.lower() in a['consultor'].lower()
            ]
        
        if projeto:
            agendas_filtradas = [
                a for a in agendas_filtradas
                if projeto.lower() in a['projeto'].lower()
            ]
        
        if not agendas_filtradas:
            return f"📭 Não encontrei agendas com os filtros especificados."
        
        resposta = f"📋 **Total de agendas:** {len(agendas_filtradas)}\n\n"
        
        # Agrupar por consultor
        consultores = {}
        for agenda in agendas_filtradas:
            cons = agenda['consultor']
            if cons not in consultores:
                consultores[cons] = []
            consultores[cons].append(agenda)
        
        for cons, ags in list(consultores.items())[:5]:  # Limitar a 5 consultores
            resposta += f"**👤 {cons}** ({len(ags)} agenda(s)):\n"
            for ag in ags[:3]:  # Limitar a 3 agendas por consultor
                inicio = datetime.strptime(ag['data_inicio'], "%Y-%m-%d").strftime("%d/%m/%Y")
                fim = datetime.strptime(ag['data_fim'], "%Y-%m-%d").strftime("%d/%m/%Y")
                resposta += f"  • {ag['projeto']} (OS {ag['os']}): {inicio} - {fim}\n"
            resposta += "\n"
        
        resposta += "_💡 Use o Dashboard para visualização completa e filtros avançados._"
        
        return resposta
    
    def _interpret_query_with_cohere(self, query: str, agendas: List[Dict]) -> str:
        """Usa Cohere para interpretar a query e filtrar dados relevantes"""
        try:
            # Extrair filtros usando métodos determinísticos
            consultor = self._extract_consultor(query)
            datas = self._extract_dates(query)
            projeto = self._extract_projeto(query)
            os_num = self._extract_os(query)
            
            print(f"[COHERE DEBUG] Consultor: {consultor}, Datas: {datas}, Projeto: {projeto}, OS: {os_num}")
            
            # Filtrar agendas
            agendas_filtradas = agendas
            
            if consultor:
                agendas_filtradas = [
                    a for a in agendas_filtradas 
                    if consultor.lower() in a['consultor'].lower()
                ]
            
            if datas:
                data_inicio, data_fim = datas
                agendas_filtradas = [
                    a for a in agendas_filtradas
                    if not (datetime.strptime(a['data_fim'], "%Y-%m-%d").date() < data_inicio or
                           datetime.strptime(a['data_inicio'], "%Y-%m-%d").date() > data_fim)
                ]
            
            if projeto:
                agendas_filtradas = [
                    a for a in agendas_filtradas
                    if projeto.lower() in a['projeto'].lower()
                ]
            
            if os_num:
                agendas_filtradas = [
                    a for a in agendas_filtradas
                    if os_num in str(a['os'])
                ]
            
            # Preparar contexto para o Cohere
            if agendas_filtradas:
                context = "Agendas encontradas:\n\n"
                for i, agenda in enumerate(agendas_filtradas[:20], 1):
                    inicio = datetime.strptime(agenda['data_inicio'], "%Y-%m-%d").strftime("%d/%m/%Y")
                    fim = datetime.strptime(agenda['data_fim'], "%Y-%m-%d").strftime("%d/%m/%Y")
                    context += f"{i}. Consultor: {agenda['consultor']}, Projeto: {agenda['projeto']}, "
                    context += f"OS: {agenda['os']}, Período: {inicio} até {fim}\n"
                
                if len(agendas_filtradas) > 20:
                    context += f"\n... e mais {len(agendas_filtradas) - 20} agendas.\n"
            else:
                context = "Nenhuma agenda encontrada com os filtros aplicados."
            
            # Montar prompt para o Cohere
            filtros_aplicados = []
            if consultor:
                filtros_aplicados.append(f"Consultor: {consultor}")
            if datas:
                data_inicio_fmt = datas[0].strftime("%d/%m/%Y")
                data_fim_fmt = datas[1].strftime("%d/%m/%Y")
                if datas[0] == datas[1]:
                    filtros_aplicados.append(f"Data: {data_inicio_fmt}")
                else:
                    filtros_aplicados.append(f"Período: {data_inicio_fmt} a {data_fim_fmt}")
            if projeto:
                filtros_aplicados.append(f"Projeto: {projeto}")
            if os_num:
                filtros_aplicados.append(f"OS: {os_num}")
            
            filtros_texto = ", ".join(filtros_aplicados) if filtros_aplicados else "Nenhum filtro específico"
            
            # Usar nova API Chat do Cohere
            message = f"""Pergunta do usuário: {query}

Filtros aplicados: {filtros_texto}

{context}

Total de agendas encontradas: {len(agendas_filtradas)}

IMPORTANTE: 
- Responda de forma clara e objetiva em português brasileiro
- Se encontrou agendas, liste as principais (máximo 10) com formatação clara
- Use emojis para deixar mais visual: 👤 para consultor, 📁 para projeto, 📋 para OS, 📅 para datas
- Se não encontrou nada, explique e sugira verificar o nome ou data
- Se encontrou muitas (mais de 10), liste as 10 primeiras e informe quantas mais existem
- Seja direto e preciso na resposta"""
            
            response = self.client.chat(
                model='command-r7b-12-2024',
                message=message,
                temperature=0.3,
                max_tokens=800
            )
            
            resposta_cohere = response.text.strip()
            print(f"[COHERE DEBUG] Resposta gerada: {len(resposta_cohere)} caracteres")
            
            return resposta_cohere
            
        except Exception as e:
            return f"❌ Erro ao processar com IA: {str(e)}\n\nTente reformular sua pergunta ou use o Dashboard."
    
    def _extract_consultor(self, text: str) -> str:
        """Extrai nome do consultor do texto com maior precisão"""
        # Lista de consultores conhecidos para melhor matching
        consultores_conhecidos = ['André', 'Andre', 'Gracina', 'Sirlene', 'Mayara', 'Miguel', 'Lucas']
        
        text_lower = text.lower()
        
        # Verificar consultores conhecidos primeiro (case-insensitive)
        for consultor in consultores_conhecidos:
            if consultor.lower() in text_lower:
                return consultor
        
        # Padrões de extração
        patterns = [
            r'consultor[a]?\s+([A-ZÀ-Ú][a-zà-ú]+(?:\s+[A-ZÀ-Ú][a-zà-ú]+)?)',
            r'(?:do|da|de|o|a)\s+([A-ZÀ-Ú][a-zà-ú]+(?:\s+[A-ZÀ-Ú][a-zà-ú]+)?)',
            r'([A-ZÀ-Ú][a-zà-ú]+(?:\s+[A-ZÀ-Ú][a-zà-ú]+)?)\s+(?:está|tem|pode|livre|ocupado)',
            r'agende\s+(?:o|a)?\s*([A-ZÀ-Ú][a-zà-ú]+(?:\s+[A-ZÀ-Ú][a-zà-ú]+)?)',
            r'agendas?\s+(?:do|da|de)\s+([A-ZÀ-Ú][a-zà-ú]+(?:\s+[A-ZÀ-Ú][a-zà-ú]+)?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                nome = match.group(1).strip()
                # Validar se não é uma palavra comum
                palavras_ignorar = ['consultor', 'consultora', 'projeto', 'agenda']
                if nome.lower() not in palavras_ignorar:
                    return nome
        
        return None
    
    def _extract_projeto(self, text: str) -> str:
        """Extrai nome do projeto do texto"""
        patterns = [
            r'[Pp]rojeto\s+([A-ZÀ-Ú][A-Za-zà-ú0-9\s]+?)(?:\s*,|\s+OS|\s+os|\s*$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()
        
        return None
    
    def _extract_os(self, text: str) -> str:
        """Extrai número da OS do texto"""
        patterns = [
            r'OS\s*[:\-]?\s*(\d+)',
            r'os\s*[:\-]?\s*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_dates(self, text: str) -> tuple:
        """Extrai datas do texto com padrões mais abrangentes"""
        hoje = datetime.now().date()
        text_lower = text.lower()
        
        # Datas relativas simples
        if any(word in text_lower for word in ['hoje', 'hoje?', 'hje']):
            return (hoje, hoje)
        
        if any(word in text_lower for word in ['amanhã', 'amanha', 'amanhã?', 'amanha?']):
            amanha = hoje + timedelta(days=1)
            return (amanha, amanha)
        
        if 'depois de amanhã' in text_lower or 'depois de amanha' in text_lower:
            depois = hoje + timedelta(days=2)
            return (depois, depois)
        
        # Dias da semana
        dias_semana = {
            'segunda': 0, 'segunda-feira': 0, 'seg': 0,
            'terça': 1, 'terca': 1, 'terça-feira': 1, 'terca-feira': 1, 'ter': 1,
            'quarta': 2, 'quarta-feira': 2, 'qua': 2,
            'quinta': 3, 'quinta-feira': 3, 'qui': 3,
            'sexta': 4, 'sexta-feira': 4, 'sex': 4,
            'sábado': 5, 'sabado': 5, 'sab': 5,
            'domingo': 6, 'dom': 6
        }
        
        for dia_nome, dia_num in dias_semana.items():
            if dia_nome in text_lower:
                dias_ate_dia = (dia_num - hoje.weekday()) % 7
                if dias_ate_dia == 0:
                    dias_ate_dia = 7  # Próxima ocorrência
                data_alvo = hoje + timedelta(days=dias_ate_dia)
                return (data_alvo, data_alvo)
        
        # Semanas
        if 'próxima semana' in text_lower or 'semana que vem' in text_lower or 'proxima semana' in text_lower:
            inicio = hoje + timedelta(days=(7 - hoje.weekday()))
            fim = inicio + timedelta(days=6)
            return (inicio, fim)
        
        if 'esta semana' in text_lower or 'essa semana' in text_lower:
            inicio = hoje - timedelta(days=hoje.weekday())
            fim = inicio + timedelta(days=6)
            return (inicio, fim)
        
        # Meses por nome
        meses_nome = {
            'janeiro': 1, 'jan': 1,
            'fevereiro': 2, 'fev': 2,
            'março': 3, 'marco': 3, 'mar': 3,
            'abril': 4, 'abr': 4,
            'maio': 5, 'mai': 5,
            'junho': 6, 'jun': 6,
            'julho': 7, 'jul': 7,
            'agosto': 8, 'ago': 8,
            'setembro': 9, 'set': 9,
            'outubro': 10, 'out': 10,
            'novembro': 11, 'nov': 11,
            'dezembro': 12, 'dez': 12
        }
        
        for mes_nome, mes_num in meses_nome.items():
            if mes_nome in text_lower:
                ano = hoje.year
                # Se o mês já passou, assume ano seguinte
                if mes_num < hoje.month:
                    ano += 1
                elif mes_num == hoje.month and 'próximo' in text_lower:
                    ano += 1
                
                inicio = datetime(ano, mes_num, 1).date()
                if mes_num == 12:
                    fim = datetime(ano, 12, 31).date()
                else:
                    fim = (datetime(ano, mes_num + 1, 1) - timedelta(days=1)).date()
                return (inicio, fim)
        
        # "este mês" / "próximo mês"
        if 'este mês' in text_lower or 'esse mês' in text_lower or 'este mes' in text_lower:
            inicio = hoje.replace(day=1)
            if hoje.month == 12:
                fim = hoje.replace(day=31)
            else:
                fim = (hoje.replace(month=hoje.month + 1, day=1) - timedelta(days=1))
            return (inicio, fim)
        
        if 'próximo mês' in text_lower or 'mês que vem' in text_lower or 'proximo mes' in text_lower:
            if hoje.month == 12:
                inicio = hoje.replace(year=hoje.year + 1, month=1, day=1)
                fim = inicio.replace(day=31)
            else:
                inicio = hoje.replace(month=hoje.month + 1, day=1)
                fim = (inicio.replace(month=inicio.month + 1, day=1) - timedelta(days=1))
            return (inicio, fim)
        
        # Datas específicas (formato dd/mm/yyyy ou dd/mm/yy ou dd/mm)
        # PRIORIDADE: Processar ANTES de "dia X"
        date_pattern = r'(\d{1,2})[\/\-](\d{1,2})(?:[\/\-](\d{2,4}))?'
        matches = re.findall(date_pattern, text)
        
        if matches:
            dates = []
            for match in matches:
                try:
                    dia, mes, ano = match[0], match[1], match[2]
                    
                    # Se não tem ano, usar ano atual ou próximo
                    if not ano or ano == '':
                        ano_ref = hoje.year
                        mes_num = int(mes)
                        # Se o mês já passou, assumir ano seguinte
                        if mes_num < hoje.month or (mes_num == hoje.month and int(dia) < hoje.day):
                            ano_ref += 1
                        ano = str(ano_ref)
                    elif len(ano) == 2:
                        ano = '20' + ano
                    
                    data = datetime.strptime(f"{dia}/{mes}/{ano}", "%d/%m/%Y").date()
                    dates.append(data)
                except:
                    continue
            
            if len(dates) >= 2:
                return (min(dates), max(dates))
            elif len(dates) == 1:
                return (dates[0], dates[0])
        
        # Dia específico "dia 15", "dia 20" (apenas quando NÃO tem barra)
        if '/' not in text and '-' not in text:
            dia_pattern = r'dia\s+(\d{1,2})(?:\s|$|,|\?|!)'
            match = re.search(dia_pattern, text_lower)
            if match:
                dia = int(match.group(1))
                try:
                    data_alvo = hoje.replace(day=dia)
                    # Se o dia já passou neste mês, assume próximo mês
                    if data_alvo < hoje:
                        if hoje.month == 12:
                            data_alvo = datetime(hoje.year + 1, 1, dia).date()
                        else:
                            data_alvo = datetime(hoje.year, hoje.month + 1, dia).date()
                    return (data_alvo, data_alvo)
                except ValueError:
                    pass
        
        # Extrair "dias X a Y"
        dias_pattern = r'dia[s]?\s+(\d+)\s+a[té]?\s+(\d+)'
        match = re.search(dias_pattern, text_lower)
        if match:
            dia_inicio = int(match.group(1))
            dia_fim = int(match.group(2))
            
            mes_ref = hoje.month
            ano_ref = hoje.year
            
            try:
                data_inicio = datetime(ano_ref, mes_ref, dia_inicio).date()
                data_fim = datetime(ano_ref, mes_ref, dia_fim).date()
                return (data_inicio, data_fim)
            except:
                pass
        
        return None
