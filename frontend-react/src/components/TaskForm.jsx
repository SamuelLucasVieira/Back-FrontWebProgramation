// src/components/TaskForm.jsx
import { useState } from 'react';

function TaskForm({ onAddTask }) {
  const [titulo, setTitulo] = useState('');
  const [descricao, setDescricao] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!titulo.trim()) return;

    const newTask = {
      id: Date.now(),
      titulo,
      descricao,
      status: 'pendente',
    };
    onAddTask(newTask);
    setTitulo('');
    setDescricao('');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-8 p-4 bg-gray-50 border border-gray-200 rounded-lg">
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