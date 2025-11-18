# ✅ CHECKLIST DE DEPLOYMENT - Agendas Ativa

## 📋 PRÉ-DEPLOYMENT

### Ambiente Local
- [ ] Python 3.10+ instalado
- [ ] Todas as dependências instaladas (`pip install -r requirements.txt`)
- [ ] Script `test_config.py` executado com sucesso
- [ ] Aplicação rodando localmente sem erros
- [ ] Todas as funcionalidades testadas

### Banco de Dados (Supabase)
- [ ] Conta Supabase criada
- [ ] Projeto criado
- [ ] Tabela `agendas` criada (via `setup_database.sql`)
- [ ] Índices criados
- [ ] Row Level Security (RLS) habilitado
- [ ] Políticas de acesso configuradas
- [ ] Dados de teste inseridos e validados
- [ ] Backup configurado (opcional)

### API Keys
- [ ] Cohere API Key obtida
- [ ] Cohere API Key testada
- [ ] Limites de uso verificados
- [ ] Plano apropriado selecionado (free/paid)

### Configuração
- [ ] Arquivo `.streamlit/secrets.toml` criado
- [ ] SUPABASE_URL configurada corretamente
- [ ] SUPABASE_KEY configurada corretamente
- [ ] COHERE_API_KEY configurada corretamente
- [ ] Valores de teste removidos
- [ ] `.gitignore` atualizado

---

## 🚀 DEPLOYMENT

### Opção 1: Streamlit Cloud (Recomendado)

#### Preparação
- [ ] Repositório Git criado
- [ ] Código commitado
- [ ] `.gitignore` verificado
- [ ] Secrets NÃO commitados
- [ ] README.md atualizado
- [ ] requirements.txt validado

#### Deploy no Streamlit Cloud
- [ ] Conta Streamlit Cloud criada (https://streamlit.io/cloud)
- [ ] Repositório conectado
- [ ] Arquivo principal definido (`app.py`)
- [ ] Python version definida (3.10+)
- [ ] Secrets configurados no painel:
  - [ ] SUPABASE_URL
  - [ ] SUPABASE_KEY
  - [ ] COHERE_API_KEY
- [ ] Deploy iniciado
- [ ] Deploy bem-sucedido
- [ ] URL personalizada configurada (opcional)
- [ ] Domínio customizado configurado (opcional)

### Opção 2: Servidor Próprio

#### Preparação do Servidor
- [ ] Servidor Linux/Windows configurado
- [ ] Python 3.10+ instalado
- [ ] Git instalado
- [ ] Firewall configurado (porta 8501)
- [ ] SSL/TLS configurado (HTTPS)
- [ ] Nginx/Apache configurado (opcional)

#### Deploy Manual
- [ ] Código clonado no servidor
- [ ] Virtual environment criado
- [ ] Dependências instaladas
- [ ] Secrets configurados no servidor
- [ ] Variáveis de ambiente definidas
- [ ] Serviço systemd criado (Linux)
- [ ] Auto-restart configurado
- [ ] Logs configurados

### Opção 3: Docker

- [ ] Dockerfile criado
- [ ] docker-compose.yml criado (opcional)
- [ ] Imagem buildada
- [ ] Container testado localmente
- [ ] Imagem publicada (Docker Hub/Registry)
- [ ] Container deployado em produção
- [ ] Volumes persistentes configurados
- [ ] Networks configuradas
- [ ] Health checks implementados

---

## 🔒 SEGURANÇA

### Credenciais
- [ ] Todas as API Keys são únicas para produção
- [ ] Secrets armazenados de forma segura
- [ ] Acesso ao Supabase restrito
- [ ] Políticas RLS revisadas
- [ ] Chaves rotacionadas regularmente (plano)

### Aplicação
- [ ] HTTPS configurado
- [ ] CORS configurado (se necessário)
- [ ] Rate limiting implementado (opcional)
- [ ] Input validation ativa
- [ ] Error handling apropriado
- [ ] Logs não expõem dados sensíveis

### Supabase
- [ ] Row Level Security habilitado
- [ ] Políticas de acesso revisadas
- [ ] Backup automático configurado
- [ ] IP whitelist configurado (se necessário)
- [ ] Monitoramento ativo

---

## ⚙️ PÓS-DEPLOYMENT

### Validação
- [ ] Aplicação acessível via URL
- [ ] Chat com IA funcionando
- [ ] Dashboard carregando
- [ ] Filtros operacionais
- [ ] Gráficos renderizando
- [ ] Exportação CSV funcionando
- [ ] Criação de agendas OK
- [ ] Atualização de agendas OK
- [ ] Exclusão de agendas OK
- [ ] Verificação de disponibilidade OK

### Performance
- [ ] Tempo de resposta < 2s
- [ ] Gráficos carregam rapidamente
- [ ] Sem memory leaks
- [ ] Cache funcionando
- [ ] Queries otimizadas

### Monitoramento
- [ ] Logs sendo gerados
- [ ] Erros sendo capturados
- [ ] Uptime monitorado
- [ ] Performance monitorada
- [ ] Alertas configurados (opcional)

### Documentação
- [ ] URL de produção documentada
- [ ] Credenciais de acesso documentadas (seguro)
- [ ] Procedimentos de backup documentados
- [ ] Contatos de suporte definidos
- [ ] Runbook de incidentes criado

---

## 👥 TREINAMENTO E ADOÇÃO

### Usuários Finais
- [ ] Documentação compartilhada (EXAMPLES.md)
- [ ] Treinamento realizado
- [ ] Casos de uso demonstrados
- [ ] FAQ criado
- [ ] Canal de suporte definido

### Administradores
- [ ] Acesso ao Supabase fornecido
- [ ] Procedimentos de manutenção documentados
- [ ] Backup/restore testado
- [ ] Escalação definida

---

## 📊 MÉTRICAS E KPIs

### Definir e Monitorar
- [ ] Número de usuários ativos
- [ ] Número de agendas criadas/dia
- [ ] Tempo médio de resposta
- [ ] Taxa de erros
- [ ] Uso de API (Cohere)
- [ ] Uso de storage (Supabase)
- [ ] Satisfação dos usuários

---

## 🔄 MANUTENÇÃO CONTÍNUA

### Semanal
- [ ] Verificar logs de erro
- [ ] Revisar métricas de uso
- [ ] Validar backups

### Mensal
- [ ] Atualizar dependências
- [ ] Revisar segurança
- [ ] Análise de performance
- [ ] Feedback dos usuários

### Trimestral
- [ ] Atualização major de dependências
- [ ] Revisão completa de segurança
- [ ] Planejamento de novas features
- [ ] Revisão de custos (APIs)

---

## 🆘 ROLLBACK

### Plano de Contingência
- [ ] Backup do código anterior
- [ ] Backup do banco de dados
- [ ] Procedimento de rollback documentado
- [ ] Testado em ambiente de staging

---

## ✅ SIGN-OFF

### Aprovações
- [ ] Testes funcionais aprovados
- [ ] Testes de segurança aprovados
- [ ] Performance aprovada
- [ ] Documentação aprovada
- [ ] Treinamento realizado
- [ ] Go-live autorizado

---

**Data de Deploy:** _________________

**Responsável:** _________________

**Versão:** 1.0.0

**Status:** ⬜ PENDENTE | ⬜ EM PROGRESSO | ⬜ COMPLETO

---

## 📝 NOTAS ADICIONAIS

```
[Adicione aqui notas específicas do seu deployment]
```

---

**IMPORTANTE:** Não pule etapas! Cada item é crucial para um deployment bem-sucedido e seguro.
