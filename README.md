# Agendas Ativa 📅

Plataforma inteligente de gerenciamento de agendas de consultores com IA integrada.

## 🚀 Funcionalidades

- **💬 Chat Inteligente com IA**: Faça perguntas em linguagem natural sobre disponibilidade e agendas
- **📊 Dashboard Visual**: Visualize todas as agendas com filtros avançados
- **🔍 Verificação de Disponibilidade**: Consulte rapidamente se um consultor está livre
- **⚡ Operações Rápidas**: Crie, consulte e atualize agendas em segundos
- **📈 Análises e Gráficos**: Visualizações interativas de distribuição de agendas

## 🛠️ Tecnologias

- **Frontend**: Streamlit
- **Banco de Dados**: Supabase
- **IA**: Cohere API
- **Visualização**: Plotly
- **Linguagem**: Python 3.10+

## 📋 Pré-requisitos

1. Python 3.10 ou superior
2. Conta no Supabase (gratuita)
3. API Key do Cohere (gratuita)

## 🔧 Instalação

### 1. Clone o repositório ou baixe os arquivos

```bash
cd "c:\Users\andre\OneDrive\Área de Trabalho\Ativa"
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure o Supabase

1. Acesse [supabase.com](https://supabase.com) e crie uma conta
2. Crie um novo projeto
3. No SQL Editor, execute o seguinte comando para criar a tabela:

```sql
CREATE TABLE agendas (
    id BIGSERIAL PRIMARY KEY,
    consultor TEXT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    projeto TEXT NOT NULL,
    os TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índices para melhor performance
CREATE INDEX idx_agendas_consultor ON agendas(consultor);
CREATE INDEX idx_agendas_datas ON agendas(data_inicio, data_fim);
CREATE INDEX idx_agendas_projeto ON agendas(projeto);
```

4. Copie a URL do projeto e a chave API (em Settings > API)

### 4. Configure o Cohere

1. Acesse [cohere.com](https://cohere.com) e crie uma conta
2. Obtenha sua API Key gratuita no dashboard

### 5. Configure as variáveis de ambiente

Crie um arquivo `.streamlit/secrets.toml` na pasta do projeto:

```bash
mkdir .streamlit
```

Crie o arquivo `secrets.toml` com o seguinte conteúdo:

```toml
SUPABASE_URL = "sua_url_do_supabase"
SUPABASE_KEY = "sua_chave_do_supabase"
COHERE_API_KEY = "sua_chave_do_cohere"
```

**Alternativa**: Use variáveis de ambiente do sistema:

```bash
# No PowerShell
$env:SUPABASE_URL="sua_url_do_supabase"
$env:SUPABASE_KEY="sua_chave_do_supabase"
$env:COHERE_API_KEY="sua_chave_do_cohere"
```

## 🚀 Como Usar

### Iniciar a aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no seu navegador em `http://localhost:8501`

### Usando o Chat com IA

Exemplos de perguntas:

**Consultas:**
- "Mostre a agenda do consultor João para dezembro"
- "Quais consultores estão livres na próxima semana?"
- "Liste todas as agendas do Projeto Alpha"

**Verificação de Disponibilidade:**
- "O consultor Maria está livre entre 15/12 e 20/12?"
- "Quem está disponível esta semana?"

**Criar Agendas:**
- "Agende o consultor Pedro para o Projeto Beta, OS 12345, de 15/01/2025 a 20/01/2025"

### Usando o Dashboard

1. Acesse a aba **📊 Dashboard**
2. Use os filtros para consultor, projeto, OS e período
3. Visualize em cards, tabela ou gráficos
4. Exporte dados em CSV quando necessário

## 🎨 Design System

**Paleta de Cores:**
- Primária: `#002B49` (Azul Escuro)
- Secundária: `#EDF0F2` (Cinza Claro)
- Suporte: Preto e Branco

## 📊 Estrutura do Banco de Dados

Tabela `agendas`:
- `id`: Identificador único (gerado automaticamente)
- `consultor`: Nome do consultor (obrigatório)
- `data_inicio`: Data de início da agenda (obrigatório)
- `data_fim`: Data de fim da agenda (obrigatório)
- `projeto`: Nome do projeto (obrigatório)
- `os`: Número da Ordem de Serviço (obrigatório)
- `created_at`: Data/hora de criação (automático)

## 🔒 Segurança

- **Nunca commite** o arquivo `secrets.toml` ou `.env` com suas chaves reais
- Use `.gitignore` para excluir arquivos sensíveis
- As chaves do Supabase e Cohere devem ser mantidas privadas

## 📝 Estrutura de Arquivos

```
Ativa/
├── app.py                 # Aplicação principal Streamlit
├── database.py            # Módulo de conexão com Supabase
├── ai_assistant.py        # Assistente de IA com Cohere
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
├── .env.example          # Exemplo de variáveis de ambiente
└── .streamlit/
    └── secrets.toml      # Configurações secretas (não commitar)
```

## 🐛 Troubleshooting

### Erro de conexão com Supabase
- Verifique se a URL e a chave estão corretas
- Confirme que a tabela `agendas` foi criada
- Teste a conexão no dashboard do Supabase

### Erro na API do Cohere
- Verifique se a API Key está válida
- Confirme que não excedeu o limite gratuito
- Tente regenerar a chave no dashboard

### Problemas com datas
- Use o formato DD/MM/YYYY nas perguntas
- Ou use termos como "próxima semana", "este mês"

## 📈 Próximas Funcionalidades

- [ ] Notificações por email
- [ ] Exportação para PDF
- [ ] Integração com calendário (Google Calendar)
- [ ] Relatórios automáticos
- [ ] Aplicativo mobile

## 👥 Suporte

Para dúvidas ou problemas, entre em contato com o administrador do sistema.

## 📄 Licença

Este projeto é proprietário da Ativa.

---

**Desenvolvido com ❤️ para otimizar o gerenciamento de agendas**
