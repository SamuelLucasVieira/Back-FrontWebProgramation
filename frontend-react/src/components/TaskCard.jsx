// src/components/TaskCard.jsx
import { useState, useEffect } from 'react';

function TaskCard({ task, onDragStart, onUpdateTask, onDeleteTask, users = [], canAssignTasks = false, currentUserRole = 'visualizacao' }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(task.titulo);
  const [editedDesc, setEditedDesc] = useState(task.descricao);
  const [editedOwnerId, setEditedOwnerId] = useState(task.owner_id);

  // Atualizar estados quando task mudar
  useEffect(() => {
    setEditedTitle(task.titulo);
    setEditedDesc(task.descricao);
    setEditedOwnerId(task.owner_id);
  }, [task]);

  const handleSave = () => {
    if (!editedTitle.trim()) return;
    const updatedTask = { ...task, titulo: editedTitle, descricao: editedDesc };
    // Se pode atribuir tarefas, sempre incluir owner_id (mesmo que seja o mesmo)
    if (canAssignTasks && editedOwnerId) {
      updatedTask.owner_id = parseInt(editedOwnerId);
    }
    onUpdateTask(updatedTask);
    setIsEditing(false);
  };

  // Verificar se pode arrastar para determinado status
  const canDragToStatus = (status) => {
    if (currentUserRole === 'visualizacao' && status === 'concluida') {
      return false;
    }
    return true;
  };

  const handleStatusChange = (newStatus) => {
    onUpdateTask({ ...task, status: newStatus });
  };

  if (isEditing) {
    return (
      <div className="bg-white p-3 rounded-lg shadow-md border-2 border-blue-400">
        <input
          type="text"
          value={editedTitle}
          onChange={(e) => setEditedTitle(e.target.value)}
          className="w-full px-2 py-1 border border-gray-300 rounded mb-2 text-sm font-semibold"
          placeholder="Título"
        />
        <textarea
          value={editedDesc}
          onChange={(e) => setEditedDesc(e.target.value)}
          className="w-full px-2 py-1 border border-gray-300 rounded mb-2 text-xs"
          placeholder="Descrição"
          rows="3"
        />
        {canAssignTasks && users.length > 0 && (
          <select
            value={editedOwnerId}
            onChange={(e) => setEditedOwnerId(e.target.value)}
            className="w-full px-2 py-1 border border-gray-300 rounded mb-2 text-xs"
          >
            {users.map(user => (
              <option key={user.id} value={user.id}>
                {user.username} ({user.role})
              </option>
            ))}
          </select>
        )}
        <div className="flex gap-2 justify-end">
          <button
            onClick={() => setIsEditing(false)}
            className="px-2 py-1 bg-gray-400 text-white text-xs rounded hover:bg-gray-500"
          >
            Cancelar
          </button>
          <button
            onClick={handleSave}
            className="px-2 py-1 bg-blue-600 text-white text-xs rounded hover:bg-blue-700"
          >
            Salvar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      draggable={true}
      onDragStart={(e) => onDragStart(e, task)}
      className="bg-white p-3 rounded-lg shadow-md cursor-move hover:shadow-lg transition-shadow border border-gray-200"
    >
      <div className="mb-2">
        <p className="font-semibold text-gray-800 text-sm break-words">
          {task.titulo}
        </p>
        {task.descricao && (
          <p className="text-xs text-gray-600 mt-1 break-words">
            {task.descricao}
          </p>
        )}
        {task.owner_username && (
          <p className="text-xs text-gray-500 mt-1">
            👤 {task.owner_username}
          </p>
        )}
      </div>
      
      <div className="flex flex-wrap gap-1 mt-3">
        <select
          value={task.status}
          onChange={(e) => handleStatusChange(e.target.value)}
          className="text-xs px-2 py-1 border border-gray-300 rounded bg-white"
        >
          <option value="pendente">Pendente</option>
          <option value="em_andamento">Em Andamento</option>
          <option value="em_revisao">Em Revisão</option>
          {currentUserRole !== 'visualizacao' && (
            <option value="concluida">Concluída</option>
          )}
        </select>
        {currentUserRole !== 'visualizacao' && (
          <>
            <button
              onClick={() => setIsEditing(true)}
              className="text-xs px-2 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600"
            >
              Editar
            </button>
            <button
              onClick={() => onDeleteTask(task.id)}
              className="text-xs px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600"
            >
              Excluir
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default TaskCard;
