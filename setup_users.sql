-- Script SQL para criar a tabela de usuários no Supabase

-- Criar tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id BIGSERIAL PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    nome TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('ADM', 'CL_MV', 'CONSULTOR')),
    consultor_vinculado TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Adicionar comentários
COMMENT ON TABLE usuarios IS 'Tabela para armazenar usuários do sistema';
COMMENT ON COLUMN usuarios.tipo_usuario IS 'Tipo de usuário: ADM, CL_MV ou CONSULTOR';
COMMENT ON COLUMN usuarios.consultor_vinculado IS 'Nome do consultor vinculado (apenas para tipo CONSULTOR)';

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_ativo ON usuarios(ativo);

-- Trigger para updated_at
DROP TRIGGER IF EXISTS update_usuarios_updated_at ON usuarios;
CREATE TRIGGER update_usuarios_updated_at 
    BEFORE UPDATE ON usuarios 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Inserir usuário admin padrão
-- Senha: admin123
INSERT INTO usuarios (email, senha_hash, nome, tipo_usuario, ativo)
VALUES (
    'admin@ativa.com',
    '$2b$12$kqXpKix4R2VyFOfK3TqKy.B/NUFaG213PjFYN3nvs9T.f7PJMn5dG',
    'Administrador',
    'ADM',
    TRUE
) ON CONFLICT (email) DO NOTHING;

-- Habilitar RLS
ALTER TABLE usuarios ENABLE ROW LEVEL SECURITY;

-- Políticas de segurança (ajuste conforme necessário)
CREATE POLICY "Permitir leitura para usuários autenticados"
ON usuarios FOR SELECT
USING (true); -- Em produção, restringir para o próprio usuário ou admins

CREATE POLICY "Permitir modificação apenas para admins"
ON usuarios FOR ALL
USING (true) -- Em produção, verificar se o usuário logado é admin
WITH CHECK (true);
