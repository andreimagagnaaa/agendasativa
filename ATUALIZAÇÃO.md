# 📋 Guia de Atualização - Sistema de Agendas Ativa

## 🎯 O que foi ajustado?

### 1. **Campos Opcionais**
- ✅ Campo **OS** agora é opcional
- ✅ Novo campo **Gerente** (opcional)
- ✅ Apenas Consultor e Projeto são obrigatórios

### 2. **Suporte para Agendas VAGO**
- ✅ Sistema reconhece quando projeto = "VAGO" ou "LIVRE"
- ✅ Agendas VAGO indicam que consultor está **DISPONÍVEL**
- ✅ Agendas VAGO não geram conflito com outras agendas
- ✅ IA entende e exibe corretamente agendas vagas

### 3. **IA Melhorada**
- ✅ Entende que "VAGO" = disponível
- ✅ Ignora agendas VAGO ao verificar conflitos
- ✅ Exibe status visual 🟢 para agendas vagas
- ✅ Mostra informações completas (OS e Gerente quando disponíveis)

---

## 🚀 Como Atualizar o Sistema

### **Passo 1: Atualizar Schema do Banco de Dados**

1. Acesse seu **Supabase Dashboard**
2. Vá em **SQL Editor**
3. Copie e execute o script: `update_database_schema.sql`

Este script irá:
- Tornar o campo `os` opcional
- Adicionar campo `gerente` (opcional)
- Adicionar campo `is_vago` (boolean)
- Criar índices para performance
- Atualizar registros existentes

---

### **Passo 2: Limpar Dados Antigos (Opcional)**

Se quiser remover as agendas fake antigas e importar os dados reais:

```powershell
# Executar script de importação
cd "c:\Users\andre\OneDrive\Área de Trabalho\Ativa"
python import_real_data.py
```

O script irá:
1. Perguntar se deseja limpar o banco (digite **s** para sim)
2. Ler o arquivo `GERAL_25052025.txt`
3. Fazer parsing das agendas reais
4. Importar tudo automaticamente

**Dados que serão importados:**
- ✅ Todos os consultores (André, Gracina, Sirlene, Mayara, Miguel, Lucas)
- ✅ Todas as datas e períodos
- ✅ Projetos reais
- ✅ Identificação automática de agendas VAGO
- ✅ Extração de gerentes quando informado

---

### **Passo 3: Reiniciar a Aplicação**

```powershell
# Parar o servidor atual (Ctrl+C no terminal)
# Depois executar novamente
cd "c:\Users\andre\OneDrive\Área de Trabalho\Ativa"
python -m streamlit run app.py
```

---

## 📊 Como Usar o Novo Sistema

### **Criar Agenda Normal**
```
Consultor: André
Projeto: CRUZ AZUL
OS: (opcional)
Gerente: ROSE (opcional)
Data Início: 14/04/2025
Data Fim: 18/04/2025
```

### **Criar Agenda Vaga (Consultor Disponível)**
```
Consultor: André
Projeto: VAGO
OS: (deixar vazio)
Gerente: (deixar vazio)
Data Início: 17/02/2025
Data Fim: 21/02/2025
```

---

## 🤖 Exemplos de Perguntas para a IA

### Consultar Disponibilidade
- ✅ "André está livre dia 20/02?"
- ✅ "Sirlene pode semana de 10/02?"
- ✅ "Quem está disponível em março?"

### Consultar Agendas
- ✅ "Mostre agendas do André em fevereiro"
- ✅ "Quais projetos da Gracina?"
- ✅ "Agendas da ROSE" (busca por gerente)

### Ver Agendas Vagas
- ✅ "Mostre agendas vagas"
- ✅ "Quem está livre em março?"
- ✅ "André tem agenda vaga?"

---

## ✅ Verificações Pós-Atualização

Execute estas verificações para confirmar que está tudo funcionando:

### 1. **Testar Criação de Agenda sem OS**
- Criar uma agenda sem preencher OS
- Deve permitir salvar normalmente

### 2. **Testar Agenda VAGO**
- Criar uma agenda com projeto "VAGO"
- Sistema deve marcar `is_vago = true`
- Não deve gerar conflito com outras agendas

### 3. **Testar Consulta com IA**
```
Pergunta: "André está livre dia 20/02?"
Resposta esperada: Deve verificar apenas agendas não-VAGO
```

### 4. **Verificar Dados no Banco**
```sql
-- No Supabase SQL Editor
SELECT 
    consultor,
    projeto,
    is_vago,
    os,
    gerente,
    data_inicio,
    data_fim
FROM agendas
WHERE is_vago = TRUE
LIMIT 10;
```

---

## 🐛 Solução de Problemas

### Erro: "column 'os' cannot be null"
**Solução:** Execute o script `update_database_schema.sql` no Supabase

### Erro: "column 'is_vago' does not exist"
**Solução:** Execute o script `update_database_schema.sql` no Supabase

### Agendas VAGO aparecem como conflito
**Solução:** Certifique-se que o código foi atualizado e reinicie o Streamlit

### Script de importação não encontra arquivo
**Solução:** Verifique o caminho em `import_real_data.py` linha 220

---

## 📝 Resumo das Alterações nos Arquivos

### `database.py`
- ✅ Método `create_agenda()` com parâmetros opcionais
- ✅ Detecta automaticamente agendas VAGO
- ✅ Ignora agendas VAGO em verificação de conflitos

### `app.py`
- ✅ Formulário com campo Gerente opcional
- ✅ Campo OS marcado como opcional
- ✅ Validação ajustada (apenas Consultor e Projeto obrigatórios)

### `ai_assistant.py`
- ✅ IA reconhece e exibe agendas VAGO
- ✅ Ignora agendas VAGO ao verificar disponibilidade
- ✅ Exibe informações completas com campos opcionais

### Novos Arquivos
- ✅ `import_real_data.py` - Script de importação
- ✅ `update_database_schema.sql` - Atualização do schema
- ✅ `ATUALIZAÇÃO.md` - Este guia

---

## 📞 Suporte

Se tiver dúvidas ou problemas:
1. Verifique os logs do terminal do Streamlit
2. Verifique logs no Supabase Dashboard
3. Execute os scripts de verificação acima

**Última atualização:** 17/11/2025
