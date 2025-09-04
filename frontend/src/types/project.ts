export interface Project {
  id: number;
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  assignees: number[];
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number;
  project: number;
  title: string;
  description: string;
  due_date: string;
  status: 'todo' | 'in_progress' | 'done';
  assignees: number[];
  created_at: string;
  updated_at: string;
  version: number;
}

export interface ProjectMembership {
  id: number;
  user: number;
  project: number;
  invited_by: number | null;
  status: 'pending' | 'accepted' | 'rejected';
  joined_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface CreateProjectRequest {
  title: string;
  description: string;
  start_date: string;
  end_date: string;
  assignees?: number[];
}

export interface CreateTaskRequest {
  title: string;
  description: string;
  due_date: string;
  status: 'todo' | 'in_progress' | 'done';
  assignees?: number[];
}

export type UpdateTaskRequest = Partial<CreateTaskRequest>;
