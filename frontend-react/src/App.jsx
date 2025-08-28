// src/App.jsx
import { useState, useEffect } from 'react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';

const API_URL = 'http://127.0.0.1:3000/tarefas';

function App() {
  const [tasks, setTasks] = useState([]);

  // Função para buscar as tarefas da API
  const fetchTasks = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error("Erro ao buscar tarefas:", error);
    }
  };

  // useEffect para buscar as tarefas quando o componente for montado
  useEffect(() => {
    fetchTasks();
  }, []);

  // Função para adicionar uma nova tarefa
  const handleAddTask = async (taskData) => {
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taskData),
      });
      if (response.ok) {
        fetchTasks(); // Re-busca as tarefas para atualizar a lista
      }
    } catch (error) {
      console.error("Erro ao adicionar tarefa:", error);
    }
  };
  
  // Função para atualizar uma tarefa (status, título, etc.)
  const handleUpdateTask = async (updatedTask) => {
    try {
      const response = await fetch(`${API_URL}/${updatedTask.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedTask),
      });
      if (response.ok) {
        fetchTasks();
      }
    } catch (error) {
      console.error("Erro ao atualizar tarefa:", error);
    }
  };

  // Função para deletar uma tarefa
  const handleDeleteTask = async (taskId) => {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return;
    try {
      const response = await fetch(`${API_URL}/${taskId}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        fetchTasks();
      }
    } catch (error) {
      console.error("Erro ao deletar tarefa:", error);
    }
  };

  return (
    <div className="bg-gray-100 min-h-screen font-sans p-4 sm:p-8">
      <div className="max-w-3xl mx-auto bg-white p-6 sm:p-8 rounded-xl shadow-lg">
        <h1 className="text-3xl sm:text-4xl font-bold text-center text-blue-600 mb-6">
          🚀 Minha Lista de Tarefas
        </h1>
        
        <TaskForm onAddTask={handleAddTask} />
        
        <TaskList 
          tasks={tasks} 
          onUpdateTask={handleUpdateTask} 
          onDeleteTask={handleDeleteTask} 
        />
      </div>
    </div>
  );
}

export default App;