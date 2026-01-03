# Staff Workload Allocation System

A React-based dashboard application for monitoring and managing staff workload distribution with a Node.js/Express backend API.

## Features

- **Dashboard Metrics**: View key metrics including:
  - Total Staff
  - Total Courses
  - Total Assignments
  - Assignment Rate

- **Workload Distribution Chart**: Visualize current workload vs capacity for each staff member

- **Workload Fairness Chart**: Analyze the distribution of workload across staff members

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

1. **Install Frontend Dependencies:**
```bash
npm install
```

2. **Install Backend Dependencies:**
```bash
cd backend
npm install
cd ..
```

### Running the Application

You need to run both the frontend and backend servers:

#### Option 1: Run in Separate Terminals

**Terminal 1 - Backend Server:**
```bash
cd backend
npm start
```
The backend will run on `http://localhost:5000`

**Terminal 2 - Frontend Server:**
```bash
npm start
```
The frontend will run on `http://localhost:3000` and automatically open in your browser.

#### Option 2: Run Backend in Development Mode (with auto-reload)

**Terminal 1 - Backend Server (with nodemon):**
```bash
cd backend
npm run dev
```

**Terminal 2 - Frontend Server:**
```bash
npm start
```

## API Endpoints

The backend provides the following endpoints:

- `GET /api/health` - Health check
- `GET /api/metrics` - Get dashboard metrics
- `GET /api/workload-distribution` - Get workload distribution data
- `GET /api/workload-fairness` - Get workload fairness data
- `GET /api/dashboard` - Get all dashboard data at once
- `PUT /api/metrics` - Update metrics
- `PUT /api/workload-distribution` - Update workload distribution
- `PUT /api/workload-fairness` - Update workload fairness

## Project Structure

```
├── backend/
│   ├── server.js          # Express server
│   └── package.json       # Backend dependencies
├── src/
│   ├── components/
│   │   ├── Dashboard.js
│   │   ├── MetricsCard.js
│   │   ├── Sidebar.js
│   │   ├── WorkloadDistributionChart.js
│   │   └── WorkloadFairnessChart.js
│   ├── App.js
│   └── index.js
├── public/
└── package.json           # Frontend dependencies
```

## Technologies Used

- **Frontend**: React 18, Recharts
- **Backend**: Node.js, Express, CORS

## Customization

You can modify the data in `backend/server.js` to connect to your own database or data source.
