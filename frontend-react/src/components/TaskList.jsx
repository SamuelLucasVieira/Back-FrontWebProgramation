// src/components/TaskList.jsx
import TaskItem from './TaskItem';

function TaskList({ tasks, onUpdateTask, onDeleteTask }) {
  if (tasks.length === 0) {
    return <p className="text-center text-gray-500 mt-8">Nenhuma tarefa cadastrada. Adicione uma! 🎉</p>;
  }

  return (
    <ul className="space-y-3">
      {tasks.map((task) => (
        <TaskItem 
          key={task.id} 
          task={task} 
          onUpdateTask={onUpdateTask} 
          onDeleteTask={onDeleteTask} 
        />
      ))}
    </ul>
  );
}

export default TaskList;