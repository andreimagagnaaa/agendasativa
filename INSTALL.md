# Guia Rápido de Instalação - Agendas Ativa

## ⚡ Instalação Rápida (5 minutos)

### 1️⃣ Instalar Dependências

Abra o PowerShell na pasta do projeto e execute:

```powershell
pip install -r requirements.txt
```

### 2️⃣ Configurar Supabase

1. Acesse: https://supabase.com
2. Clique em "Start your project"
3. Crie uma nova conta (gratuita)
4. Crie um novo projeto:
   - Nome do projeto: "agendas-ativa"
   - Database Password: escolha uma senha forte
   - Região: escolha a mais próxima

5. Aguarde o projeto ser criado (1-2 minutos)

6. No menu lateral, clique em "SQL Editor"
7. Clique em "New query"
8. Copie e cole todo o conteúdo do arquivo `setup_database.sql`
9. Clique em "Run" para executar

10. No menu lateral, vá em "Settings" > "API"
11. Copie:
    - **URL**: campo "Project URL"
    - **Key**: campo "anon public" (service_role key)

### 3️⃣ Configurar Cohere

1. Acesse: https://cohere.com
2. Clique em "Get Started"
3. Crie uma conta (gratuita)
4. No dashboard, clique em "API Keys"
5. Copie sua API Key

### 4️⃣ Configurar Secrets

Crie a pasta `.streamlit` e o arquivo de secrets:

```powershell
mkdir .streamlit
New-Item -Path ".streamlit\secrets.toml" -ItemType File
```

Abra o arquivo `.streamlit\secrets.toml` em um editor de texto e adicione:

```toml
SUPABASE_URL = "cole_aqui_a_url_do_supabase"
SUPABASE_KEY = "cole_aqui_a_key_do_supabase"
COHERE_API_KEY = "cole_aqui_a_key_do_cohere"
```

**Exemplo:**
```toml
SUPABASE_URL = "https://xyzcompany.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
COHERE_API_KEY = "abcd1234efgh5678ijkl..."
```

### 5️⃣ Executar a Aplicação

```powershell
streamlit run app.py
```

A aplicação abrirá automaticamente em: http://localhost:8501

## ✅ Checklist de Verificação

- [ ] Python 3.10+ instalado
- [ ] Todas as dependências instaladas (`pip install -r requirements.txt`)
- [ ] Conta no Supabase criada
- [ ] Tabela `agendas` criada no Supabase
- [ ] URL e Key do Supabase copiadas
- [ ] Conta no Cohere criada
- [ ] API Key do Cohere copiada
- [ ] Arquivo `.streamlit/secrets.toml` criado e configurado
- [ ] Aplicação executando sem erros

## 🎯 Teste Rápido

Após iniciar a aplicação:

1. Acesse a aba **💬 Chat com IA**
2. Digite: "Liste todas as agendas"
3. Você deve ver as agendas de exemplo (ou mensagem de nenhuma agenda)
4. Acesse a aba **📊 Dashboard**
5. Visualize as agendas em cards, tabela e gráficos

## 🐛 Problemas Comuns

### "Erro ao conectar com Supabase"
- Verifique se copiou a URL e Key corretas
- Confirme que o arquivo `secrets.toml` está em `.streamlit/secrets.toml`
- Teste a conexão no dashboard do Supabase

### "Assistente de IA não disponível"
- Verifique se a API Key do Cohere está correta
- Confirme que tem créditos disponíveis na conta Cohere
- A API gratuita tem limite de requisições

### "Tabela agendas não encontrada"
- Execute o script `setup_database.sql` no SQL Editor do Supabase
- Verifique se a tabela foi criada em "Table Editor"

## 📞 Suporte

Se continuar com problemas:
1. Verifique os logs no terminal
2. Revise cada passo do guia
3. Confirme que todas as dependências foram instaladas

## 🚀 Próximos Passos

Após a instalação bem-sucedida:
1. Explore o chat com IA fazendo perguntas
2. Crie algumas agendas de teste
3. Experimente os filtros no dashboard
4. Exporte dados para CSV

**Pronto! Agendas Ativa está funcionando! 🎉**
