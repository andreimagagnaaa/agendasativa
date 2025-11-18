# 🚀 Guia de Deploy - Sistema de Agendas Ativa

## 📋 Status Atual

❌ **Vercel**: Não recomendado para Streamlit (serverless timeout)
✅ **GitHub**: Repositório configurado e atualizado

## 🎯 Plataformas Recomendadas para Streamlit

### 1. 🌟 **Streamlit Cloud** (Mais Fácil - Recomendado)

#### Vantagens:
- ✅ Gratuito para projetos pessoais
- ✅ Deploy direto do GitHub
- ✅ Otimizado para Streamlit
- ✅ Auto-scaling
- ✅ Sem configuração complexa

#### Como fazer deploy:

1. **Acesse:** https://share.streamlit.io/
2. **Conecte sua conta GitHub**
3. **Selecione o repositório:** `andreimagagnaaa/agendasativa`
4. **Configure:**
   - **Main file:** `app.py`
   - **Python version:** 3.9 ou superior
5. **Deploy!** 🚀

#### URL resultante:
```
https://agendasativa.streamlit.app
```

---

### 2. 🐘 **Heroku** (Profissional)

#### Vantagens:
- ✅ Plano gratuito disponível
- ✅ Suporte completo a Python
- ✅ Banco de dados PostgreSQL integrado
- ✅ Logs detalhados
- ✅ Auto-scaling

#### Arquivos necessários:

**requirements.txt** (já existe)
**Procfile:**
```
web: streamlit run app.py --server.port $PORT --server.headless true
```

**runtime.txt:**
```
python-3.12.0
```

#### Como fazer deploy:

1. **Instale Heroku CLI**
2. **Login:** `heroku login`
3. **Crie app:** `heroku create agendas-ativa`
4. **Configure variáveis:**
   ```bash
   heroku config:set SUPABASE_URL="your_url"
   heroku config:set SUPABASE_KEY="your_key"
   heroku config:set COHERE_API_KEY="your_key"
   ```
5. **Deploy:** `git push heroku master`

---

### 3. 🚂 **Railway** (Moderno e Simples)

#### Vantagens:
- ✅ Deploy direto do GitHub
- ✅ PostgreSQL integrado
- ✅ Auto-scaling
- ✅ Interface moderna
- ✅ Preços acessíveis

#### Arquivos necessários:

**requirements.txt** (já existe)
**railway.json:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run app.py --server.port $PORT --server.headless true"
  }
}
```

#### Como fazer deploy:

1. **Acesse:** https://railway.app/
2. **Conecte GitHub**
3. **Selecione repositório**
4. **Deploy automático**

---

### 4. 🐳 **Docker + Cloud** (Avançado)

#### Dockerfile:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]
```

#### Deploy em:
- **DigitalOcean App Platform**
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**

---

### 5. ☁️ **AWS EC2** (Máximo Controle)

#### Vantagens:
- ✅ Controle total
- ✅ Escalabilidade infinita
- ✅ Custos previsíveis
- ✅ Alta disponibilidade

#### Setup básico:

```bash
# Instalar Python e dependências
sudo apt update
sudo apt install python3 python3-pip
pip install -r requirements.txt

# Configurar como serviço
sudo nano /etc/systemd/system/streamlit.service
```

**streamlit.service:**
```ini
[Unit]
Description=Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/agendasativa
ExecStart=/home/ubuntu/.local/bin/streamlit run app.py --server.port 8501 --server.headless true
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🔧 Configurações Comuns

### Variáveis de Ambiente

Todas as plataformas precisam destas variáveis:

```bash
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
COHERE_API_KEY=kk6JjxQxYXNngcxx1RJiZtD6ZGL1MzeJAzysE9ym
```

### Configurações Streamlit

Para produção, use:
```bash
streamlit run app.py --server.headless true --server.port $PORT
```

---

## 📊 Comparação de Plataformas

| Plataforma | Facilidade | Custo | Escalabilidade | Recomendado |
|------------|------------|-------|----------------|-------------|
| **Streamlit Cloud** | ⭐⭐⭐⭐⭐ | Gratuito | ⭐⭐⭐ | ✅ Iniciante |
| **Railway** | ⭐⭐⭐⭐ | $5/mês | ⭐⭐⭐⭐ | ✅ Intermediário |
| **Heroku** | ⭐⭐⭐ | $7/mês | ⭐⭐⭐ | ✅ Profissional |
| **AWS EC2** | ⭐⭐ | $10+/mês | ⭐⭐⭐⭐⭐ | ✅ Avançado |
| **Vercel** | ⭐ | ❌ | ❌ | ❌ Não recomendado |

---

## 🚀 Recomendação Final

### Para começar rápido: **Streamlit Cloud**
1. Acesse https://share.streamlit.io/
2. Conecte GitHub
3. Deploy em 2 minutos
4. URL: `https://agendasativa.streamlit.app`

### Para produção profissional: **Railway**
1. Melhor custo-benefício
2. Deploy automático
3. PostgreSQL integrado
4. Escalabilidade automática

---

## ⚠️ Importante

- **Sempre teste localmente** antes do deploy
- **Configure variáveis de ambiente** corretamente
- **Monitore logs** após deploy
- **Faça backup** do banco de dados
- **Atualize dependências** regularmente

---

**🎯 Próximo passo:** Escolha uma plataforma e faça deploy!