import React, { useContext, useEffect, useState } from 'react';
import { Users, CheckCircle, Activity, TrendingUp } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { AuthContext } from '../context/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const isTeacher = user?.role === 'teacher';
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return;
    fetch('http://localhost:8000/api/v1/analytics/dashboard', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.ok ? response.json() : Promise.reject())
      .then(setAnalytics)
      .catch(() => setAnalytics(null));
  }, []);

  const metrics = analytics?.metrics || {};
  const completion = analytics?.completion_status || { not_started: 0, in_progress: 0, completed: 0 };
  const data = analytics?.monthly_activity || [];
  const maxCourseValue = Math.max(...(analytics?.top_courses || []).map((course) => course.value), 1);

  return (
    <div className="dashboard-container">
      
      {/* Top Metrics Row */}
      <div className="metrics-grid">
        <div className="metric-card card">
          <div className="metric-header">
            <div className="icon-wrapper orange-light">
              <Users size={20} className="icon-orange" />
            </div>
            <div className="metric-value">{metrics.people_count ?? 0}</div>
          </div>
          <div className="metric-label">{isTeacher ? "My Students" : "Employees"}</div>
        </div>
        
        <div className="metric-card card">
          <div className="metric-header">
            <div className="icon-wrapper orange-light">
              <CheckCircle size={20} className="icon-orange" />
            </div>
            <div className="metric-value">{metrics.completed_count ?? 0}</div>
          </div>
          <div className="metric-label">Completed</div>
        </div>
        
        <div className="metric-card card">
          <div className="metric-header">
            <div className="icon-wrapper orange-light">
              <Activity size={20} className="icon-orange" />
            </div>
            <div className="metric-value">{metrics.active_percent ?? 0}<span className="percent">%</span></div>
          </div>
          <div className="metric-label">Active</div>
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
              <span style={{color: '#9ca3af'}}>Not started: {completion.not_started}%</span>
              <span style={{color: '#3b82f6'}}>In progress: {completion.in_progress}%</span>
              <span style={{color: '#10b981'}}>Completed: {completion.completed}%</span>
            </div>
            <div className="progress-bar-container">
              <div className="progress-segment" style={{width: `${completion.not_started}%`, backgroundColor: '#f3f4f6'}}></div>
              <div className="progress-segment" style={{width: `${completion.in_progress}%`, backgroundColor: '#bfdbfe'}}></div>
              <div className="progress-segment" style={{width: `${completion.completed}%`, backgroundColor: '#bbf7d0'}}></div>
            </div>
          </div>

          <div className="panel-card card">
            <h4>Assignment sources</h4>
            <div className="status-labels center-labels">
              {(analytics?.assignment_sources || []).map((source) => <span key={source.name}>{source.name}: {source.value}</span>)}
            </div>
            <div className="progress-bar-container gap-bar">
              {(analytics?.assignment_sources || []).map((source) => <div key={source.name} className="progress-segment" style={{width: `${source.value * 100 / Math.max((analytics.assignment_sources || []).reduce((sum, item) => sum + item.value, 0), 1)}%`, backgroundColor: '#ffedd5'}}></div>)}
            </div>
          </div>

          <div className="panel-card card">
            <h4>{isTeacher ? "Student levels" : "Employee levels"}</h4>
            <div className="status-labels space-between">
              {(analytics?.employee_levels || []).map((level) => <span key={level.name}>{level.name}: {level.value}</span>)}
            </div>
            <div className="progress-bar-container gap-bar">
              {(analytics?.employee_levels || []).map((level) => <div key={level.name} className="progress-segment" style={{width: `${level.value * 100 / Math.max((analytics.employee_levels || []).reduce((sum, item) => sum + item.value, 0), 1)}%`, backgroundColor: '#dbeafe'}}></div>)}
            </div>
          </div>

          <div className="panel-card card top-courses">
            <h4>Top courses</h4>
            <div className="course-list">
              {(analytics?.top_courses || []).map((course, index) => <div className="course-item" key={course.id}>
                <span className="course-num">{index + 1}.</span>
                <div className="course-bar-wrapper">
                  <span className="course-name">{course.name}</span>
                  <div className="course-bar" style={{width: `${course.value * 100 / maxCourseValue}%`, backgroundColor: '#ffedd5'}}></div>
                </div>
                <span className="course-val">{course.value}</span>
              </div>)}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default Dashboard;
