# Exemplos de Uso - Agendas Ativa

## 💬 Chat com IA - Exemplos de Comandos

### 📋 Consultas de Agendas

```
"Mostre a agenda do consultor João para dezembro de 2024"
"Liste todas as agendas do Projeto Alpha"
"Quais são as agendas da OS 12345?"
"Mostre todas as agendas deste mês"
"Liste os projetos do consultor Maria"
```

### 🔍 Verificação de Disponibilidade

```
"O consultor Pedro está livre na próxima semana?"
"Maria está disponível entre 15/12 e 20/12?"
"Quais consultores estão livres esta semana?"
"João pode trabalhar de 10/01 a 15/01?"
"Quem está disponível para o próximo mês?"
```

### ➕ Criar Agendas

```
"Agende o consultor Carlos para o Projeto Beta, OS 98765, de 10/12/2024 a 15/12/2024"
"Aloque o consultor Ana no Projeto Gamma, OS 11111, dias 1 a 10 de janeiro"
"Registre agenda: Consultor Pedro, Projeto Delta, OS 22222, 20/01 a 25/01"
```

### 📊 Listagens e Relatórios

```
"Liste todas as agendas"
"Mostre todos os consultores"
"Quais projetos estão ativos?"
"Liste as agendas da próxima semana"
"Mostre agendas do mês passado"
```

## 🎯 Casos de Uso Práticos

### Caso 1: Gestor precisa alocar consultor

**Situação**: Novo projeto começando em 15/01/2025

**Comandos**:
1. `"Quais consultores estão livres entre 15/01 e 31/01?"`
2. `"Mostre a agenda do consultor João para janeiro"`
3. `"Agende o consultor João para o Projeto Novo, OS 55555, de 15/01 a 31/01"`

### Caso 2: Verificar conflitos de agenda

**Situação**: Cliente quer marcar reunião com consultor

**Comandos**:
1. `"Maria está disponível dia 20/12?"`
2. `"Mostre a agenda da Maria para esta semana"`
3. `"Lista todas as agendas da Maria"`

### Caso 3: Planejamento mensal

**Situação**: Início do mês, precisar ver panorama geral

**Comandos**:
1. `"Liste todas as agendas deste mês"`
2. `"Quais projetos estão ativos?"`
3. `"Mostre agendas por consultor"`

### Caso 4: Consultor verifica própria agenda

**Situação**: Consultor quer ver seus compromissos

**Comandos**:
1. `"Mostre a agenda do consultor Pedro"`
2. `"Minha agenda para esta semana"` (se nome estiver no contexto)
3. `"Quais são meus projetos?"` (se nome estiver no contexto)

## 📊 Dashboard - Como Usar

### Filtros Disponíveis

1. **Por Consultor**: Selecione um consultor específico
2. **Por Projeto**: Filtre por nome do projeto
3. **Por OS**: Busque por número de OS
4. **Por Período**:
   - Todos
   - Esta Semana
   - Este Mês
   - Próximos 30 Dias
   - Personalizado (escolha datas)

### Visualizações

#### 📇 Cards
- Visualização em cards coloridos
- Status visual (Em andamento, Agendado, Concluído)
- Informações completas de cada agenda
- Botão para excluir agenda

#### 📅 Tabela
- Visualização tabular completa
- Exportação para CSV
- Ordenação por colunas
- Fácil leitura de dados

#### 📈 Gráficos
- **Agendas por Consultor**: Gráfico de barras horizontal
- **Distribuição por Projeto**: Gráfico de pizza
- **Timeline**: Visualização temporal das alocações

## 🔧 Uso Programático (API)

### Conectar ao Banco

```python
from database import Database

db = Database()
```

### Criar Agenda

```python
sucesso = db.create_agenda(
    consultor="João Silva",
    data_inicio="2025-01-15",
    data_fim="2025-01-31",
    projeto="Projeto Alpha",
    os="12345"
)
```

### Buscar Agendas

```python
# Todas as agendas
todas = db.get_all_agendas()

# Por consultor
agendas_joao = db.get_agendas_by_consultor("João")

# Por projeto
agendas_projeto = db.get_agendas_by_projeto("Alpha")

# Por período
agendas_periodo = db.get_agendas_by_date_range(
    "2025-01-01",
    "2025-01-31"
)
```

### Verificar Disponibilidade

```python
resultado = db.check_disponibilidade(
    consultor="Maria",
    data_inicio="2025-01-15",
    data_fim="2025-01-20"
)

if resultado["disponivel"]:
    print("Consultor está livre!")
else:
    print(f"Conflitos: {resultado['mensagem']}")
```

### Atualizar Agenda

```python
sucesso = db.update_agenda(
    agenda_id=1,
    projeto="Novo Nome do Projeto"
)
```

### Deletar Agenda

```python
sucesso = db.delete_agenda(agenda_id=1)
```

## 🤖 IA Assistant - Uso Programático

```python
from ai_assistant import AIAssistant

ai = AIAssistant()
agendas = db.get_all_agendas()

resposta = ai.process_query(
    "Quem está livre esta semana?",
    agendas
)

print(resposta)
```

## 💡 Dicas de Uso

### Para Gestores

1. **Planejamento Semanal**: Toda segunda-feira, pergunte "Liste agendas desta semana"
2. **Alocação Rápida**: Use o chat para verificar disponibilidade antes de alocar
3. **Exportação**: Use o dashboard para exportar relatórios mensais em CSV

### Para Consultores

1. **Verificação Diária**: "Mostre minha agenda de hoje"
2. **Planejamento**: "Quais são meus projetos ativos?"
3. **Timeline**: Use a visualização de timeline no dashboard

### Para Administradores

1. **Análise de Carga**: Use gráficos para ver distribuição de trabalho
2. **Conflitos**: O sistema avisa automaticamente sobre conflitos
3. **Histórico**: Todas as agendas ficam registradas com timestamps

## ⚠️ Boas Práticas

### DO ✅

- Use datas no formato DD/MM/YYYY ou termos relativos ("próxima semana")
- Seja específico ao nomear consultores e projetos
- Verifique disponibilidade antes de criar agendas
- Exporte backups periódicos via CSV

### DON'T ❌

- Não use abreviações ambíguas
- Não esqueça de especificar a OS
- Não crie agendas com datas passadas sem necessidade
- Não delete agendas sem confirmar

## 📱 Atalhos do Teclado

- **Ctrl + K**: Focar no campo de busca (se disponível)
- **Tab**: Navegar entre campos
- **Enter**: Enviar mensagem no chat
- **F5**: Recarregar dashboard

## 🎓 Tutoriais em Vídeo

### 1. Primeiro Acesso (5 min)
- Login e navegação básica
- Conhecendo o chat e dashboard
- Criando primeira agenda

### 2. Uso do Chat com IA (10 min)
- Tipos de perguntas
- Interpretação de respostas
- Comandos avançados

### 3. Dashboard Completo (10 min)
- Uso de filtros
- Interpretação de gráficos
- Exportação de dados

### 4. Casos Práticos (15 min)
- Cenário 1: Alocação de equipe
- Cenário 2: Gestão de conflitos
- Cenário 3: Relatórios gerenciais

---

**📚 Para mais informações, consulte o README.md completo**
