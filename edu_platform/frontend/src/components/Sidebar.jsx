import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Layers, CreditCard, CheckSquare, Users, Settings, Sparkles } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
  const { user } = useContext(AuthContext);

  const menuItems = [
    { name: 'Home', icon: <Home size={22} />, path: user?.role === 'student' ? '/student-dashboard' : '/' },
    { name: 'Courses', icon: <Layers size={22} />, path: '/courses' },
  ];

  if (user && user.role !== 'student') {
    menuItems.push({ name: 'Practice', icon: <CheckSquare size={22} />, path: '/admin/homeworks' });
    menuItems.push({ name: 'People', icon: <Users size={22} />, path: '/students' });
  }

  // Admin, Manager va Buxgalter ko'ra oladigan qismlar
  if (user && (user.role === 'admin' || user.role === 'manager' || user.role === 'accountant')) {
    menuItems.push({ name: 'Sales', icon: <CreditCard size={22} />, path: '/payments' });
  }
  
  if (user && user.role === 'admin') {
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
