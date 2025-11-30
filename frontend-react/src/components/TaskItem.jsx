// src/components/TaskItem.jsx
import { useState } from 'react';

function TaskItem({ task, onUpdateTask, onDeleteTask }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(task.titulo);
  const [editedDesc, setEditedDesc] = useState(task.descricao);
  
  const handleSave = () => {
    if (!editedTitle.trim()) return;
    onUpdateTask({ ...task, titulo: editedTitle, descricao: editedDesc });
    setIsEditing(false);
  };

  const handleToggleStatus = () => {
    const newStatus = task.status === 'pendente' ? 'concluida' : 'pendente';
    onUpdateTask({ ...task, status: newStatus });
  };
  
  // Visualização de Edição
  if (isEditing) {
    return (
      <li className="p-4 bg-gray-100 border border-blue-300 rounded-lg shadow-sm flex flex-col gap-3">
        <input 
          type="text" 
          value={editedTitle} 
          onChange={(e) => setEditedTitle(e.target.value)} 
          className="w-full px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-semibold"
        />
        <input 
          type="text" 
          value={editedDesc} 
          onChange={(e) => setEditedDesc(e.target.value)}
          className="w-full px-3 py-1 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
        <div className="flex gap-2 justify-end">
          <button onClick={() => setIsEditing(false)} className="px-3 py-1 bg-gray-500 text-white text-xs font-bold rounded-md hover:bg-gray-600">Cancelar</button>
          <button onClick={handleSave} className="px-3 py-1 bg-blue-600 text-white text-xs font-bold rounded-md hover:bg-blue-700">Salvar</button>
        </div>
      </li>
    );
  }

  // Visualização Padrão
  return (
    <li className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div className={`flex-grow ${task.status === 'concluida' ? 'text-gray-400 line-through' : ''}`}>
        <p className="font-bold text-gray-800 break-words">{task.titulo}</p>
        <p className="text-sm text-gray-600 break-words">{task.descricao}</p>
      </div>
      <div className="flex gap-2 flex-shrink-0 self-end sm:self-center">
        <button onClick={handleToggleStatus} className={`px-3 py-1 text-white text-xs font-bold rounded-md ${task.status === 'pendente' ? 'bg-green-500 hover:bg-green-600' : 'bg-gray-500 hover:bg-gray-600'}`}>
          {task.status === 'pendente' ? 'Concluir' : 'Reabrir'}
        </button>
        <button onClick={() => setIsEditing(true)} className="px-3 py-1 bg-yellow-500 text-white text-xs font-bold rounded-md hover:bg-yellow-600">Editar</button>
        <button onClick={() => onDeleteTask(task.id)} className="px-3 py-1 bg-red-500 text-white text-xs font-bold rounded-md hover:bg-red-600">Excluir</button>
      </div>
    </li>
  );
}

export default TaskItem;