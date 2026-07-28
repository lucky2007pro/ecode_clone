import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Layers, CreditCard, CheckSquare, Users, Settings, Sparkles, Bell } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
  const { user } = useContext(AuthContext);

  const role = user?.role;
  const menuItems = [
    { name: 'Home', icon: <Home size={22} />, path: role === 'student' ? '/student-dashboard' : '/' },
    { name: 'Bildirishnomalar', icon: <Bell size={22} />, path: '/notifications' },
  ];

  if (['student', 'curator', 'teacher', 'manager', 'admin'].includes(role)) {
    menuItems.push({ name: 'Courses', icon: <Layers size={22} />, path: '/courses' });
  }
  if (['curator', 'teacher', 'manager', 'admin'].includes(role)) {
    menuItems.push({ name: 'Practice', icon: <CheckSquare size={22} />, path: '/admin/homeworks' });
    menuItems.push({ name: 'People', icon: <Users size={22} />, path: '/students' });
  }
  if (['accountant', 'admin'].includes(role)) {
    menuItems.push({ name: 'Sales', icon: <CreditCard size={22} />, path: '/payments' });
  }
  if (role === 'admin') {
    menuItems.push({ name: 'Settings', icon: <Settings size={22} />, path: '/settings' });
  }

  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">
          <Sparkles size={24} color="#fff" />
        </div>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink 
            to={item.path} 
            key={item.name}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <div className="nav-icon">{item.icon}</div>
            <span className="nav-text">{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
};

export default Sidebar;
