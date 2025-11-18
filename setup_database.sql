-- Script SQL para criar a tabela de agendas no Supabase
-- Execute este script no SQL Editor do seu projeto Supabase

-- Criar tabela principal
CREATE TABLE IF NOT EXISTS agendas (
    id BIGSERIAL PRIMARY KEY,
    consultor TEXT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    projeto TEXT NOT NULL,
    os TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Adicionar comentários para documentação
COMMENT ON TABLE agendas IS 'Tabela para armazenar agendas de consultores';
COMMENT ON COLUMN agendas.id IS 'Identificador único da agenda';
COMMENT ON COLUMN agendas.consultor IS 'Nome completo do consultor';
COMMENT ON COLUMN agendas.data_inicio IS 'Data de início da alocação';
COMMENT ON COLUMN agendas.data_fim IS 'Data de término da alocação';
COMMENT ON COLUMN agendas.projeto IS 'Nome do projeto';
COMMENT ON COLUMN agendas.os IS 'Número da Ordem de Serviço';
COMMENT ON COLUMN agendas.created_at IS 'Data e hora de criação do registro';
COMMENT ON COLUMN agendas.updated_at IS 'Data e hora da última atualização';

-- Criar índices para melhor performance
CREATE INDEX IF NOT EXISTS idx_agendas_consultor ON agendas(consultor);
CREATE INDEX IF NOT EXISTS idx_agendas_datas ON agendas(data_inicio, data_fim);
CREATE INDEX IF NOT EXISTS idx_agendas_projeto ON agendas(projeto);
CREATE INDEX IF NOT EXISTS idx_agendas_os ON agendas(os);
CREATE INDEX IF NOT EXISTS idx_agendas_created_at ON agendas(created_at DESC);

-- Criar trigger para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

DROP TRIGGER IF EXISTS update_agendas_updated_at ON agendas;

CREATE TRIGGER update_agendas_updated_at 
    BEFORE UPDATE ON agendas 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Adicionar constraint para garantir que data_fim >= data_inicio
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'check_datas'
    ) THEN
        ALTER TABLE agendas 
        ADD CONSTRAINT check_datas 
        CHECK (data_fim >= data_inicio);
    END IF;
END $$;

-- Inserir dados de exemplo (opcional - remova se não quiser dados de teste)
INSERT INTO agendas (consultor, data_inicio, data_fim, projeto, os) 
SELECT * FROM (VALUES
    ('João Silva', '2025-01-15'::DATE, '2025-01-31'::DATE, 'Projeto Alpha', '12345'),
    ('Maria Santos', '2025-02-01'::DATE, '2025-02-28'::DATE, 'Projeto Beta', '12346'),
    ('Pedro Oliveira', '2025-01-20'::DATE, '2025-02-10'::DATE, 'Projeto Gamma', '12347'),
    ('Ana Costa', '2025-03-01'::DATE, '2025-03-15'::DATE, 'Projeto Delta', '12348')
) AS dados(consultor, data_inicio, data_fim, projeto, os)
WHERE NOT EXISTS (
    SELECT 1 FROM agendas WHERE consultor = dados.consultor AND projeto = dados.projeto
);

-- Verificar se os dados foram inseridos
SELECT * FROM agendas ORDER BY data_inicio;

-- Habilitar Row Level Security (RLS) - IMPORTANTE para segurança
ALTER TABLE agendas ENABLE ROW LEVEL SECURITY;

-- Remover políticas existentes antes de criar novas
DROP POLICY IF EXISTS "Permitir leitura para todos" ON agendas;
DROP POLICY IF EXISTS "Permitir inserção para todos" ON agendas;
DROP POLICY IF EXISTS "Permitir atualização para todos" ON agendas;
DROP POLICY IF EXISTS "Permitir exclusão para todos" ON agendas;

-- Criar política para permitir leitura pública (ajuste conforme necessário)
CREATE POLICY "Permitir leitura para todos"
ON agendas FOR SELECT
USING (true);

-- Criar política para permitir inserção (ajuste conforme necessário)
CREATE POLICY "Permitir inserção para todos"
ON agendas FOR INSERT
WITH CHECK (true);

-- Criar política para permitir atualização (ajuste conforme necessário)
CREATE POLICY "Permitir atualização para todos"
ON agendas FOR UPDATE
USING (true)
WITH CHECK (true);

-- Criar política para permitir exclusão (ajuste conforme necessário)
CREATE POLICY "Permitir exclusão para todos"
ON agendas FOR DELETE
USING (true);

-- Nota: As políticas acima permitem acesso total. Em produção, você deve
-- ajustá-las para incluir autenticação e autorização apropriadas.
-- Por exemplo, usando auth.uid() para restringir acesso apenas a usuários autenticados.

-- Exemplo de política mais restrita (comentado):
-- CREATE POLICY "Usuários autenticados podem ler"
-- ON agendas FOR SELECT
-- USING (auth.role() = 'authenticated');
