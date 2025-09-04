export type Role = 'admin' | 'member';

export interface User {
  id: number;
  email: string;
  name?: string;
  picture?: string;
  role: Role;
}

export interface LoginRequest {
  email?: string;
  username?: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username?: string;
  password: string;
  confirm_password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  expires_at?: number;
  user?: User;
}
