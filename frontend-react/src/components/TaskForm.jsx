// src/components/TaskForm.jsx
import { useState } from 'react';

function TaskForm({ onAddTask, users = [], currentUser, canAssignTasks = false }) {
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');
  const [ownerId, setOwnerId] = useState(currentUser?.id || '');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!titulo.trim()) return;

    const newTask = {
      titulo,
      descricao,
      status: 'pendente'
    };
    
    // Se pode atribuir tarefas, incluir owner_id (se selecionado, senão será o usuário atual no backend)
    if (canAssignTasks) {
      if (ownerId) {
        newTask.owner_id = parseInt(ownerId);
      }
      // Se não selecionou ninguém, o backend usará o current_user.id automaticamente
    }
    onAddTask(newTask);
    setTitulo('');
    setDescricao('');
    setOwnerId(currentUser?.id || '');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8 p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex flex-col flex-grow gap-4">
          <input
            type="text"
            placeholder="Título da tarefa"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <input
            type="text"
            placeholder="Descrição (opcional)"
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {canAssignTasks && users.length > 0 && (
            <select
              value={ownerId}
              onChange={(e) => setOwnerId(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Selecione o responsável (padrão: você)</option>
              {users.map(user => (
                <option key={user.id} value={user.id}>
                  {user.username} ({user.role})
                </option>
              ))}
            </select>
          )}
        </div>
        <button
          type="submit"
          className="bg-blue-600 text-white font-semibold px-6 py-2 rounded-md hover:bg-blue-700 transition-colors duration-200 self-start sm:self-center"
        >
          Adicionar
        </button>
      </div>
    </form>
  );
}

export default TaskForm;