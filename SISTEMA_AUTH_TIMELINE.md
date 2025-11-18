# 🚀 Sistema de Autenticação e Visualização Timeline MV

## ✅ O que foi implementado?

### 1. **Sistema de Autenticação**
- ✅ Login com email e senha
- ✅ Hash de senhas com bcrypt
- ✅ Sessões de usuário
- ✅ Logs de acesso

### 2. **Níveis de Usuário**

#### 👤 **CONSULTOR**
- ✅ Vê apenas sua própria agenda
- ✅ Pode editar sua própria agenda
- ✅ Vinculado a um consultor específico
- ✅ Acesso restrito ao chat

#### 👁️ **CL_MV (Cliente MV)**
- ✅ Visualização completa em formato Timeline/Calendário (estilo MV)
- ✅ Vê todas as agendas de todos os consultores
- ✅ **NÃO** pode editar agendas
- ✅ Ideal para parceiro MV Sistemas

#### 🔑 **ADM (Administrador)**
- ✅ Acesso completo a todas funcionalidades
- ✅ Gerenciar usuários (criar, desativar)
- ✅ Visualização Timeline MV
- ✅ Dashboard completo
- ✅ Chat com IA

### 3. **Visualização Timeline MV**
- ✅ Calendário em formato tabela (como na imagem)
- ✅ Visualização por consultor e dia
- ✅ Status visual: 🟢 LIVRE | 🔴 OCUPADO
- ✅ Navegação por mês/ano
- ✅ Estatísticas do período

---

## 📋 Passos para Implementar

### **Passo 1: Atualizar Banco de Dados**

Execute o script SQL no Supabase:

```sql
-- No SQL Editor do Supabase, execute:
```

Abra `update_auth_schema.sql` e execute no Supabase Dashboard.

Isso criará:
- Tabela `usuarios` (email, senha, tipo, etc)
- Tabela `logs_acesso` (auditoria)
- Usuário admin padrão

### **Passo 2: Testar o Sistema**

```powershell
cd "c:\Users\andre\OneDrive\Área de Trabalho\Ativa"
python -m streamlit run app.py
```

**Login padrão:**
- Email: `admin@ativa.com`
- Senha: `admin123`

### **Passo 3: Criar Usuários**

Após logar como admin, vá em aba **"Usuários"** e crie:

#### Para MV Sistemas (parceiro):
```
Email: mv@mvsistemas.com
Nome: MV Sistemas
Tipo: CL_MV
Senha: (defina uma senha)
```

#### Para Consultores:
```
Email: andre@ativa.com
Nome: André
Tipo: CONSULTOR
Consultor Vinculado: André
Senha: (defina uma senha)
```

---

## 🎯 Como Usar

### **Para Usuário CL_MV (Visualização MV)**

1. Login com credenciais
2. Visualização Timeline automaticamente aberta
3. Navegue por mês/ano
4. Veja status de todos os consultores
5. 🟢 LIVRE = Disponível | 🔴 OCUPADO = Alocado

### **Para Consultores**

1. Login com credenciais
2. Vê apenas sua própria agenda
3. Timeline compacta dos próximos 60 dias
4. Pode usar chat para consultas

### **Para Administradores**

1. Acesso completo
2. Chat, Dashboard, Timeline MV e Gerenciar Usuários
3. Criar/desativar usuários

---

## 📁 Arquivos Criados

### Backend/Database
- `auth.py` - Sistema de autenticação
- `update_auth_schema.sql` - Script SQL para criar tabelas

### Frontend
- `login_page.py` - Tela de login e menu de usuário
- `timeline_view.py` - Visualização Timeline estilo MV

### Atualizados
- `app.py` - Integração completa com autenticação
- `requirements.txt` - Adicionado bcrypt

---

## 🔐 Segurança

### Senhas
- ✅ Hash com bcrypt (nunca armazenadas em texto plano)
- ✅ Salt aleatório por senha
- ✅ Algoritmo bcrypt resistente a brute-force

### Sessões
- ✅ Gerenciadas pelo Streamlit
- ✅ Dados do usuário em `st.session_state`
- ✅ Logout limpa sessão completamente

### Permissões
- ✅ Verificação por tipo de usuário
- ✅ Restrição de acesso por rota
- ✅ Logs de todas as ações

---

## 📊 Estrutura de Permissões

| Funcionalidade | CONSULTOR | CL_MV | ADM |
|---|---|---|---|
| Ver própria agenda | ✅ | ❌ | ✅ |
| Ver todas agendas | ❌ | ✅ | ✅ |
| Editar agenda | ⚠️ Própria | ❌ | ✅ |
| Visualização Timeline MV | ❌ | ✅ | ✅ |
| Chat IA | ⚠️ Limitado | ❌ | ✅ |
| Dashboard | ❌ | ❌ | ✅ |
| Gerenciar usuários | ❌ | ❌ | ✅ |

---

## 🎨 Visualização Timeline MV

### Características:
- ✅ Formato tabela com consultores nas linhas
- ✅ Dias do mês nas colunas
- ✅ Dia da semana (SEG, TER, QUA, etc)
- ✅ Status visual claro
- ✅ Scroll horizontal para muitos dias
- ✅ Responsivo

### Exemplo de Exibição:
```
Consultor | 01/11 SEG | 02/11 TER | 03/11 QUA | ...
André     | 🟢 LIVRE  | 🔴 PROJ-X | 🔴 PROJ-X | ...
Gracina   | 🔴 PROJ-Y | 🔴 PROJ-Y | 🟢 LIVRE  | ...
Sirlene   | 🟢 LIVRE  | 🟢 LIVRE  | 🔴 PROJ-Z | ...
```

---

## 🔧 Próximas Melhorias Sugeridas

1. **Recuperação de Senha**
   - Email com token de reset
   - Validação por tempo limitado

2. **Perfil de Usuário**
   - Alterar própria senha
   - Foto de perfil
   - Preferências

3. **Auditoria Avançada**
   - Relatório de acessos
   - Histórico de modificações
   - Export de logs

4. **Notificações**
   - Email quando agenda muda
   - Avisos de conflitos
   - Lembretes

5. **API REST**
   - Integração com MV Sistemas
   - Endpoints protegidos
   - Webhooks

---

## 📞 Suporte

**Credenciais padrão do sistema:**
- Email: admin@ativa.com
- Senha: admin123

**Importante:** Altere a senha do admin após primeiro acesso!

---

## ✅ Checklist de Implementação

- [ ] Executar `update_auth_schema.sql` no Supabase
- [ ] Instalar bcrypt (`pip install bcrypt==4.1.2`)
- [ ] Reiniciar aplicação
- [ ] Login com admin@ativa.com / admin123
- [ ] Criar usuário tipo CL_MV para MV Sistemas
- [ ] Criar usuários tipo CONSULTOR
- [ ] Testar permissões de cada tipo
- [ ] Alterar senha do admin
- [ ] Configurar usuários para produção

**Última atualização:** 17/11/2025
