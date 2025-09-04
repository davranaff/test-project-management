import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const GoogleCallbackPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();
  const [countdown, setCountdown] = useState(3);

  useEffect(() => {
    const access_token = searchParams.get('access_token');
    const refresh_token = searchParams.get('refresh_token');
    const userId = searchParams.get('user_id');
    const email = searchParams.get('email');
    const role = searchParams.get('role');

    if (!userId || !email || !role) {
      navigate('/login');
      return;
    }

    const user = {
      id: parseInt(userId, 10),
      email: email,
      name: searchParams.get('name') || undefined,
      picture: searchParams.get('picture') || undefined,
      role: role as 'admin' | 'member',
    };

    if (access_token && refresh_token) {
      authLogin({
        access: access_token,
        refresh: refresh_token,
        user,
      });

      const timer = setInterval(() => {
        setCountdown((prev) => {
          if (prev <= 1) {
            clearInterval(timer);
            navigate('/projects');
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    } else {
      navigate('/login');
    }
  }, [searchParams, authLogin, navigate]);

  return (
    <div className="login-container">
      <div className="login-title">
        <h1>Successfully logged in!</h1>
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
