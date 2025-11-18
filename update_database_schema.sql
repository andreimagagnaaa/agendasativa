-- Script SQL para atualizar a estrutura da tabela agendas
-- Execute este script no SQL Editor do seu projeto Supabase

-- 1. Adicionar novos campos opcionais
ALTER TABLE agendas 
  ALTER COLUMN os DROP NOT NULL;

ALTER TABLE agendas 
  ADD COLUMN IF NOT EXISTS gerente TEXT;

ALTER TABLE agendas 
  ADD COLUMN IF NOT EXISTS is_vago BOOLEAN DEFAULT FALSE;

-- 2. Adicionar comentários para documentação
COMMENT ON COLUMN agendas.os IS 'Número da Ordem de Serviço (opcional)';
COMMENT ON COLUMN agendas.gerente IS 'Nome do gerente responsável (opcional)';
COMMENT ON COLUMN agendas.is_vago IS 'Indica se é uma agenda vaga (consultor disponível)';

-- 3. Criar índice para melhor performance
CREATE INDEX IF NOT EXISTS idx_agendas_is_vago ON agendas(is_vago);
CREATE INDEX IF NOT EXISTS idx_agendas_gerente ON agendas(gerente);

-- 4. Atualizar registros existentes para marcar agendas VAGO
UPDATE agendas 
SET is_vago = TRUE 
WHERE UPPER(projeto) = 'VAGO' OR UPPER(projeto) = 'LIVRE';

-- 5. Exibir estatísticas
SELECT 
    COUNT(*) as total_agendas,
    COUNT(CASE WHEN is_vago = TRUE THEN 1 END) as agendas_vagas,
    COUNT(CASE WHEN is_vago = FALSE THEN 1 END) as agendas_ocupadas,
    COUNT(CASE WHEN os IS NOT NULL THEN 1 END) as agendas_com_os,
    COUNT(CASE WHEN gerente IS NOT NULL THEN 1 END) as agendas_com_gerente
FROM agendas;

-- 6. Exibir sample de dados
SELECT 
    consultor,
    projeto,
    os,
    gerente,
    is_vago,
    data_inicio,
    data_fim
FROM agendas
ORDER BY data_inicio DESC
LIMIT 10;
