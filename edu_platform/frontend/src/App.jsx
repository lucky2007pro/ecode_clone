import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, AuthContext } from './context/AuthContext';
import { useContext } from 'react';

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem('token');
  
  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const RoleRoute = ({ children, deniedRoles = [] }) => {
  const { user } = useContext(AuthContext);
  
  if (user && deniedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }
  return children;
};

import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Students from './pages/admin/Students';
import Courses from './pages/admin/Courses';
import CourseBuilder from './pages/admin/CourseBuilder';
import HomeworkReview from './pages/admin/HomeworkReview';
import AnalyticsDashboard from './pages/admin/AnalyticsDashboard';
import StudentDashboard from './pages/student/StudentDashboard';
import CourseView from './pages/student/CourseView';
import Chat from './pages/student/Chat';
import Settings from './pages/admin/Settings';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Full-screen routes without sidebar */}
          <Route path="/courses/:id" element={<CourseView />} />

          <Route path="/*" element={
            <ProtectedRoute>
              <div className="app-container">
              <Sidebar />
              <div className="main-content">
                <Header />
                <main className="page-content">
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/analytics" element={<AnalyticsDashboard />} />
                    <Route path="/chat" element={<Chat />} />
                    <Route path="/students" element={<Students />} />
                    <Route path="/courses" element={<Courses />} />
                    <Route path="/admin/courses/:id/builder" element={<CourseBuilder />} />
                    <Route path="/admin/homeworks" element={<HomeworkReview />} />
                    <Route path="/student-dashboard" element={<StudentDashboard />} />
                    <Route path="/settings" element={<RoleRoute deniedRoles={['teacher']}><Settings /></RoleRoute>} />
                    
                    {/* Qolgan yo'nalishlar */}
                    <Route path="/videos" element={<div className="card"><h2>Videolar sahifasi</h2><p>Tez orada...</p></div>} />
                    <Route path="/payments" element={<RoleRoute deniedRoles={['teacher']}><div className="card"><h2>To'lovlar sahifasi</h2><p>Tez orada...</p></div></RoleRoute>} />
                    <Route path="/notifications" element={<div className="card"><h2>Bildirishnomalar</h2><p>Tez orada...</p></div>} />
                  </Routes>
                </main>
                </div>
              </div>
            </ProtectedRoute>
          } />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;

