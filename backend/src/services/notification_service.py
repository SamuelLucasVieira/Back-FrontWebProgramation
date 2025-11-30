"""
Serviço de Notificações - Service Layer Pattern
Gerencia notificações do sistema usando o padrão Observer.
Usa padrão Singleton para garantir que todas as instâncias compartilhem as mesmas notificações.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from src.repositories.user_repository import UserRepository


class NotificationService:
    """
    Serviço singleton para gerenciar notificações.
    Todas as instâncias compartilham o mesmo armazenamento de notificações.
    """
    _instance = None
    _notifications: List[Dict[str, Any]] = []
    
    def __new__(cls, user_repository: Optional[UserRepository] = None):
        """
        Implementa padrão Singleton para garantir que todas as instâncias
        compartilhem o mesmo armazenamento de notificações.
        """
        if cls._instance is None:
            cls._instance = super(NotificationService, cls).__new__(cls)
            cls._instance._notifications = []
        return cls._instance
    
    def __init__(self, user_repository: Optional[UserRepository] = None):
        """
        Inicializa o serviço de notificações.
        
        Args:
            user_repository: Repositório de usuários para buscar admins e gerenciais
        """
        # Se já foi inicializado (singleton), não reinicializar
        if hasattr(self, '_initialized'):
            return
        
        self.user_repository = user_repository or UserRepository()
        # Usar a lista compartilhada da classe (singleton)
        if not hasattr(self, '_notifications'):
            self._notifications = NotificationService._notifications
        self._initialized = True
    
    def create_review_notification(self, task: Dict[str, Any], updated_by: Optional[Dict[str, Any]] = None) -> None:
        """
        Cria notificações para admin e gerencial quando uma tarefa vai para revisão.
        
        Args:
            task: Dados da tarefa que foi movida para revisão
            updated_by: Usuário que fez a atualização (opcional)
        """
        # Buscar todos os usuários admin e gerencial
        all_users = self.user_repository.find_all()
        target_users = [
            user for user in all_users 
            if user.get('role') in ['admin', 'gerencial']
        ]
        
        # Criar notificação para cada usuário alvo
        print(f"📢 Criando notificações para {len(target_users)} usuários (admin/gerencial)")
        for user in target_users:
            # Usar o ID baseado no tamanho atual da lista compartilhada
            notification_id = len(NotificationService._notifications) + 1
            notification = {
                'id': notification_id,
                'user_id': user.get('id'),
                'type': 'task_review',
                'title': 'Tarefa em Revisão',
                'message': f"A tarefa '{task.get('titulo', 'Sem título')}' foi movida para revisão.",
                'task_id': task.get('id'),
                'task_title': task.get('titulo'),
                'created_at': datetime.now().isoformat(),
                'read': False,
                'updated_by': updated_by.get('username') if updated_by and isinstance(updated_by, dict) else (updated_by.username if hasattr(updated_by, 'username') else None)
            }
            NotificationService._notifications.append(notification)
            print(f"✅ Notificação criada para usuário {user.get('id')} ({user.get('username')}): {notification['message']}")
    
    def create_completion_notification(self, task: Dict[str, Any], updated_by: Optional[Dict[str, Any]] = None) -> None:
        """
        Cria notificação para o responsável pela tarefa quando ela é concluída.
        
        Args:
            task: Dados da tarefa que foi concluída
            updated_by: Usuário que fez a atualização (opcional)
        """
        owner_id = task.get('owner_id')
        if not owner_id:
            print(f"⚠️  Tarefa {task.get('id')} não tem owner_id, não é possível notificar")
            return
        
        # Buscar o usuário responsável pela tarefa
        owner = self.user_repository.find_by_id(owner_id)
        if not owner:
            print(f"⚠️  Usuário {owner_id} não encontrado, não é possível notificar")
            return
        
        # Criar notificação para o responsável
        notification_id = len(NotificationService._notifications) + 1
        notification = {
            'id': notification_id,
            'user_id': owner_id,
            'type': 'task_completed',
            'title': 'Tarefa Concluída',
            'message': f"Sua tarefa '{task.get('titulo', 'Sem título')}' foi concluída.",
            'task_id': task.get('id'),
            'task_title': task.get('titulo'),
            'created_at': datetime.now().isoformat(),
            'read': False,
            'updated_by': updated_by.get('username') if updated_by and isinstance(updated_by, dict) else (updated_by.username if hasattr(updated_by, 'username') else None)
        }
        NotificationService._notifications.append(notification)
        print(f"✅ Notificação de conclusão criada para usuário {owner_id} ({owner.get('username')}): {notification['message']}")
    
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> List[Dict[str, Any]]:
        """
        Busca notificações de um usuário específico.
        
        Args:
            user_id: ID do usuário
            unread_only: Se True, retorna apenas notificações não lidas
        
        Returns:
            Lista de notificações do usuário
        """
        notifications = [
            notif for notif in NotificationService._notifications 
            if notif.get('user_id') == user_id
        ]
        
        if unread_only:
            notifications = [notif for notif in notifications if not notif.get('read')]
        
        # Ordenar por data de criação (mais recentes primeiro)
        notifications.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return notifications
    
    def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        """
        Marca uma notificação como lida.
        
        Args:
            notification_id: ID da notificação
            user_id: ID do usuário (para segurança)
        
        Returns:
            True se a notificação foi marcada como lida, False caso contrário
        """
        for notification in NotificationService._notifications:
            if notification.get('id') == notification_id and notification.get('user_id') == user_id:
                notification['read'] = True
                return True
        return False
    
    def mark_all_as_read(self, user_id: int) -> int:
        """
        Marca todas as notificações de um usuário como lidas.
        
        Args:
            user_id: ID do usuário
        
        Returns:
            Número de notificações marcadas como lidas
        """
        count = 0
        for notification in NotificationService._notifications:
            if notification.get('user_id') == user_id and not notification.get('read'):
                notification['read'] = True
                count += 1
        return count
    
    def get_unread_count(self, user_id: int) -> int:
        """
        Retorna o número de notificações não lidas de um usuário.
        
        Args:
            user_id: ID do usuário
        
        Returns:
            Número de notificações não lidas
        """
        return len(self.get_user_notifications(user_id, unread_only=True))

