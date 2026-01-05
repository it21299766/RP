const express = require('express');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Sample data
let metrics = {
  totalStaff: 5,
  totalCourses: 8,
  totalAssignments: 0,
  assignmentRate: 0.0,
  unassigned: 8
};

let workloadData = [
  { name: 'Dr. Smith', workload: 18, capacity: 20 },
  { name: 'Dr. Johnson', workload: 15, capacity: 20 },
  { name: 'Dr. Williams', workload: 20, capacity: 20 },
  { name: 'Dr. Brown', workload: 12, capacity: 20 },
  { name: 'Dr. Davis', workload: 16, capacity: 20 }
];

let fairnessData = [
  { name: 'Dr. Smith', value: 18 },
  { name: 'Dr. Johnson', value: 15 },
  { name: 'Dr. Williams', value: 20 },
  { name: 'Dr. Brown', value: 12 },
  { name: 'Dr. Davis', value: 16 }
];

let staffData = [
  {
    id: 1,
    name: 'Dr. John Smith',
    email: 'john.smith@university.edu',
    department: 'Computer Science',
    position: 'Professor',
    teachingHours: 12,
    researchHours: 6,
    totalHours: 18
  },
  {
    id: 2,
    name: 'Dr. Sarah Johnson',
    email: 'sarah.johnson@university.edu',
    department: 'Mathematics',
    position: 'Associate Professor',
    teachingHours: 10,
    researchHours: 5,
    totalHours: 15
  },
  {
    id: 3,
    name: 'Dr. Michael Williams',
    email: 'michael.williams@university.edu',
    department: 'Physics',
    position: 'Professor',
    teachingHours: 15,
    researchHours: 5,
    totalHours: 20
  },
  {
    id: 4,
    name: 'Dr. Emily Brown',
    email: 'emily.brown@university.edu',
    department: 'Computer Science',
    position: 'Assistant Professor',
    teachingHours: 8,
    researchHours: 4,
    totalHours: 12
  },
  {
    id: 5,
    name: 'Dr. David Davis',
    email: 'david.davis@university.edu',
    department: 'Mathematics',
    position: 'Associate Professor',
    teachingHours: 11,
    researchHours: 5,
    totalHours: 16
  }
];

// API Routes

// Get dashboard metrics
app.get('/api/metrics', (req, res) => {
  res.json(metrics);
});

// Get workload distribution data
app.get('/api/workload-distribution', (req, res) => {
  res.json(workloadData);
});

// Get workload fairness data
app.get('/api/workload-fairness', (req, res) => {
  res.json(fairnessData);
});

// Get all dashboard data
app.get('/api/dashboard', (req, res) => {
  res.json({
    metrics,
    workloadDistribution: workloadData,
    workloadFairness: fairnessData
  });
});

// Update metrics
app.put('/api/metrics', (req, res) => {
  metrics = { ...metrics, ...req.body };
  res.json(metrics);
});

// Update workload distribution
app.put('/api/workload-distribution', (req, res) => {
  workloadData = req.body;
  res.json(workloadData);
});

// Update workload fairness
app.put('/api/workload-fairness', (req, res) => {
  fairnessData = req.body;
  res.json(fairnessData);
});

// Get staff members
app.get('/api/staff', (req, res) => {
  res.json(staffData);
});

// Get single staff member
app.get('/api/staff/:id', (req, res) => {
  const staff = staffData.find(s => s.id === parseInt(req.params.id));
  if (staff) {
    res.json(staff);
  } else {
    res.status(404).json({ error: 'Staff member not found' });
  }
});

// Add new staff member
app.post('/api/staff', (req, res) => {
  const newStaff = {
    id: staffData.length + 1,
    ...req.body
  };
  staffData.push(newStaff);
  res.json(newStaff);
});

// Update staff member
app.put('/api/staff/:id', (req, res) => {
  const index = staffData.findIndex(s => s.id === parseInt(req.params.id));
  if (index !== -1) {
    staffData[index] = { ...staffData[index], ...req.body };
    res.json(staffData[index]);
  } else {
    res.status(404).json({ error: 'Staff member not found' });
  }
});

// Delete staff member
app.delete('/api/staff/:id', (req, res) => {
  const index = staffData.findIndex(s => s.id === parseInt(req.params.id));
  if (index !== -1) {
    staffData.splice(index, 1);
    res.json({ message: 'Staff member deleted' });
  } else {
    res.status(404).json({ error: 'Staff member not found' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Server is running' });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

