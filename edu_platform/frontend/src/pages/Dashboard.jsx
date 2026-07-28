import React, { useContext } from 'react';
import { Users, CheckCircle, Activity, Award, TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AuthContext } from '../context/AuthContext';
import './Dashboard.css';

const data = [
  { name: 'MAY', value: 100 },
  { name: 'JUN', value: 160 },
  { name: 'JUL', value: 180 },
  { name: 'AUG', value: 200 },
  { name: 'SEP', value: 250 },
  { name: 'OCT', value: 280 },
  { name: 'NOV', value: 310 },
  { name: 'DEC', value: 380 },
];

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const isTeacher = user?.role === 'teacher';

  return (
    <div className="dashboard-container">
      
      {/* Top Metrics Row */}
      <div className="metrics-grid">
        <div className="metric-card card">
          <div className="metric-header">
            <div className="icon-wrapper orange-light">
              <Users size={20} className="icon-orange" />
            </div>
            <div className="metric-value">342</div>
          </div>
          <div className="metric-label">{isTeacher ? "My Students" : "Employees"}</div>
        </div>
        
        <div className="metric-card card">
          <div className="metric-header">
            <div className="icon-wrapper orange-light">
              <CheckCircle size={20} className="icon-orange" />
            </div>
            <div className="metric-value">238</div>
          </div>
          <div className="metric-label">Completed</div>
        </div>
        
        <div className="metric-card card">
          <div className="metric-header">
            <div className="icon-wrapper orange-light">
              <Activity size={20} className="icon-orange" />
            </div>
            <div className="metric-value">91<span className="percent">%</span></div>
          </div>
          <div className="metric-label">Active</div>
        </div>
        
        <div className="metric-card card">
          <div className="metric-header">
            <div className="icon-wrapper orange-light">
              <Award size={20} className="icon-orange" />
            </div>
            <div className="metric-value">198</div>
          </div>
          <div className="metric-label">Certificates</div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="dashboard-content">
        
        {/* Left Side - Chart */}
        <div className="chart-section card">
          <div className="chart-header">
            <div>
              <h3>Monthly activity</h3>
              <div className="chart-subtitle">
                <span className="dot orange-dot"></span> Tech Onboarding - 2026
              </div>
            </div>
            <div className="icon-wrapper-small orange-light">
              <TrendingUp size={16} className="icon-orange" />
            </div>
          </div>
          
          <div className="chart-body">
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={data} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f97316" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f97316" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#9ca3af', fontSize: 12}} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#9ca3af', fontSize: 12}} dx={-10} />
                <Tooltip />
                <Area type="monotone" dataKey="value" stroke="#f97316" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right Side - Panels */}
        <div className="right-panels">
          
          <div className="panel-card card">
            <h4>Completion status</h4>
            <div className="status-labels">
              <span style={{color: '#9ca3af'}}>Not started: ...</span>
              <span style={{color: '#3b82f6'}}>In progress: 42%</span>
              <span style={{color: '#10b981'}}>Completed: 44%</span>
            </div>
            <div className="progress-bar-container">
              <div className="progress-segment" style={{width: '14%', backgroundColor: '#f3f4f6'}}></div>
              <div className="progress-segment" style={{width: '42%', backgroundColor: '#bfdbfe'}}></div>
              <div className="progress-segment" style={{width: '44%', backgroundColor: '#bbf7d0'}}></div>
            </div>
          </div>

          <div className="panel-card card">
            <h4>Assignment sources</h4>
            <div className="status-labels center-labels">
              <span style={{color: '#f97316'}}>HR</span>
              <span style={{color: '#10b981'}}>Manager</span>
              <span style={{color: '#8b5cf6'}}>Self</span>
              <span style={{color: '#9ca3af'}}>Auto</span>
            </div>
            <div className="progress-bar-container gap-bar">
              <div className="progress-segment" style={{width: '20%', backgroundColor: '#ffedd5'}}></div>
              <div className="progress-segment" style={{width: '40%', backgroundColor: '#d1fae5'}}></div>
              <div className="progress-segment" style={{width: '25%', backgroundColor: '#ede9fe'}}></div>
              <div className="progress-segment" style={{width: '15%', backgroundColor: '#f3f4f6'}}></div>
            </div>
          </div>

          <div className="panel-card card">
            <h4>{isTeacher ? "Student levels" : "Employee levels"}</h4>
            <div className="status-labels space-between">
              <span style={{color: '#6b7280'}}>Junior: 35%</span>
              <span style={{color: '#10b981'}}>Middle: 35%</span>
              <span style={{color: '#3b82f6'}}>Senior: 20%</span>
              <span style={{color: '#f97316'}}>Lead</span>
            </div>
            <div className="progress-bar-container gap-bar">
              <div className="progress-segment" style={{width: '35%', backgroundColor: '#e5e7eb'}}></div>
              <div className="progress-segment" style={{width: '35%', backgroundColor: '#d1fae5'}}></div>
              <div className="progress-segment" style={{width: '20%', backgroundColor: '#dbeafe'}}></div>
              <div className="progress-segment" style={{width: '10%', backgroundColor: '#ffedd5'}}></div>
            </div>
          </div>

          <div className="panel-card card top-courses">
            <h4>Top courses</h4>
            <div className="course-list">
              <div className="course-item">
                <span className="course-num">1.</span>
                <div className="course-bar-wrapper">
                  <span className="course-name">Git & CI/CD</span>
                  <div className="course-bar" style={{width: '100%', backgroundColor: '#ffedd5'}}></div>
                </div>
                <span className="course-val">312</span>
              </div>
              <div className="course-item">
                <span className="course-num">2.</span>
                <div className="course-bar-wrapper">
                  <span className="course-name">Service architecture</span>
                  <div className="course-bar" style={{width: '90%', backgroundColor: '#ffedd5'}}></div>
                </div>
                <span className="course-val">298</span>
              </div>
              <div className="course-item">
                <span className="course-num">3.</span>
                <div className="course-bar-wrapper">
                  <span className="course-name">Code Review</span>
                  <div className="course-bar" style={{width: '80%', backgroundColor: '#ffedd5'}}></div>
                </div>
                <span className="course-val">284</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;
