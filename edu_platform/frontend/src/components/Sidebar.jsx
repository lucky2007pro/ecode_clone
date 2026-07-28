import React, { useContext } from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Layers, CreditCard, CheckSquare, Users, Settings, Sparkles } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
  const { user } = useContext(AuthContext);

  const menuItems = [
    { name: 'Home', icon: <Home size={22} />, path: '/' },
    { name: 'Courses', icon: <Layers size={22} />, path: '/courses' },
    { name: 'Practice', icon: <CheckSquare size={22} />, path: '/admin/homeworks' },
    { name: 'People', icon: <Users size={22} />, path: '/students' },
  ];

  // Admin and Manager ko'ra oladigan qismlar
  if (user && (user.role === 'admin' || user.role === 'manager')) {
    menuItems.splice(2, 0, { name: 'Sales', icon: <CreditCard size={22} />, path: '/payments' });
    menuItems.push({ name: 'My school', icon: <Settings size={22} />, path: '/settings' });
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
