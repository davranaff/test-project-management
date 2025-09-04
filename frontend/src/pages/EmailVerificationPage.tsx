import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { axiosInstance } from '../api/axios';

export const EmailVerificationPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState<'verifying' | 'success' | 'error'>('verifying');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = searchParams.get('token');
    if (!token) {
      setStatus('error');
      setMessage('Verification token is missing');
      return;
    }

    const verifyEmail = async () => {
      try {
        await axiosInstance.post('/auth/verify-email/', { token });
        setStatus('success');
        setMessage('Email successfully verified! You can now use all features.');
        setTimeout(() => navigate('/login'), 3000);
      } catch (error: any) {
        setStatus('error');
        setMessage(error.response?.data?.detail || 'Verification failed. Please try again.');
      }
    };

    verifyEmail();
  }, [searchParams, navigate]);

  return (
    <div className="login-container">
      <div className="login-title">
        <h1>Email Verification</h1>
      </div>
      <div style={{ textAlign: 'center', marginTop: '2rem' }}>
        {status === 'verifying' && (
          <p>Verifying your email...</p>
        )}
        {status === 'success' && (
          <>
            <p className="success-message">{message}</p>
            <p>Redirecting to login page...</p>
          </>
        )}
        {status === 'error' && (
          <p className="error-message">{message}</p>
        )}
      </div>
    </div>
  );
};
