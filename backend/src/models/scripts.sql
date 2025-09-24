-- Apaga as tabelas se elas já existirem para permitir que o script seja executado novamente.
-- A cláusula CASCADE remove objetos dependentes (como sequências)
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS tarefas CASCADE;

-- Tabela para armazenar os usuários
CREATE TABLE usuarios (
    id_user SERIAL PRIMARY KEY,                -- SERIAL é o tipo do PostgreSQL para um inteiro que se auto-incrementa.
    username TEXT UNIQUE NOT NULL,        -- Nome de usuário, deve ser único. TEXT é um tipo apropriado.
    hashed_password TEXT NOT NULL,        -- Senha já criptografada (hash).
    role TEXT NOT NULL CHECK(role IN ('admin', 'viewer')) -- Papel do usuário (apenas 'admin' ou 'viewer').
);

-- Tabela para armazenar as tarefas
CREATE TABLE tarefas (
    id_task SERIAL PRIMARY KEY,               -- Usando SERIAL também para as tarefas, o que é uma prática comum.
    titulo TEXT NOT NULL,                 -- Título da tarefa.
    descricao TEXT,                       -- Descrição opcional.
    status TEXT NOT NULL CHECK(status IN ('pendente', 'concluída')) -- Status da tarefa.
);
