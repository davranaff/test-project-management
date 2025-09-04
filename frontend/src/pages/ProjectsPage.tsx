import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getProjects, createProject } from '../api/project';
import { Project } from '../types/project';
import { RoleBased } from '../components/RoleBased';

export const ProjectsPage: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isCreating, setIsCreating] = useState(false);
  const [newProject, setNewProject] = useState({
    title: '',
    description: '',
    start_date: '',
    end_date: '',
    assignees: [] as number[]
  });
  const [error, setError] = useState('');

  const fetchProjects = async () => {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (err) {
      setError('Failed to fetch projects');
    }
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  const handleCreateProject = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const project = await createProject(newProject);
      setProjects([...projects, project]);
      setIsCreating(false);
      setNewProject({
        title: '',
        description: '',
        start_date: '',
        end_date: '',
        assignees: []
      });
    } catch (err) {
      setError('Failed to create project');
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Projects</h1>
        <RoleBased allowedRoles={['admin']}>
          <button
            onClick={() => setIsCreating(true)}
            className="btn"
          >
            Create Project
          </button>
        </RoleBased>
      </div>

      {error && <div className="error">{error}</div>}

      {isCreating && (
        <div>
          <form onSubmit={handleCreateProject}>
            <div className="form-group">
              <label>Title</label>
              <input
                type="text"
                value={newProject.title}
                onChange={(e) =>
                  setNewProject({ ...newProject, title: e.target.value })
                }
                className="form-control"
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                value={newProject.description}
                onChange={(e) =>
                  setNewProject({ ...newProject, description: e.target.value })
                }
                className="form-control"
                required
              />
            </div>
            <div className="form-group">
              <label>Start Date</label>
              <input
                type="date"
                value={newProject.start_date}
                onChange={(e) =>
                  setNewProject({ ...newProject, start_date: e.target.value })
                }
                className="form-control"
                required
              />
            </div>
            <div className="form-group">
              <label>End Date</label>
              <input
                type="date"
                value={newProject.end_date}
                onChange={(e) =>
                  setNewProject({ ...newProject, end_date: e.target.value })
                }
                className="form-control"
                required
              />
            </div>
            <div>
              <button type="button" onClick={() => setIsCreating(false)} className="btn">
                Cancel
              </button>
              <button type="submit" className="btn">
                Create
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="project-grid">
        {projects.map((project) => (
          <Link
            key={project.id}
            to={`/projects/${project.id}`}
            className="project-card"
          >
            <h2>{project.title}</h2>
            <p>{project.description}</p>
            <div>
              <div>Start: {new Date(project.start_date).toLocaleDateString()}</div>
              <div>End: {new Date(project.end_date).toLocaleDateString()}</div>
              <div>Created: {new Date(project.created_at).toLocaleDateString()}</div>
              <div>Team: {project.assignees.length} members</div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};
