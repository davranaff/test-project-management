import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { axiosInstance } from '../api/axios';
import { useAuth } from '../contexts/AuthContext';

export const ProjectInvitePage: React.FC = () => {
  const { projectId } = useParams();
  const { isAdmin } = useAuth();
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'sending' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  if (!isAdmin()) {
    return (
      <div className="login-container">
        <div className="login-title">
          <h1>Access Denied</h1>
          <p>Only administrators can invite users to projects.</p>
        </div>
      </div>
    );
  }

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('sending');

    try {
      await axiosInstance.post(`/projects/invite/`, { email, project: projectId });
      setStatus('success');
      setMessage('Invitation sent successfully!');
      setEmail('');
    } catch (error: any) {
      setStatus('error');
      setMessage(error.response?.data?.detail || 'Failed to send invitation');
    }
  };

  return (
    <div className="container">
      <h1>Invite User to Project</h1>

      <form onSubmit={handleInvite} className="form">
        <div className="form-group">
          <label htmlFor="email">User Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter user email"
            className="form-control"
            required
          />
        </div>

        {status === 'success' && (
          <div className="success-message">{message}</div>
        )}
        {status === 'error' && (
          <div className="error-message">{message}</div>
        )}

        <button
          type="submit"
          className="btn"
          disabled={status === 'sending'}
        >
          {status === 'sending' ? 'Sending Invitation...' : 'Send Invitation'}
        </button>
      </form>
    </div>
  );
};
