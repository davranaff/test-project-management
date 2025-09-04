import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Role } from '../types/auth';

interface RoleBasedProps {
  allowedRoles: Role[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export const RoleBased: React.FC<RoleBasedProps> = ({
  allowedRoles,
  children,
  fallback = null
}) => {
  const { user } = useAuth();

  if (!user || !allowedRoles.includes(user.role)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
};
