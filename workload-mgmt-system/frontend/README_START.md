# Frontend Startup Guide

This guide explains how to start the WAM frontend development server.

## Prerequisites

1. **Node.js 14+** installed (includes npm)
2. **Backend server** running (http://localhost:8000)

## Quick Start

### Step 1: Install Dependencies (First Time Only)

If `node_modules` folder doesn't exist:

```bash
npm install
```

### Step 2: Run Startup Script

Simply double-click `start_frontend.bat` or run from command line:

```bash
start_frontend.bat
```

The script will:
1. ✅ Check if Node.js is installed
2. ✅ Verify npm is available
3. ✅ Install dependencies if needed
4. ✅ Start the React development server

## Manual Start (Alternative)

If you prefer to start manually:

```bash
# Install dependencies (first time only)
npm install

# Start development server
npm start
```

## Access Points

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000 (must be running)

## Troubleshooting

### Error: Node.js not found
- Install Node.js from https://nodejs.org/
- Restart command prompt after installation
- Verify installation: `node --version`

### Error: npm not found
- Node.js includes npm
- Reinstall Node.js if npm is missing
- Verify: `npm --version`

### Error: Cannot connect to backend
- Ensure backend server is running (http://localhost:8000)
- Check backend `.env` file is configured correctly
- Verify backend server is accessible: http://localhost:8000/docs

### Error: Port 3000 already in use
- Stop other applications using port 3000
- Or set different port: `set PORT=3001 && npm start`

### Error: Module not found
- Delete `node_modules` folder
- Delete `package-lock.json`
- Run `npm install` again

## Development Notes

- Hot reload is enabled (code changes automatically refresh browser)
- Browser will automatically open to http://localhost:3000
- Press Ctrl+C to stop the server
- Check browser console for errors

