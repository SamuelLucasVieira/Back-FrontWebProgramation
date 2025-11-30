"""
Implementação do Padrão Observer para notificações.
Quando uma tarefa muda para status "em_revisao", notifica observadores (admin e gerencial).
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class Observer(ABC):
    """Interface abstrata para observadores."""
    
    @abstractmethod
    def update(self, subject: 'Subject', event_data: Dict[str, Any]) -> None:
        """
        Método chamado quando o subject notifica os observadores.
        
        Args:
            subject: O objeto que está sendo observado
            event_data: Dados do evento (ex: tarefa atualizada)
        """
        pass


class Subject(ABC):
    """Interface abstrata para subjects (objetos observados)."""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        """Adiciona um observador à lista."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        """Remove um observador da lista."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_data: Dict[str, Any]) -> None:
        """Notifica todos os observadores sobre um evento."""
        for observer in self._observers:
            observer.update(self, event_data)


class TaskNotificationObserver(Observer):
    """
    Observador que cria notificações quando uma tarefa muda de status.
    - Quando muda para "em_revisao": notifica admin e gerencial
    - Quando muda para "concluida": notifica o responsável pela tarefa (owner)
    """
    
    def __init__(self, notification_service):
        """
        Inicializa o observador com um serviço de notificações.
        
        Args:
            notification_service: Serviço responsável por criar e armazenar notificações
        """
        self.notification_service = notification_service
    
    def update(self, subject: Subject, event_data: Dict[str, Any]) -> None:
        """
        Cria notificações quando uma tarefa muda de status.
        
        Args:
            subject: O objeto observado (não usado aqui, mas parte da interface)
            event_data: Dicionário contendo:
                - task: dados da tarefa
                - old_status: status anterior (opcional)
                - new_status: novo status
                - updated_by: usuário que fez a atualização (opcional)
        """
        task = event_data.get('task')
        new_status = event_data.get('new_status')
        old_status = event_data.get('old_status')
        
        # Notificar quando muda para "em_revisao" (admin e gerencial)
        if new_status == 'em_revisao' and old_status != 'em_revisao':
            print(f"🔔 Observer detectou mudança para 'em_revisao'. Criando notificações...")
            self.notification_service.create_review_notification(task, event_data.get('updated_by'))
            print(f"✅ Observer concluiu criação de notificações de revisão")
        
        # Notificar quando muda para "concluida" (responsável pela tarefa)
        if new_status == 'concluida' and old_status != 'concluida':
            print(f"🔔 Observer detectou mudança para 'concluida'. Criando notificação para o responsável...")
            self.notification_service.create_completion_notification(task, event_data.get('updated_by'))
            print(f"✅ Observer concluiu criação de notificação de conclusão")


class TaskSubject(Subject):
    """
    Subject que representa uma tarefa.
    Notifica observadores quando a tarefa é atualizada.
    """
    
    def __init__(self, task: Dict[str, Any]):
        """
        Inicializa o subject com uma tarefa.
        
        Args:
            task: Dicionário com dados da tarefa
        """
        super().__init__()
        self.task = task
    
    def update_task(self, updated_task: Dict[str, Any], old_status: str = None, updated_by: Dict[str, Any] = None) -> None:
        """
        Atualiza a tarefa e notifica observadores se necessário.
        
        Args:
            updated_task: Dados atualizados da tarefa
            old_status: Status anterior da tarefa
            updated_by: Usuário que fez a atualização
        """
        new_status = updated_task.get('status')
        
        # Atualizar a tarefa
        self.task = updated_task
        
        # Notificar observadores sobre a mudança
        event_data = {
            'task': self.task,
            'old_status': old_status or self.task.get('status'),
            'new_status': new_status,
            'updated_by': updated_by
        }
        
        self.notify(event_data)

