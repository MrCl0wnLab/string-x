-- Arquivo de inicialização para criar a estrutura do banco de dados
-- Este script será executado quando o contêiner for iniciado pela primeira vez

-- Usar banco de dados strx_db
USE strx_db;

-- Criar tabela simplificada para armazenar todos os resultados
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    module_type VARCHAR(50) DEFAULT 'unknown',
    processed_at DATETIME,
    source VARCHAR(255),
    metadata TEXT
);

-- Criar índices para melhorar o desempenho das consultas
CREATE INDEX idx_module_type ON results (module_type);
CREATE INDEX idx_processed_at ON results (processed_at);

-- Criar usuário com permissões limitadas para a aplicação
CREATE USER IF NOT EXISTS 'strx_user'@'%' IDENTIFIED BY 'Str1ngX_p4ss!';
GRANT SELECT, INSERT, UPDATE ON strx_db.* TO 'strx_user'@'%';
FLUSH PRIVILEGES;

-- Inserir dados de exemplo para teste
INSERT INTO results (data, processed_at, module_type, source, metadata) 
VALUES ('example@domain.com', NOW(), 'ext:email', 'sample_data', '{"confidence": 0.95}');

INSERT INTO results (data, processed_at, module_type, source, metadata) 
VALUES ('example.com', NOW(), 'ext:domain', 'sample_data', '{"category": "organization"}');

INSERT INTO results (data, processed_at, module_type, source, metadata) 
VALUES ('192.168.1.1', NOW(), 'ext:ip', 'network_scan', '{"location": "internal"}');

INSERT INTO results (data, processed_at, module_type, source, metadata) 
VALUES ('Google search result', NOW(), 'clc:google', 'dork_query', '{"url": "https://example.com", "title": "Example Domain"}');
