import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { AuthContext } from './context/auth-context';
import { useContext } from 'react';

const ProtectedRoute = ({ children }) => {
  const { user } = useContext(AuthContext);
  const token = localStorage.getItem('token');

  if (!token || !user) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const ROLE_HOME = {
  student: '/student-dashboard',
  accountant: '/payments',
  admin: '/dashboard',
  manager: '/dashboard',
  teacher: '/dashboard',
  curator: '/dashboard',
};

const RoleRoute = ({ children, allowedRoles }) => {
  const { user } = useContext(AuthContext);

  if (user && allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to={ROLE_HOME[user.role] || '/dashboard'} replace />;
  }
  return children;
};

import Landing from './pages/Landing';
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
import Payments from './pages/admin/Payments';
import NotificationsPage from './pages/NotificationsPage';

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {}
          <Route path="/courses/:id" element={<ProtectedRoute><RoleRoute allowedRoles={['student', 'curator', 'teacher', 'manager', 'admin']}><CourseView /></RoleRoute></ProtectedRoute>} />

          <Route path="/*" element={
            <ProtectedRoute>
              <div className="app-container">
              <Sidebar />
              <div className="main-content">
                <Header />
                <main className="page-content">
                  <Routes>
                    <Route path="/dashboard" element={<RoleRoute allowedRoles={['admin', 'accountant', 'curator', 'teacher', 'manager']}><Dashboard /></RoleRoute>} />
                    <Route path="/analytics" element={<RoleRoute allowedRoles={['admin']}><AnalyticsDashboard /></RoleRoute>} />
                    <Route path="/chat" element={<RoleRoute allowedRoles={['admin']}><Chat /></RoleRoute>} />
                    <Route path="/students" element={<RoleRoute allowedRoles={['curator', 'teacher', 'manager', 'admin']}><Students /></RoleRoute>} />
                    <Route path="/courses" element={<RoleRoute allowedRoles={['student', 'curator', 'teacher', 'manager', 'admin']}><Courses /></RoleRoute>} />
                    <Route path="/admin/courses/:id/builder" element={<RoleRoute allowedRoles={['teacher', 'manager', 'admin']}><CourseBuilder /></RoleRoute>} />
                    <Route path="/admin/homeworks" element={<RoleRoute allowedRoles={['curator', 'teacher', 'manager', 'admin']}><HomeworkReview /></RoleRoute>} />
                    <Route path="/student-dashboard" element={<RoleRoute allowedRoles={['student']}><StudentDashboard /></RoleRoute>} />
                    <Route path="/settings" element={<RoleRoute allowedRoles={['admin']}><Settings /></RoleRoute>} />

                    {}
                    <Route path="/videos" element={<RoleRoute allowedRoles={['admin']}><div className="card"><h2>Videolar sahifasi</h2><p>Tez orada...</p></div></RoleRoute>} />
                    <Route path="/payments" element={<RoleRoute allowedRoles={['admin', 'accountant']}><Payments /></RoleRoute>} />
                    <Route path="/notifications" element={<RoleRoute allowedRoles={['student', 'accountant', 'curator', 'teacher', 'manager', 'admin']}><NotificationsPage /></RoleRoute>} />
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
