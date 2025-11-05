-- Script de migração para adicionar novos status ao kanban
-- Execute este script se você já tem um banco de dados existente

-- Primeiro, atualizar todas as tarefas com status 'concluída' para 'concluida' (sem acento)
UPDATE tarefas SET status = 'concluida' WHERE status = 'concluída';

-- Dropar o tipo antigo e recriar com os novos valores
DROP TYPE IF EXISTS task_status CASCADE;

CREATE TYPE task_status AS ENUM (
    'pendente',
    'em_andamento',
    'em_revisao',
    'concluida'
);

-- Recriar a coluna status na tabela tarefas
ALTER TABLE tarefas 
    ALTER COLUMN status TYPE task_status 
    USING status::text::task_status;

-- Se houver alguma restrição ou índice que precise ser recriado, adicione aqui
