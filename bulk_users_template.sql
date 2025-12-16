-- Template para criação de usuários em massa
-- Senha padrão para todos: ativa123
-- Hash: $2b$12$7TpxxGWA4TRJ1IHbizQmgOlcqvEdHQP6jSzoXMm7VyKoiShJUHbIG

-- Consultores (Exemplos - Substitua pelos reais)
INSERT INTO usuarios (email, senha_hash, nome, tipo_usuario, consultor_vinculado) VALUES
('joao.silva@ativa.com', '$2b$12$7TpxxGWA4TRJ1IHbizQmgOlcqvEdHQP6jSzoXMm7VyKoiShJUHbIG', 'João Silva', 'CONSULTOR', 'João Silva'),
('maria.santos@ativa.com', '$2b$12$7TpxxGWA4TRJ1IHbizQmgOlcqvEdHQP6jSzoXMm7VyKoiShJUHbIG', 'Maria Santos', 'CONSULTOR', 'Maria Santos');

-- Clientes / Visualização (Exemplos)
INSERT INTO usuarios (email, senha_hash, nome, tipo_usuario) VALUES
('cliente.mv@hospital.com', '$2b$12$7TpxxGWA4TRJ1IHbizQmgOlcqvEdHQP6jSzoXMm7VyKoiShJUHbIG', 'Gestor MV', 'CL_MV');

-- Admins adicionais
INSERT INTO usuarios (email, senha_hash, nome, tipo_usuario) VALUES
('gerente@ativa.com', '$2b$12$7TpxxGWA4TRJ1IHbizQmgOlcqvEdHQP6jSzoXMm7VyKoiShJUHbIG', 'Gerente de Projetos', 'ADM');
