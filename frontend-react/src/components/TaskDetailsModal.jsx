// src/components/TaskDetailsModal.jsx
function TaskDetailsModal({ task, isOpen, onClose, onUpdateTask, onDeleteTask, users = [], canAssignTasks = false, currentUserRole = 'visualizacao' }) {
  if (!isOpen || !task) return null;

  const getStatusLabel = (status) => {
    const statusMap = {
      'pendente': 'Pendente',
      'em_andamento': 'Em Andamento',
      'em_revisao': 'Em Revisão',
      'concluida': 'Concluída'
    };
    return statusMap[status] || status;
  };

  const getStatusColor = (status) => {
    const colorMap = {
      'pendente': 'bg-gray-200 text-gray-800',
      'em_andamento': 'bg-blue-200 text-blue-800',
      'em_revisao': 'bg-yellow-200 text-yellow-800',
      'concluida': 'bg-green-200 text-green-800'
    };
    return colorMap[status] || 'bg-gray-200 text-gray-800';
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Não informado';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  };

  const handleStatusChange = (newStatus) => {
    if (currentUserRole === 'visualizacao' && newStatus === 'concluida') {
      alert('Usuários com perfil visualização não podem concluir tarefas');
      return;
    }
    onUpdateTask({ ...task, status: newStatus });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4" onClick={onClose}>
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="bg-blue-600 text-white p-6 rounded-t-lg">
          <div className="flex justify-between items-start">
            <h2 className="text-2xl font-bold">{task.titulo}</h2>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 text-2xl font-bold"
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Status */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Status
            </label>
            <select
              value={task.status}
              onChange={(e) => handleStatusChange(e.target.value)}
              className={`w-full px-4 py-2 border border-gray-300 rounded-md ${getStatusColor(task.status)} font-semibold`}
              disabled={currentUserRole === 'visualizacao' && task.status === 'concluida'}
            >
              <option value="pendente">Pendente</option>
              <option value="em_andamento">Em Andamento</option>
              <option value="em_revisao">Em Revisão</option>
              {currentUserRole !== 'visualizacao' && (
                <option value="concluida">Concluída</option>
              )}
            </select>
          </div>

          {/* Descrição */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Descrição
            </label>
            <div className="bg-gray-50 p-4 rounded-md border border-gray-200 min-h-[100px]">
              <p className="text-gray-700 whitespace-pre-wrap">
                {task.descricao || 'Sem descrição'}
              </p>
            </div>
          </div>

          {/* Informações Adicionais */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Responsável */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Responsável
              </label>
              <div className="bg-gray-50 p-3 rounded-md border border-gray-200">
                <p className="text-gray-700">
                  {task.owner_username || 'Não atribuído'}
                </p>
              </div>
            </div>

            {/* Data de Criação */}
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Data de Criação
              </label>
              <div className="bg-gray-50 p-3 rounded-md border border-gray-200">
                <p className="text-gray-700">
                  {formatDate(task.created_at)}
                </p>
              </div>
            </div>
          </div>

          {/* ID da Tarefa */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              ID da Tarefa
            </label>
            <div className="bg-gray-50 p-3 rounded-md border border-gray-200">
              <p className="text-gray-700 font-mono text-sm">
                #{task.id}
              </p>
            </div>
          </div>
        </div>

        {/* Footer com Ações */}
        {currentUserRole !== 'visualizacao' && (
          <div className="bg-gray-50 p-6 rounded-b-lg border-t border-gray-200 flex justify-end gap-3">
            <button
              onClick={() => {
                if (window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
                  onDeleteTask(task.id);
                  onClose();
                }
              }}
              className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 font-semibold"
            >
              Excluir Tarefa
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 font-semibold"
            >
              Fechar
            </button>
          </div>
        )}

        {currentUserRole === 'visualizacao' && (
          <div className="bg-gray-50 p-6 rounded-b-lg border-t border-gray-200 flex justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 font-semibold"
            >
              Fechar
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default TaskDetailsModal;

