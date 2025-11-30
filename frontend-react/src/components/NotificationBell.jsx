// src/components/NotificationBell.jsx
import { useState, useEffect } from 'react';

const API_URL = 'http://127.0.0.1:3000';

function NotificationBell({ token, currentUser, refreshTrigger = 0, onTaskClick = null }) {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const getAuthHeaders = () => ({
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  });

  const fetchNotifications = async () => {
    if (!token) return; // Agora todos os usuários podem receber notificações
    
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/notifications/`, {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (error) {
      console.error('Erro ao buscar notificações:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchUnreadCount = async () => {
    if (!token) return; // Agora todos os usuários podem receber notificações
    
    try {
      const response = await fetch(`${API_URL}/notifications/unread-count`, {
        headers: getAuthHeaders()
      });
      if (response.ok) {
        const data = await response.json();
        setUnreadCount(data.unread_count || 0);
      }
    } catch (error) {
      console.error('Erro ao buscar contador de notificações:', error);
    }
  };

  const markAsRead = async (notificationId) => {
    try {
      const response = await fetch(`${API_URL}/notifications/${notificationId}/read`, {
        method: 'PUT',
        headers: getAuthHeaders()
      });
      if (response.ok) {
        // Atualizar notificação local
        setNotifications(notifications.map(notif => 
          notif.id === notificationId ? { ...notif, read: true } : notif
        ));
        setUnreadCount(Math.max(0, unreadCount - 1));
      }
    } catch (error) {
      console.error('Erro ao marcar notificação como lida:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      const response = await fetch(`${API_URL}/notifications/read-all`, {
        method: 'PUT',
        headers: getAuthHeaders()
      });
      if (response.ok) {
        setNotifications(notifications.map(notif => ({ ...notif, read: true })));
        setUnreadCount(0);
      }
    } catch (error) {
      console.error('Erro ao marcar todas como lidas:', error);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      if (diffMins < 1) return 'Agora';
      if (diffMins < 60) return `${diffMins} min atrás`;
      if (diffHours < 24) return `${diffHours}h atrás`;
      if (diffDays < 7) return `${diffDays}d atrás`;
      
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

  // Atualizar quando refreshTrigger mudar (quando tarefa é atualizada)
  useEffect(() => {
    if (token && refreshTrigger > 0) {
      // Pequeno delay para garantir que o backend processou a notificação
      const timeout = setTimeout(() => {
        fetchNotifications();
        fetchUnreadCount();
      }, 1500);
      
      return () => clearTimeout(timeout);
    }
  }, [refreshTrigger, token]);
  
  // Atualização periódica e inicial
  useEffect(() => {
    if (token) {
      // Buscar imediatamente ao montar
      fetchNotifications();
      fetchUnreadCount();
      
      // Atualizar a cada 5 segundos (mais frequente para notificações em tempo real)
      const interval = setInterval(() => {
        fetchNotifications();
        fetchUnreadCount();
      }, 5000);
      
      return () => clearInterval(interval);
    }
  }, [token, currentUser]);

  return (
    <div className="relative">
      <button
        onClick={() => {
          setIsOpen(!isOpen);
          if (!isOpen) {
            fetchNotifications();
          }
        }}
        className="relative p-2 text-gray-600 hover:text-gray-800 focus:outline-none transition-colors"
        title={`${unreadCount > 0 ? `${unreadCount} notificação${unreadCount > 1 ? 'ões' : ''} não lida${unreadCount > 1 ? 's' : ''}` : 'Notificações'}`}
      >
        <svg
          className="w-6 h-6"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          />
        </svg>
        {unreadCount > 0 && (
          <span className="absolute top-0 right-0 min-w-[20px] h-5 px-1.5 rounded-full bg-red-600 text-white text-xs font-bold flex items-center justify-center border-2 border-white shadow-lg animate-pulse">
            {unreadCount > 99 ? '99+' : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <>
          {/* Overlay para fechar ao clicar fora */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Painel de notificações */}
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-xl z-50 border border-gray-200 max-h-96 overflow-hidden flex flex-col">
            {/* Header */}
            <div className="bg-blue-600 text-white p-4 flex justify-between items-center">
              <h3 className="font-semibold">Notificações</h3>
              {unreadCount > 0 && (
                <button
                  onClick={markAllAsRead}
                  className="text-xs hover:underline"
                >
                  Marcar todas como lidas
                </button>
              )}
            </div>

            {/* Lista de notificações */}
            <div className="overflow-y-auto flex-1">
              {isLoading ? (
                <div className="p-4 text-center text-gray-500">
                  Carregando...
                </div>
              ) : notifications.length === 0 ? (
                <div className="p-4 text-center text-gray-500">
                  Nenhuma notificação
                </div>
              ) : (
                <div className="divide-y divide-gray-200">
                  {notifications.map((notification) => (
                    <div
                      key={notification.id}
                      className={`p-4 hover:bg-gray-50 cursor-pointer transition-colors ${
                        !notification.read ? 'bg-blue-50' : ''
                      }`}
                      onClick={() => {
                        // Marcar como lida se não estiver lida
                        if (!notification.read) {
                          markAsRead(notification.id);
                        }
                        // Abrir modal da tarefa se tiver task_id e função de callback
                        if (notification.task_id && onTaskClick) {
                          setIsOpen(false); // Fechar painel de notificações
                          onTaskClick(notification.task_id);
                        }
                      }}
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <p className="text-sm font-semibold text-gray-800">
                            {notification.title}
                          </p>
                          <p className="text-xs text-gray-600 mt-1">
                            {notification.message}
                          </p>
                          {notification.task_title && (
                            <p className="text-xs text-blue-600 mt-1 font-medium">
                              📋 Tarefa: {notification.task_title}
                            </p>
                          )}
                          {notification.task_id && (
                            <p className="text-xs text-gray-400 mt-1 italic">
                              Clique para ver detalhes
                            </p>
                          )}
                          <p className="text-xs text-gray-400 mt-2">
                            {formatDate(notification.created_at)}
                          </p>
                        </div>
                        {!notification.read && (
                          <span className="ml-2 h-2 w-2 bg-blue-600 rounded-full flex-shrink-0 mt-1" />
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default NotificationBell;

