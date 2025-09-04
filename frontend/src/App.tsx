
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { ProjectsPage } from './pages/ProjectsPage';
import { ProjectDetailPage } from './pages/ProjectDetailPage';
import { GoogleCallbackPage } from './pages/GoogleCallbackPage';
import { EmailVerificationPage } from './pages/EmailVerificationPage';
import { ProjectInvitePage } from './pages/ProjectInvitePage';
import { AcceptInvitePage } from './pages/AcceptInvitePage';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const PublicRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return !isAuthenticated ? <>{children}</> : <Navigate to="/projects" />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route
            path="/login"
            element={
              <PublicRoute>
                <LoginPage />
              </PublicRoute>
            }
          />
          <Route
            path="/register"
            element={
              <PublicRoute>
                <RegisterPage />
              </PublicRoute>
            }
          />
          <Route
            path="/projects"
            element={
              <PrivateRoute>
                <ProjectsPage />
              </PrivateRoute>
            }
          />
          <Route
            path="/projects/:projectId"
            element={
              <PrivateRoute>
                <ProjectDetailPage />
              </PrivateRoute>
            }
          />
          <Route path="/oauth/google/callback" element={<GoogleCallbackPage />} />
          <Route path="/verify-email" element={<EmailVerificationPage />} />
          <Route path="/accept_invite" element={<AcceptInvitePage />} />
          <Route
            path="/projects/:projectId/invite"
            element={
              <PrivateRoute>
                <ProjectInvitePage />
              </PrivateRoute>
            }
          />
          <Route path="/" element={<Navigate to="/projects" />} />
          <Route path="*" element={<Navigate to="/projects" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
