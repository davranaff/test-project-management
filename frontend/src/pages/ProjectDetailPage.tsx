import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProject, getTasks, createTask, updateTask, deleteTask } from '../api/project';
import { Project, Task } from '../types/project';
import { useAuth } from '../contexts/AuthContext';
import { RoleBased } from '../components/RoleBased';
import '../styles/ProjectDetail.css';

export const ProjectDetailPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { user, isAdmin, isMember } = useAuth();
  const [project, setProject] = useState<Project | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [newTask, setNewTask] = useState<{
    title: string;
    description: string;
    status: Task['status'];
    due_date: string;
  }>({
    title: '',
    description: '',
    status: 'todo',
    due_date: '',
  });
  const [error, setError] = useState('');

  const fetchProjectAndTasks = async () => {
    try {
      const projectData = await getProject(Number(projectId));
      setProject(projectData);
      const tasksData = await getTasks(Number(projectId));
      setTasks(tasksData);
    } catch (err) {
      setError('Failed to fetch project data');
    }
  };

  useEffect(() => {
    if (projectId) {
      fetchProjectAndTasks();
    }
  }, [projectId]);

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const task = await createTask(Number(projectId), newTask);
      setTasks([...tasks, task]);
      setIsCreating(false);
      setNewTask({
        title: '',
        description: '',
        status: 'todo',
        due_date: '',
      });
    } catch (err) {
      setError('Failed to create task');
    }
  };

  const handleUpdateTaskStatus = async (taskId: number, newStatus: Task['status']) => {
    try {
      const currentTask = tasks.find(t => t.id === taskId);
      if (!currentTask) {
        throw new Error('Task not found');
      }

      const updatedTask = await updateTask(Number(projectId), taskId, {
        status: newStatus,
      });
      setTasks(tasks.map(task => task.id === taskId ? updatedTask : task));
    } catch (err: any) {
      if (err.response?.status === 409) {
        setError('Task was modified by another user. Please refresh and try again.');
        await fetchProjectAndTasks();
      } else {
        setError('Failed to update task');
      }
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await deleteTask(Number(projectId), taskId);
        setTasks(tasks.filter(task => task.id !== taskId));
      } catch (err) {
        setError('Failed to delete task');
      }
    }
  };

  const canEditTask = (task: Task) => {
    return isAdmin() || isMember() || task.assignees.includes(user?.id || 0);
  };

  if (!project) {
    return <div className="container">Loading...</div>;
  };

  return (
    <div className="container">
      <div className="project-header">
        <h1>{project.title}</h1>
        <p className="project-description">{project.description}</p>
        <div className="project-meta">
          <span>Start: {new Date(project.start_date).toLocaleDateString()}</span>
          <span>Due: {new Date(project.end_date).toLocaleDateString()}</span>
        </div>

        <RoleBased allowedRoles={['admin']}>
          <div className="project-actions">
            <button
              className="btn"
              onClick={() => navigate(`/projects/${projectId}/edit`)}
            >
              Edit Project
            </button>
            <button
              className="btn"
              onClick={() => navigate(`/projects/${projectId}/invite`)}
            >
              Invite Members
            </button>
          </div>
        </RoleBased>
      </div>

      <div className="tasks-section">
        <div className="flex-between">
          <h2>Tasks</h2>
          <RoleBased allowedRoles={['admin']}>
            <button className="btn" onClick={() => setIsCreating(true)}>
              Add Task
            </button>
          </RoleBased>
        </div>

        {isCreating && (
          <form onSubmit={handleCreateTask} className="task-form">
            <div className="form-group">
              <label className="label">Title</label>
              <input
                className="form-control"
                value={newTask.title}
                onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                required
              />
            </div>
            <div className="form-group">
              <label className="label">Description</label>
              <textarea
                className="form-control"
                value={newTask.description}
                onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                rows={3}
                required
              />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label className="label">Due Date</label>
                <input
                  type="date"
                  className="form-control"
                  value={newTask.due_date}
                  onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label className="label">Status</label>
                <select
                  className="form-control"
                  value={newTask.status}
                  onChange={(e) => setNewTask({ ...newTask, status: e.target.value as Task['status'] })}
                >
                  <option value="todo">To Do</option>
                  <option value="in_progress">In Progress</option>
                  <option value="done">Done</option>
                </select>
              </div>
            </div>
            <div className="task-form-actions">
              <button type="submit" className="btn">Create Task</button>
              <button
                type="button"
                className="btn"
                onClick={() => setIsCreating(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        <div className="tasks-board">
          <div className="tasks-column">
            <h3>To Do</h3>
            {tasks
              .filter(task => task.status === 'todo')
              .map(task => (
                <div key={task.id} className="task-item">
                  <div className="task-title">{task.title}</div>
                  <div className="task-description">{task.description}</div>
                  <div className="task-meta">
                    Due: {new Date(task.due_date).toLocaleDateString()}
                  </div>
                  {canEditTask(task) && (
                    <div className="task-actions">
                      <select
                        className="form-control"
                        value={task.status}
                        onChange={(e) => handleUpdateTaskStatus(task.id, e.target.value as Task['status'])}
                      >
                        <option value="todo">To Do</option>
                        <option value="in_progress">In Progress</option>
                        <option value="done">Done</option>
                      </select>
                      <RoleBased allowedRoles={['admin']}>
                        <button
                          className="btn button-small button-danger"
                          onClick={() => handleDeleteTask(task.id)}
                        >
                          Delete
                        </button>
                      </RoleBased>
                    </div>
                  )}
                </div>
              ))}
          </div>

          <div className="tasks-column">
            <h3>In Progress</h3>
            {tasks
              .filter(task => task.status === 'in_progress')
              .map(task => (
                <div key={task.id} className="task-item">
                  <div className="task-title">{task.title}</div>
                  <div className="task-description">{task.description}</div>
                  <div className="task-meta">
                    Due: {new Date(task.due_date).toLocaleDateString()}
                  </div>
                  {canEditTask(task) && (
                    <div className="task-actions">
                      <select
                        className="form-control"
                        value={task.status}
                        onChange={(e) => handleUpdateTaskStatus(task.id, e.target.value as Task['status'])}
                      >
                        <option value="todo">To Do</option>
                        <option value="in_progress">In Progress</option>
                        <option value="done">Done</option>
                      </select>
                      <RoleBased allowedRoles={['admin']}>
                        <button
                          className="btn button-small button-danger"
                          onClick={() => handleDeleteTask(task.id)}
                        >
                          Delete
                        </button>
                      </RoleBased>
                    </div>
                  )}
                </div>
              ))}
          </div>

          <div className="tasks-column">
            <h3>Done</h3>
            {tasks
              .filter(task => task.status === 'done')
              .map(task => (
                <div key={task.id} className="task-item">
                  <div className="task-title">{task.title}</div>
                  <div className="task-description">{task.description}</div>
                  <div className="task-meta">
                    Due: {new Date(task.due_date).toLocaleDateString()}
                  </div>
                  <div className="task-actions">
                    {canEditTask(task) && (
                      <select
                        className="form-control"
                        value={task.status}
                        onChange={(e) => handleUpdateTaskStatus(task.id, e.target.value as Task['status'])}
                      >
                        <option value="todo">To Do</option>
                        <option value="in_progress">In Progress</option>
                        <option value="done">Done</option>
                      </select>
                    )}
                    <RoleBased allowedRoles={['admin']}>
                      <button
                        className="btn button-small button-danger"
                        onClick={() => handleDeleteTask(task.id)}
                      >
                        Delete
                      </button>
                    </RoleBased>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>

      {error && (
        <div className="message message-error">{error}</div>
      )}
    </div>
  );
};