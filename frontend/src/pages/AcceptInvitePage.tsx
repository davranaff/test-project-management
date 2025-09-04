import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { acceptInvite } from '../api/project';

export const AcceptInvitePage: React.FC = () => {
  const countdown = 3;
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const projectId = searchParams.get("project_id")
  const projectMembershipId = searchParams.get("project_membership_id")
  const { user } = useAuth();

  const handleFetch = async () => {
    if (user && projectId && projectMembershipId) {
      const response = await acceptInvite(projectId, projectMembershipId);
      return response
    }
    return null
  }

  useEffect(() => {
    handleFetch();
    setTimeout(() => navigate('/projects'), countdown * 1000);
  }, [user]);

  if (!user) {
    return (
      <div className="login-container">
        <div className="login-title">
          <h1>You are not Authorized</h1>
        </div>
      </div>
    )
  }

  return (
    <div className="login-container">
      <div className="login-title success-message">
        <h1>Successfully!</h1>
      </div>
      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        <p>You will be redirected to your projects in {countdown} seconds...</p>
        <button
          onClick={() => navigate('/projects')}
          className="btn"
          style={{ marginTop: '1rem' }}
        >
          Go to Projects Now
        </button>
      </div>
    </div>
  );
};
