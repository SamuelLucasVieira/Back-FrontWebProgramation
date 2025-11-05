// src/components/KanbanBoard.jsx
import { useState } from 'react';
import TaskCard from './TaskCard';

const STATUSES = [
  { id: 'pendente', label: 'Pendente', color: 'bg-gray-200' },
  { id: 'em_andamento', label: 'Em Andamento', color: 'bg-blue-200' },
  { id: 'em_revisao', label: 'Em Revisão', color: 'bg-yellow-200' },
  { id: 'concluida', label: 'Concluída', color: 'bg-green-200' }
];

function KanbanBoard({ tasks, onUpdateTask, onDeleteTask, users = [], canAssignTasks = false, currentUserRole = 'visualizacao' }) {
  const [draggedTask, setDraggedTask] = useState(null);

  const handleDragStart = (e, task) => {
    setDraggedTask(task);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e, newStatus) => {
    e.preventDefault();
    if (draggedTask && draggedTask.status !== newStatus) {
      // Verificar se visualizacao pode mover para esse status
      if (currentUserRole === 'visualizacao' && newStatus === 'concluida') {
        alert('Usuários com perfil visualização não podem concluir tarefas');
        setDraggedTask(null);
        return;
      }
      onUpdateTask({ ...draggedTask, status: newStatus });
    }
    setDraggedTask(null);
  };

  const getTasksByStatus = (status) => {
    return tasks.filter(task => task.status === status);
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
      {STATUSES.map((status) => {
        // Visualização não pode dropar na coluna "concluida"
        const canDropHere = !(currentUserRole === 'visualizacao' && status.id === 'concluida');
        return (
        <div
          key={status.id}
          className={`${status.color} rounded-lg p-4 min-h-[400px] ${!canDropHere ? 'opacity-60' : ''}`}
          onDragOver={canDropHere ? handleDragOver : undefined}
          onDrop={canDropHere ? (e) => handleDrop(e, status.id) : undefined}
        >
          <h2 className="text-lg font-bold text-gray-800 mb-4 text-center">
            {status.label}
            <span className="ml-2 text-sm font-normal bg-white px-2 py-1 rounded-full">
              {getTasksByStatus(status.id).length}
            </span>
          </h2>
          <div className="space-y-3">
            {getTasksByStatus(status.id).map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onDragStart={handleDragStart}
                onUpdateTask={onUpdateTask}
                onDeleteTask={onDeleteTask}
                users={users}
                canAssignTasks={canAssignTasks}
                currentUserRole={currentUserRole}
              />
            ))}
            {getTasksByStatus(status.id).length === 0 && (
              <p className="text-gray-500 text-sm text-center py-4">
                Nenhuma tarefa
              </p>
            )}
          </div>
        </div>
        );
      })}
    </div>
  );
}

export default KanbanBoard;
