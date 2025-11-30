// src/App.jsx
import { useState, useEffect } from 'react';
import Login from './components/Login';
import TaskForm from './components/TaskForm';
import KanbanBoard from './components/KanbanBoard';
import UserManager from './components/UserManager';
import TaskDetailsModal from './components/TaskDetailsModal';
import NotificationBell from './components/NotificationBell';

const API_URL = 'http://127.0.0.1:3000';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || null);
  const [currentUser, setCurrentUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [activeTab, setActiveTab] = useState('tasks');
  const [selectedTask, setSelectedTask] = useState(null);
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [notificationRefreshTrigger, setNotificationRefreshTrigger] = useState(0);

  const getAuthHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  });

  const handleLogin = (newToken, user) => {
    setToken(newToken);
    setCurrentUser(user);
    localStorage.setItem('token', newToken);
  };

  const handleLogout = () => {
    setToken(null);
    setCurrentUser(null);
    localStorage.removeItem('token');
  };

  // Função para buscar as tarefas da API
  const fetchTasks = async () => {
    if (!token) return;
    
    try {
      const response = await fetch(`${API_URL}/tasks/`, {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setTasks(data);
      } else if (response.status === 401) {
        handleLogout();
      }
    } catch (error) {
      console.error("Erro ao buscar tarefas:", error);
    }
  };

  // Função para buscar usuários (apenas para admin e gerencial)
  const fetchUsers = async () => {
    if (!token) return;
    
    try {
      const response = await fetch(`${API_URL}/users/`, {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setUsers(data);
      } else if (response.status === 401) {
        handleLogout();
        alert('Sua sessão expirou. Por favor, faça login novamente.');
      }
    } catch (error) {
      console.error("Erro ao buscar usuários:", error);
    }
  };

  // useEffect para buscar as tarefas quando o componente for montado
  useEffect(() => {
    if (token) {
      fetchTasks();
      // Buscar informações do usuário
      fetch(`${API_URL}/users/me/`, {
        headers: getAuthHeaders()
      })
        .then(res => {
          if (res.ok) {
            return res.json();
          } else if (res.status === 401) {
            handleLogout();
            throw new Error('Não autenticado');
          }
          throw new Error('Erro ao buscar usuário');
        })
        .then(user => {
          setCurrentUser(user || { username: 'Usuário', role: 'visualizacao' });
          // Se for admin ou gerencial, buscar lista de usuários
          if (user && ['admin', 'gerencial'].includes(user.role)) {
            fetchUsers();
          }
        })
        .catch(err => console.error('Erro ao buscar usuário:', err));
    }
  }, [token]);

  // Função para adicionar uma nova tarefa
  const handleAddTask = async (taskData) => {
    try {
      const response = await fetch(`${API_URL}/tasks/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });
      if (response.ok) {
        fetchTasks(); // Re-busca as tarefas para atualizar a lista
      }
    } catch (error) {
      console.error("Erro ao adicionar tarefa:", error);
      alert('Erro ao adicionar tarefa');
    }
  };
  
  // Função para atualizar uma tarefa (status, título, etc.)
  const handleUpdateTask = async (updatedTask) => {
    try {
      const response = await fetch(`${API_URL}/tasks/${updatedTask.id}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(updatedTask),
      });
      if (response.ok) {
        fetchTasks();
        // Disparar atualização de notificações após atualizar tarefa
        // Isso garante que notificações sejam atualizadas imediatamente
        setNotificationRefreshTrigger(prev => prev + 1);
      }
    } catch (error) {
      console.error("Erro ao atualizar tarefa:", error);
      alert('Erro ao atualizar tarefa');
    }
  };

  // Função para deletar uma tarefa
  const handleDeleteTask = async (taskId) => {
    if (!confirm('Tem certeza que deseja excluir esta tarefa?')) return;
    try {
      const response = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });
      if (response.ok) {
        fetchTasks();
      }
    } catch (error) {
      console.error("Erro ao deletar tarefa:", error);
      alert('Erro ao deletar tarefa');
    }
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  const canManageUsers = currentUser?.role === 'admin' || currentUser?.role === 'gerencial';
  const canManageTasks = currentUser?.role === 'admin' || currentUser?.role === 'gerencial';
  const canAssignTasks = currentUser?.role === 'admin' || currentUser?.role === 'gerencial';
  const canDeleteUsers = currentUser?.role === 'admin';
  const canCreateUsers = currentUser?.role === 'admin';

  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-blue-600">
              🚀 Gerenciador de Tarefas
            </h1>
            <div className="flex items-center gap-4">
              <NotificationBell 
                token={token} 
                currentUser={currentUser}
                refreshTrigger={notificationRefreshTrigger}
                onTaskClick={(taskId) => {
                  // Buscar a tarefa e abrir o modal
                  const task = tasks.find(t => t.id === taskId);
                  if (task) {
                    setSelectedTask(task);
                    setIsTaskModalOpen(true);
                  } else {
                    // Se a tarefa não estiver na lista, buscar da API
                    fetch(`${API_URL}/tasks/${taskId}`, {
                      headers: getAuthHeaders()
                    })
                      .then(res => res.json())
                      .then(taskData => {
                        setSelectedTask(taskData);
                        setIsTaskModalOpen(true);
                      })
                      .catch(err => {
                        console.error('Erro ao buscar tarefa:', err);
                        alert('Erro ao abrir tarefa. Tente atualizar a página.');
                      });
                  }
                }}
              />
              <span className="text-sm text-gray-600">
                Olá, <strong>{currentUser?.username}</strong> ({currentUser?.role})
              </span>
              <button
                onClick={handleLogout}
                className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 text-sm"
              >
                Sair
              </button>
            </div>
          </div>
          
          {/* Tabs */}
          <div className="mt-4 flex gap-2 border-b">
            <button
              onClick={() => setActiveTab('tasks')}
              className={`px-4 py-2 font-medium ${
                activeTab === 'tasks'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              Tarefas
            </button>
            {canManageUsers && (
              <button
                onClick={() => setActiveTab('users')}
                className={`px-4 py-2 font-medium ${
                  activeTab === 'users'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-800'
                }`}
              >
                Usuários
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'tasks' && (
          <div>
            {canManageTasks && (
              <TaskForm 
                onAddTask={handleAddTask}
                users={users}
                currentUser={currentUser}
                canAssignTasks={canAssignTasks}
              />
            )}
            <KanbanBoard
              tasks={tasks}
              onUpdateTask={handleUpdateTask}
              onDeleteTask={handleDeleteTask}
              onShowTaskDetails={(task) => {
                setSelectedTask(task);
                setIsTaskModalOpen(true);
              }}
              users={users}
              canAssignTasks={canAssignTasks}
              currentUserRole={currentUser?.role || 'visualizacao'}
            />
            <TaskDetailsModal
              task={selectedTask}
              isOpen={isTaskModalOpen}
              onClose={() => {
                setIsTaskModalOpen(false);
                setSelectedTask(null);
              }}
              onUpdateTask={handleUpdateTask}
              onDeleteTask={handleDeleteTask}
              users={users}
              canAssignTasks={canAssignTasks}
              currentUserRole={currentUser?.role || 'visualizacao'}
            />
          </div>
        )}

        {activeTab === 'users' && canManageUsers && (
          <UserManager 
            token={token} 
            currentUser={currentUser}
            canDeleteUsers={canDeleteUsers}
            canCreateUsers={canCreateUsers}
          />
        )}
      </main>
    </div>
  );
}

export default App;