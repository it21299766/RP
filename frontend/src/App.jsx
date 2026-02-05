import React, { useState,  } from 'react';
import { MapPin, Bus, Users, Clock, DollarSign, Settings, BarChart3, TrendingUp, AlertCircle, CheckCircle, Zap, Navigation, Calendar, UserCircle } from 'lucide-react';
import './App.css';
const App = () => {
  const [activeRole, setActiveRole] = useState('admin');
  const [activePage, setActivePage] = useState('dashboard');
  const [optimizationRunning, setOptimizationRunning] = useState(false);
  const [optimizationProgress, setOptimizationProgress] = useState(0);

  // Simulate optimization process
  const runOptimization = () => {
    setOptimizationRunning(true);
    setOptimizationProgress(0);
    const interval = setInterval(() => {
      setOptimizationProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setOptimizationRunning(false);
          return 100;
        }
        return prev + 10;
      });
    }, 500);
  };

  // Sample data
  const routes = [
    { id: 'A', time: 40, cost: 1200, pickups: 5, passengers: 45, efficiency: 92 },
    { id: 'B', time: 45, cost: 950, pickups: 4, passengers: 38, efficiency: 88 },
    { id: 'C', time: 52, cost: 750, pickups: 3, passengers: 32, efficiency: 85 }
  ];

  const pickupPoints = [
    { id: 1, name: 'Colombo Fort', lat: 6.9271, lon: 79.8612, users: 18, status: 'active', cluster: 1 },
    { id: 2, name: 'Bambalapitiya', lat: 6.8916, lon: 79.8540, users: 32, status: 'active', cluster: 2 },
    { id: 3, name: 'Wellawatte', lat: 6.8741, lon: 79.8585, users: 5, status: 'inactive', cluster: 3 },
    { id: 4, name: 'Dehiwala', lat: 6.8519, lon: 79.8630, users: 24, status: 'active', cluster: 4 },
    { id: 5, name: 'Mount Lavinia', lat: 6.8385, lon: 79.8638, users: 15, status: 'active', cluster: 5 }
  ];

  const NavigationBar = () => (
    <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <Bus className="w-8 h-8" />
            <div>
              <h1 className="text-2xl font-bold">SmartShuttle</h1>
              <p className="text-xs text-indigo-200">AI-Powered Route Optimization</p>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button
              onClick={() => setActiveRole('student')}
              className={`px-4 py-2 rounded-lg transition ${activeRole === 'student' ? 'bg-white text-indigo-600' : 'bg-indigo-500 hover:bg-indigo-400'}`}
            >
              <UserCircle className="w-4 h-4 inline mr-2" />
              Student
            </button>
            <button
              onClick={() => setActiveRole('admin')}
              className={`px-4 py-2 rounded-lg transition ${activeRole === 'admin' ? 'bg-white text-indigo-600' : 'bg-indigo-500 hover:bg-indigo-400'}`}
            >
              <Settings className="w-4 h-4 inline mr-2" />
              Admin
            </button>
            <button
              onClick={() => setActiveRole('system')}
              className={`px-4 py-2 rounded-lg transition ${activeRole === 'system' ? 'bg-white text-indigo-600' : 'bg-indigo-500 hover:bg-indigo-400'}`}
            >
              <Zap className="w-4 h-4 inline mr-2" />
              System
            </button>
          </div>
        </div>
      </div>
    </div>
  );

  const DashboardView = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <StatCard icon={<Bus />} title="Active Routes" value="12" color="blue" trend="+2" />
        <StatCard icon={<Users />} title="Total Users" value="847" color="green" trend="+45" />
        <StatCard icon={<MapPin />} title="Pickup Points" value="28" color="purple" trend="+3" />
        <StatCard icon={<Clock />} title="Avg Time" value="42 min" color="orange" trend="-5 min" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <BarChart3 className="w-5 h-5 mr-2 text-indigo-600" />
            Optimization Results (Pareto Front)
          </h3>
          <div className="space-y-3">
            {routes.map(route => (
              <div key={route.id} className="border-l-4 border-indigo-500 bg-indigo-50 p-4 rounded-r-lg">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-bold text-lg text-indigo-700">Route {route.id}</span>
                  <span className="bg-indigo-600 text-white px-3 py-1 rounded-full text-sm">
                    {route.efficiency}% Efficient
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600">Time:</span>
                    <span className="font-semibold ml-2">{route.time} min</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Cost:</span>
                    <span className="font-semibold ml-2">Rs. {route.cost}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Pickups:</span>
                    <span className="font-semibold ml-2">{route.pickups}</span>
                  </div>
                  <div>
                    <span className="text-gray-600">Passengers:</span>
                    <span className="font-semibold ml-2">{route.passengers}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <Zap className="w-5 h-5 mr-2 text-purple-600" />
            AI Optimization Engine
          </h3>
          <div className="space-y-4">
            <div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-4 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="font-semibold text-gray-700">Algorithm Stack</span>
                <span className="text-xs bg-green-500 text-white px-2 py-1 rounded">LEVEL-4</span>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  <span>K-Means Clustering (Pickup Discovery)</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  <span>Genetic Algorithm (Route Encoding)</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  <span>NSGA-II (Multi-Objective)</span>
                </div>
                <div className="flex items-center">
                  <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                  <span>Memetic Search (Local Optimization)</span>
                </div>
              </div>
            </div>

            <button
              onClick={runOptimization}
              disabled={optimizationRunning}
              className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition disabled:opacity-50"
            >
              {optimizationRunning ? 'Running Optimization...' : 'Run New Optimization'}
            </button>

            {optimizationRunning && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm text-gray-600">
                  <span>Progress</span>
                  <span>{optimizationProgress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-gradient-to-r from-indigo-500 to-purple-500 h-3 rounded-full transition-all duration-500"
                    style={{ width: `${optimizationProgress}%` }}
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const PickupPointsView = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <MapPin className="w-5 h-5 mr-2 text-indigo-600" />
          K-Means Cluster Analysis
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {pickupPoints.map(point => (
            <div key={point.id} className={`border-2 rounded-lg p-4 ${point.status === 'active' ? 'border-green-400 bg-green-50' : 'border-gray-300 bg-gray-50'}`}>
              <div className="flex justify-between items-start mb-3">
                <div>
                  <h4 className="font-bold text-gray-800">{point.name}</h4>
                  <p className="text-xs text-gray-500">Cluster #{point.cluster}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-semibold ${point.status === 'active' ? 'bg-green-500 text-white' : 'bg-gray-400 text-white'}`}>
                  {point.status.toUpperCase()}
                </span>
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Registered Users:</span>
                  <span className="font-bold">{point.users}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Coordinates:</span>
                  <span className="font-mono text-xs">{point.lat.toFixed(4)}, {point.lon.toFixed(4)}</span>
                </div>
              </div>
              <div className="mt-3 pt-3 border-t">
                <div className="text-xs text-gray-500">
                  {point.users >= 10 ? '✓ Threshold met (≥10 users)' : '✗ Below threshold (<10 users)'}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl shadow-lg p-6">
        <h4 className="font-bold text-gray-800 mb-4">Clustering Logic</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="bg-white p-4 rounded-lg">
            <div className="font-semibold text-indigo-600 mb-2">1. Input</div>
            <p className="text-gray-600">1000+ user GPS locations</p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <div className="font-semibold text-purple-600 mb-2">2. Process</div>
            <p className="text-gray-600">K-Means groups nearby users</p>
          </div>
          <div className="bg-white p-4 rounded-lg">
            <div className="font-semibold text-green-600 mb-2">3. Output</div>
            <p className="text-gray-600">Active pickup points (≥10 users)</p>
          </div>
        </div>
      </div>
    </div>
  );

  const ChromosomeView = () => (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
          <Zap className="w-5 h-5 mr-2 text-purple-600" />
          Level-4 Chromosome Structure
        </h3>
        
        <div className="bg-gradient-to-r from-purple-100 to-indigo-100 p-6 rounded-lg mb-6">
          <div className="font-mono text-sm mb-2 text-gray-700">
            [Pickup Status | Visit Order | Priority | Load]
          </div>
          <div className="font-mono text-lg font-bold text-indigo-700">
            [2,1,0,2,1 | 3,0,4,1 | 3,2,1,2 | 12,8,6,5]
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="border-l-4 border-blue-500 bg-blue-50 p-4 rounded-r-lg">
            <h4 className="font-bold text-blue-700 mb-2">Pickup Status</h4>
            <div className="space-y-1 text-sm">
              <div><span className="font-mono bg-gray-200 px-2 py-1 rounded">0</span> = Skip</div>
              <div><span className="font-mono bg-gray-200 px-2 py-1 rounded">1</span> = Normal demand</div>
              <div><span className="font-mono bg-gray-200 px-2 py-1 rounded">2</span> = High demand</div>
            </div>
          </div>

          <div className="border-l-4 border-green-500 bg-green-50 p-4 rounded-r-lg">
            <h4 className="font-bold text-green-700 mb-2">Visit Order</h4>
            <div className="text-sm">
              <p>Sequence in which pickups are visited</p>
              <p className="mt-2 font-mono bg-gray-200 px-2 py-1 rounded inline">3,0,4,1</p>
              <p className="mt-1 text-xs">= Visit pickup 3 → 0 → 4 → 1</p>
            </div>
          </div>

          <div className="border-l-4 border-yellow-500 bg-yellow-50 p-4 rounded-r-lg">
            <h4 className="font-bold text-yellow-700 mb-2">Priority</h4>
            <div className="text-sm">
              <p>Time importance level (1-3)</p>
              <p className="mt-2">Higher = More time-sensitive</p>
            </div>
          </div>

          <div className="border-l-4 border-purple-500 bg-purple-50 p-4 rounded-r-lg">
            <h4 className="font-bold text-purple-700 mb-2">Load</h4>
            <div className="text-sm">
              <p>Passenger count at each pickup</p>
              <p className="mt-2">Used for capacity constraints</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Fitness Functions</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-red-50 to-orange-50 p-4 rounded-lg">
            <Clock className="w-8 h-8 text-orange-600 mb-2" />
            <h4 className="font-bold text-gray-800 mb-2">Minimize Time</h4>
            <p className="text-sm text-gray-600">Travel time + dwell time at stops</p>
          </div>
          <div className="bg-gradient-to-br from-green-50 to-emerald-50 p-4 rounded-lg">
            <DollarSign className="w-8 h-8 text-green-600 mb-2" />
            <h4 className="font-bold text-gray-800 mb-2">Minimize Cost</h4>
            <p className="text-sm text-gray-600">Fuel + driver wages + distance</p>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 p-4 rounded-lg">
            <TrendingUp className="w-8 h-8 text-indigo-600 mb-2" />
            <h4 className="font-bold text-gray-800 mb-2">Maximize Reliability</h4>
            <p className="text-sm text-gray-600">Time windows + capacity adherence</p>
          </div>
        </div>
      </div>
    </div>
  );

  const StudentView = () => (
    <div className="space-y-6">
      <div className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white rounded-xl shadow-lg p-6">
        <h2 className="text-2xl font-bold mb-2">Welcome, Student!</h2>
        <p className="text-blue-100">Register your location and view your assigned shuttle</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Registration</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Your Location</label>
              <input
                type="text"
                placeholder="Enter your address"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Preferred Time</label>
              <input
                type="time"
                defaultValue="07:45"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>
            <button className="w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition">
              Register Location
            </button>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Your Assignment</h3>
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center mb-2">
                <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
                <span className="font-semibold text-green-800">Assigned Pickup Point</span>
              </div>
              <p className="text-gray-700 font-bold text-lg">Bambalapitiya Junction</p>
              <p className="text-sm text-gray-600 mt-1">Cluster #2 • 32 users</p>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Route:</span>
                <span className="font-bold text-indigo-600">Route B</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Estimated Arrival:</span>
                <span className="font-bold">07:52 AM</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Journey Time:</span>
                <span className="font-bold">45 minutes</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t">
              <button className="w-full bg-indigo-100 text-indigo-700 py-2 rounded-lg font-medium hover:bg-indigo-200 transition">
                <Navigation className="w-4 h-4 inline mr-2" />
                Get Directions
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const StatCard = ({ icon, title, value, color, trend }) => (
    <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition">
      <div className="flex justify-between items-start mb-4">
        <div className={`p-3 rounded-lg bg-${color}-100`}>
          {React.cloneElement(icon, { className: `w-6 h-6 text-${color}-600` })}
        </div>
        {trend && (
          <span className="text-sm font-semibold text-green-600">
            {trend}
          </span>
        )}
      </div>
      <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
      <p className="text-2xl font-bold text-gray-800 mt-1">{value}</p>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <NavigationBar />
      
      <div className="max-w-7xl mx-auto px-6 py-8">
        {activeRole === 'admin' && (
          <>
            <div className="mb-6 bg-white rounded-lg shadow p-4">
              <div className="flex space-x-2">
                <button
                  onClick={() => setActivePage('dashboard')}
                  className={`px-4 py-2 rounded-lg transition ${activePage === 'dashboard' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                >
                  Dashboard
                </button>
                <button
                  onClick={() => setActivePage('pickups')}
                  className={`px-4 py-2 rounded-lg transition ${activePage === 'pickups' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                >
                  Pickup Points
                </button>
                <button
                  onClick={() => setActivePage('chromosome')}
                  className={`px-4 py-2 rounded-lg transition ${activePage === 'chromosome' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
                >
                  AI Engine
                </button>
              </div>
            </div>

            {activePage === 'dashboard' && <DashboardView />}
            {activePage === 'pickups' && <PickupPointsView />}
            {activePage === 'chromosome' && <ChromosomeView />}
          </>
        )}

        {activeRole === 'student' && <StudentView />}

        {activeRole === 'system' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">System Architecture</h2>
              <div className="space-y-4">
                <div className="flex items-center space-x-4 bg-gray-50 p-4 rounded-lg">
                  <div className="bg-indigo-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">1</div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800">Registration</div>
                    <div className="text-sm text-gray-600">User provides GPS location, time preference</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 bg-gray-50 p-4 rounded-lg">
                  <div className="bg-indigo-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">2</div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800">K-Means Clustering</div>
                    <div className="text-sm text-gray-600">Discover optimal pickup points from user locations</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 bg-gray-50 p-4 rounded-lg">
                  <div className="bg-indigo-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">3</div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800">Genetic Algorithm</div>
                    <div className="text-sm text-gray-600">Encode routes using Level-4 chromosome structure</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 bg-gray-50 p-4 rounded-lg">
                  <div className="bg-indigo-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">4</div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800">NSGA-II Optimization</div>
                    <div className="text-sm text-gray-600">Multi-objective optimization (Time vs Cost)</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 bg-gray-50 p-4 rounded-lg">
                  <div className="bg-indigo-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">5</div>
                  <div className="flex-1">
                    <div className="font-bold text-gray-800">Memetic Improvement</div>
                    <div className="text-sm text-gray-600">Local optimization using 2-Opt algorithm</div>
                  </div>
                </div>
                <div className="flex items-center space-x-4 bg-green-50 p-4 rounded-lg border-2 border-green-500">
                  <div className="bg-green-600 text-white w-8 h-8 rounded-full flex items-center justify-center font-bold">✓</div>
                  <div className="flex-1">
                    <div className="font-bold text-green-800">Output</div>
                    <div className="text-sm text-green-700">Optimized routes, schedules, and assignments</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;