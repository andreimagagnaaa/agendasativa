# 🚀 INÍCIO RÁPIDO - Agendas Ativa

## ⚡ 3 Passos para Começar

### 1️⃣ Instalar (2 minutos)

```powershell
# Execute o script automático
.\setup.ps1
```

OU manualmente:

```powershell
pip install -r requirements.txt
```

### 2️⃣ Configurar (3 minutos)

Crie o arquivo `.streamlit\secrets.toml`:

```toml
SUPABASE_URL = "sua_url_aqui"
SUPABASE_KEY = "sua_key_aqui"
COHERE_API_KEY = "sua_key_aqui"
```

**Onde conseguir as chaves:**
- 🗄️ Supabase: https://supabase.com (gratuito)
- 🤖 Cohere: https://cohere.com (gratuito)

### 3️⃣ Executar

```powershell
streamlit run app.py
```

Acesse: http://localhost:8501

---

## 📚 Documentação Completa

- **INSTALL.md** - Guia detalhado de instalação
- **EXAMPLES.md** - Exemplos de uso e comandos
- **README.md** - Documentação técnica completa

## 🆘 Problemas?

Execute o teste de configuração:

```powershell
python test_config.py
```

---

## 🎯 Teste Rápido

Após iniciar a aplicação:

1. Vá em **💬 Chat com IA**
2. Digite: `"Liste todas as agendas"`
3. Pronto! 🎉

---

**Dúvidas? Consulte INSTALL.md para instruções passo a passo**
