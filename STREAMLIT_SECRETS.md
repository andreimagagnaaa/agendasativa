# Configuração de Secrets para Streamlit Cloud

Para fazer o deploy no Streamlit Cloud, você precisa configurar as seguintes secrets:

1. Acesse seu app em https://share.streamlit.io
2. Vá em **Settings** → **Secrets**
3. Adicione as seguintes variáveis:

```toml
SUPABASE_URL = "https://sua-url.supabase.co"
SUPABASE_ANON_KEY = "sua-chave-anonima-aqui"
COHERE_API_KEY = "sua-chave-cohere-aqui"
```

## Obtendo as Credenciais

### Supabase
1. Acesse https://supabase.com e faça login
2. Selecione seu projeto
3. Vá em **Settings** → **API**
4. Copie:
   - **Project URL** (SUPABASE_URL)
   - **anon public** key (SUPABASE_ANON_KEY)

### Cohere
1. Acesse https://cohere.ai e faça login
2. Vá em **API Keys**
3. Copie sua API key (COHERE_API_KEY)

## Verificação

Após configurar as secrets, o app será reiniciado automaticamente e deverá funcionar corretamente.
