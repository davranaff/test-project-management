import { axiosInstance } from './axios';
import { Project, Task, CreateProjectRequest, CreateTaskRequest, UpdateTaskRequest } from '../types/project';

export const getProjects = async () => {
  const response = await axiosInstance.get<Project[]>('/projects/');
  return response.data;
};

export const getProject = async (projectId: number) => {
  const response = await axiosInstance.get<Project>(`/projects/${projectId}/`);
  return response.data;
};

export const createProject = async (data: CreateProjectRequest) => {
  const response = await axiosInstance.post<Project>('/projects/', data);
  return response.data;
};

export const updateProject = async (projectId: number, data: Partial<CreateProjectRequest>) => {
  const response = await axiosInstance.put<Project>(`/projects/${projectId}/`, data);
  return response.data;
};

export const deleteProject = async (projectId: number) => {
  await axiosInstance.delete(`/projects/${projectId}/`);
};

export const getTasks = async (projectId: number) => {
  const response = await axiosInstance.get<Task[]>(`/projects/${projectId}/tasks/`);
  return response.data;
};

export const createTask = async (projectId: number, data: CreateTaskRequest) => {
  const response = await axiosInstance.post<Task>(`/projects/${projectId}/tasks/`, data);
  return response.data;
};

export const updateTask = async (projectId: number, taskId: number, data: UpdateTaskRequest) => {
  const response = await axiosInstance.put<Task>(`/projects/${projectId}/tasks/${taskId}/`, data);
  return response.data;
};

export const deleteTask = async (projectId: number, taskId: number) => {
  await axiosInstance.delete(`/projects/${projectId}/tasks/${taskId}/`);
};

export const inviteToProject = async (projectId: number, email: string) => {
  const response = await axiosInstance.post('/projects/invite/', { project_id: projectId, email });
  return response.data;
};

export const acceptInvite = async (projectId: string, projectMembershipId: string) => {
    await axiosInstance.get(
        '/projects/invite/',
        {
            params: {
                project_id: projectId,
                project_membership_id: projectMembershipId,
            }
        }
    );
}
