import { axiosInstance } from './axios';
import { LoginRequest, RegisterRequest, AuthResponse } from '../types/auth';

export const login = async (data: LoginRequest) => {
  const response = await axiosInstance.post<AuthResponse>('/login/', data);
  return response.data;
};

export const register = async (data: RegisterRequest) => {
  const response = await axiosInstance.post<AuthResponse>('/register/', data);
  return response.data;
};

export const verifyEmail = async (token: string) => {
  const response = await axiosInstance.post('/verify-email/', { token });
  return response.data;
};

export const logout = async () => {
  const response = await axiosInstance.post('/logout/');
  return response.data;
};

export const loginWithGoogle = async (code: string) => {
  const response = await axiosInstance.get<AuthResponse>(`/login/?code=${code}`);
  return response.data;
};
