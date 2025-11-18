-- Script SQL para adicionar sistema de autenticação e permissões
-- Execute este script no SQL Editor do Supabase

-- 1. Criar tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id BIGSERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    nome TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('CONSULTOR', 'CL_MV', 'ADM')),
    consultor_vinculado TEXT, -- Nome do consultor se tipo_usuario = 'CONSULTOR'
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Adicionar comentários
COMMENT ON TABLE usuarios IS 'Tabela de usuários do sistema';
COMMENT ON COLUMN usuarios.tipo_usuario IS 'Tipo de usuário: CONSULTOR (acesso própria agenda), CL_MV (acesso visualização MV), ADM (acesso completo)';
COMMENT ON COLUMN usuarios.consultor_vinculado IS 'Nome do consultor vinculado (apenas para tipo CONSULTOR)';

-- 3. Criar índices
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_tipo ON usuarios(tipo_usuario);
CREATE INDEX IF NOT EXISTS idx_usuarios_ativo ON usuarios(ativo);

-- 4. Criar trigger para updated_at
CREATE OR REPLACE FUNCTION update_usuarios_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_usuarios_timestamp ON usuarios;
CREATE TRIGGER update_usuarios_timestamp 
    BEFORE UPDATE ON usuarios 
    FOR EACH ROW 
    EXECUTE FUNCTION update_usuarios_updated_at();

-- 5. Criar usuário admin padrão (senha: admin123)
-- Hash bcrypt de 'admin123' gerado corretamente
INSERT INTO usuarios (email, senha_hash, nome, tipo_usuario, ativo)
VALUES (
    'admin@ativa.com',
    '$2b$12$JQqSGem5p4olI2c3OAzrdOtYZzorBKVjViFxx6Hfmuvp5ZNPNt5Pq',
    'Administrador',
    'ADM',
    TRUE
)
ON CONFLICT (email) DO UPDATE SET
    senha_hash = '$2b$12$JQqSGem5p4olI2c3OAzrdOtYZzorBKVjViFxx6Hfmuvp5ZNPNt5Pq',
    nome = 'Administrador',
    tipo_usuario = 'ADM',
    ativo = TRUE;

-- 6. Criar tabela de logs de acesso
CREATE TABLE IF NOT EXISTS logs_acesso (
    id BIGSERIAL PRIMARY KEY,
    usuario_id BIGINT REFERENCES usuarios(id),
    acao TEXT NOT NULL,
    detalhes JSONB,
    ip_address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_logs_usuario ON logs_acesso(usuario_id);
CREATE INDEX IF NOT EXISTS idx_logs_created_at ON logs_acesso(created_at DESC);

-- 7. Exibir usuários criados
SELECT id, email, nome, tipo_usuario, ativo, created_at
FROM usuarios
ORDER BY created_at DESC;

-- 8. Adicionar campos de detalhes nas agendas
ALTER TABLE agendas 
  ADD COLUMN IF NOT EXISTS horas_cliente DECIMAL(5,2),
  ADD COLUMN IF NOT EXISTS descricao_entrega TEXT;

-- 9. Adicionar comentários
COMMENT ON COLUMN agendas.horas_cliente IS 'Quantidade de horas trabalhadas no cliente';
COMMENT ON COLUMN agendas.descricao_entrega IS 'Descrição da entrega realizada';

-- 10. Exibir estrutura final da tabela agendas
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'agendas'
ORDER BY ordinal_position;
