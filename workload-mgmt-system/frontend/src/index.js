/**
 * Application Entry Point
 * 
 * This is the main entry point for the React application. It:
 * 1. Renders the root React component
 * 2. Wraps the app in AuthProvider for authentication context
 * 3. Enables React StrictMode for development warnings
 * 
 * The AuthProvider makes authentication state (user, token, login/logout) 
 * available to all components in the application tree.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { AuthProvider } from './context/AuthContext';

// Get the root DOM element where the React app will be mounted
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the application
// StrictMode helps identify potential problems during development
// AuthProvider wraps the app to provide authentication context to all components
root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);

