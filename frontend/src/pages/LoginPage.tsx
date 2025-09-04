import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';
import { useAuth } from '../contexts/AuthContext';
import { axiosInstance } from '../api/axios';

export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await login({ email, password });
      authLogin(response);
      navigate('/projects');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to login');
    }
  };

  const handleGoogleLogin = async () => {
    try {
      const response = await axiosInstance.get('/oauth/', {
        params: { oauth_type: 'google' }
      });

      if (response.data.detail) {
        window.location.href = response.data.detail;
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to initialize Google login');
    }
  };

  return (
    <div className="login-container">
      <div className="login-title">
        <h1>Sign in</h1>
      </div>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div style={{ marginTop: '1.5rem' }}>
          <button type="submit" className="btn" style={{ width: '100%' }}>
            Sign in
          </button>
        </div>

        <div style={{ marginTop: '1rem' }}>
          <button
            type="button"
            onClick={handleGoogleLogin}
            className="btn"
            style={{
              width: '100%',
              backgroundColor: '#fff',
              color: '#333',
              border: '1px solid #ddd'
            }}
          >
            Sign in with Google
          </button>
        </div>
      </form>

      <div className="login-footer">
        Don't have an account?{' '}
        <button
          onClick={() => navigate('/register')}
          className="link-button"
        >
          Register here
        </button>
      </div>
    </div>
  );
};
