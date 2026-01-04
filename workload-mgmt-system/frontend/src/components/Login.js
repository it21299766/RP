import React, { useState, useContext } from 'react';
import './Login.css';
import Swal from 'sweetalert2';
import { login as loginApi } from '../api/authApi';
import { AuthContext } from '../context/AuthContext';

const Login = ({ onLogin }) => {
  const { login } = useContext(AuthContext);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    // Validate inputs
    if (!username.trim()) {
      setError('Please enter your username.');
      setLoading(false);
      return;
    }
    if (!password) {
      setError('Please enter your password.');
      setLoading(false);
      return;
    }

    try {
      // Call login API with username
      const response = await loginApi(username.trim(), password);
      
      // Update AuthContext
      login(response.access_token, response.user);

      await Swal.fire({
        icon: 'success',
        title: 'Login Successful',
        text: `Welcome, ${response.user.name}!`,
        showConfirmButton: false,
        timer: 1600,
        timerProgressBar: true,
      });

      // Call onLogin callback if provided
      if (onLogin) {
        onLogin();
      }
    } catch (err) {
      // Handle error
      const errorMessage = err.response?.data?.detail || err.message || 'Login failed. Please try again.';
      setError(errorMessage);
      
      await Swal.fire({
        icon: 'error',
        title: 'Login Failed',
        text: errorMessage,
        confirmButtonText: 'OK'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="login-page"
      style={{
        backgroundImage: `linear-gradient(135deg, rgba(15, 23, 42, 0.35), rgba(30, 41, 59, 0.35)), url("${encodeURI(
          `${process.env.PUBLIC_URL}/images/SLIIT login.jpg`
        )}")`,
      }}
    >
      <div className="login-card">
        <div className="login-header">
          <div className="login-title">Staff Workload System</div>
          <div className="login-subtitle">Sign in to continue</div>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="login-field">
            <label htmlFor="username">Username</label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username (e.g., sf1, adm1)"
              autoComplete="username"
              disabled={loading}
            />
          </div>

          <div className="login-field">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              autoComplete="current-password"
              disabled={loading}
            />
          </div>

          {error ? <div className="login-error">{error}</div> : null}

          <button 
            className="login-button" 
            type="submit"
            disabled={loading}
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;


