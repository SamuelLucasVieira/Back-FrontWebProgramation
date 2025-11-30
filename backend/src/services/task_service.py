"""
Serviço de Tarefas - Service Layer Pattern
Contém a lógica de negócio relacionada a tarefas.
Usa o padrão Observer para notificar quando tarefas vão para revisão.
"""
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from src.repositories.task_repository import TaskRepository
from src.repositories.user_repository import UserRepository
from src.config import schemas
from src.patterns import TaskSubject, TaskNotificationObserver
from src.services.notification_service import NotificationService


class TaskService:
    """Serviço para gerenciamento de tarefas."""
    
    def __init__(
        self, 
        task_repository: Optional[TaskRepository] = None,
        user_repository: Optional[UserRepository] = None,
        notification_service: Optional[NotificationService] = None
    ):
        """
        Inicializa o serviço com repositórios (Dependency Injection).
        Configura o padrão Observer para notificações.
        """
        self.task_repository = task_repository or TaskRepository()
        self.user_repository = user_repository or UserRepository()
        self.notification_service = notification_service or NotificationService(self.user_repository)
        
        # Configurar Observer Pattern
        # Criar observador de notificações
        self.notification_observer = TaskNotificationObserver(self.notification_service)
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Retorna todas as tarefas."""
        return self.task_repository.find_all()
    
    def get_task_by_id(self, task_id: int) -> Dict[str, Any]:
        """Busca uma tarefa pelo ID. Lança exceção se não encontrada."""
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        return task
    
    def create_task(
        self,
        task_data: schemas.TaskCreate,
        current_user_id: int
    ) -> Dict[str, Any]:
        """
        Cria uma nova tarefa.
        Valida se o owner_id existe (se fornecido).
        """
        # Se owner_id foi fornecido, usar ele; senão, usar o id do usuário atual
        owner_id = task_data.owner_id if task_data.owner_id is not None else current_user_id
        
        # Verificar se o usuário destino existe (se foi fornecido um owner_id diferente)
        if task_data.owner_id is not None and task_data.owner_id != current_user_id:
            target_user = self.user_repository.find_by_id(task_data.owner_id)
            if not target_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuário destino não encontrado"
                )
        
        return self.task_repository.create(
            titulo=task_data.titulo,
            descricao=task_data.descricao,
            status=task_data.status,
            owner_id=owner_id
        )
    
    def update_task(
        self,
        task_id: int,
        task_data: schemas.TaskCreate,
        current_user_role: str,
        current_user: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Atualiza uma tarefa existente.
        Aplica regras de negócio baseadas no perfil do usuário.
        """
        # Verificar se a tarefa existe
        current_task = self.task_repository.find_by_id(task_id)
        if not current_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        
        # Guardar status anterior para o Observer
        old_status = current_task.get('status')
        
        # Restrições para usuário com role "visualizacao"
        if current_user_role == "visualizacao":
            # Visualização não pode alterar título, descrição ou owner_id
            if task_data.status and task_data.status == "concluida":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuários com perfil visualização não podem concluir tarefas"
                )
            # Apenas atualizar status, ignorar outros campos
            # Se status não foi fornecido, não atualizar nada
            if task_data.status:
                success = self.task_repository.update(
                    task_id=task_id,
                    titulo=None,
                    descricao=None,
                    status=task_data.status,
                    owner_id=None
                )
                if not success:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Tarefa não encontrada"
                    )
                # Buscar tarefa atualizada
                updated_task = self.task_repository.find_by_id(task_id)
                # Usar Observer Pattern para notificar se mudou para em_revisao
                self._notify_if_review(updated_task, old_status, current_user)
                return updated_task
            else:
                # Se não há status para atualizar, retornar tarefa atual
                return current_task
        else:
            # Admin e gerencial podem alterar tudo
            # Se owner_id foi fornecido, verificar se o usuário destino existe
            owner_id = None
            if task_data.owner_id is not None:
                target_user = self.user_repository.find_by_id(task_data.owner_id)
                if not target_user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuário destino não encontrado"
                    )
                owner_id = task_data.owner_id
            
            success = self.task_repository.update(
                task_id=task_id,
                titulo=task_data.titulo,
                descricao=task_data.descricao,
                status=task_data.status,
                owner_id=owner_id
            )
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Tarefa não encontrada"
                )
        
        # Retornar a tarefa atualizada
        updated_task = self.task_repository.find_by_id(task_id)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Erro ao buscar tarefa atualizada"
            )
        
        # Usar Observer Pattern para notificar se mudou para em_revisao
        self._notify_if_review(updated_task, old_status, current_user)
        
        return updated_task
    
    def _notify_if_review(self, task: Dict[str, Any], old_status: str, updated_by: Optional[Dict[str, Any]]) -> None:
        """
        Usa o padrão Observer para notificar quando uma tarefa muda de status.
        - Notifica admin/gerencial quando vai para "em_revisao"
        - Notifica o responsável quando vai para "concluida"
        
        Args:
            task: Tarefa atualizada
            old_status: Status anterior
            updated_by: Usuário que fez a atualização
        """
        new_status = task.get('status')
        
        # Debug: imprimir informações
        print(f"🔍 Verificando notificação: old_status={old_status}, new_status={new_status}")
        
        # Se mudou para em_revisao ou concluida, usar Observer Pattern
        if (new_status == 'em_revisao' and old_status != 'em_revisao') or \
           (new_status == 'concluida' and old_status != 'concluida'):
            status_msg = 'em_revisao' if new_status == 'em_revisao' else 'concluida'
            print(f"✅ Status mudou para '{status_msg}'! Disparando notificações...")
            # Criar Subject (tarefa)
            task_subject = TaskSubject(task)
            
            # Anexar observador de notificações
            task_subject.attach(self.notification_observer)
            
            # Notificar observadores
            task_subject.update_task(task, old_status, updated_by)
            
            # Desanexar observador (opcional, pode manter anexado)
            task_subject.detach(self.notification_observer)
            print(f"✅ Notificações disparadas via Observer Pattern")
        else:
            print(f"ℹ️  Não precisa notificar: old_status={old_status}, new_status={new_status}")
    
    def delete_task(self, task_id: int) -> bool:
        """Deleta uma tarefa."""
        success = self.task_repository.delete(task_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tarefa não encontrada"
            )
        return success

