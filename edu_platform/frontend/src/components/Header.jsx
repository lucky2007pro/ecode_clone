import React, { useContext, useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Bell, UserCircle, Settings, User, CreditCard, LogOut, ChevronDown } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import './Header.css';

const Header = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const profileMenuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setShowProfileMenu(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className="header">
      <div className="header-search">
        <Search size={20} className="search-icon" />
        <input type="text" placeholder="Qidirish..." />
      </div>

      <div className="header-actions">
        <div className="notification-wrapper">
          <button 
            className="icon-btn" 
            onClick={() => setShowNotifications(!showNotifications)}
          >
            <Bell size={20} />
            <span className="badge">3</span>
          </button>
          
          {showNotifications && (
            <div className="notifications-dropdown card">
              <h4>Bildirishnomalar</h4>
              <div className="notification-item">
                <p><strong>Yangi o'quvchi</strong> ro'yxatdan o'tdi</p>
                <span className="time">2 daqiqa oldin</span>
              </div>
              <div className="notification-item">
                <p><strong>Uy vazifasi</strong> yuborildi</p>
                <span className="time">1 soat oldin</span>
              </div>
            </div>
          )}
        </div>

        <div className="user-profile-wrapper" ref={profileMenuRef}>
          <div className="user-profile" onClick={() => setShowProfileMenu(!showProfileMenu)}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', marginRight: '10px' }}>
              {user && (user.role === 'admin' || user.role === 'student') && (
                <span style={{ fontSize: '12px', fontWeight: 'bold', color: '#10b981', background: '#d1fae5', padding: '2px 6px', borderRadius: '4px' }}>
                  {user.balance?.toLocaleString()} UZS
                </span>
              )}
            </div>
            <UserCircle size={32} color="#9ca3af" />
            <div className="user-info">
              <span className="user-name">{user ? user.full_name : 'Foydalanuvchi'}</span>
              <span className="user-role" style={{ textTransform: 'capitalize' }}>{user ? user.role : 'Mehmon'}</span>
            </div>
            <ChevronDown size={16} className={`profile-chevron ${showProfileMenu ? 'open' : ''}`} />
          </div>

          {showProfileMenu && (
            <div className="profile-dropdown card">
              <div className="profile-dropdown-item" onClick={() => { setShowProfileMenu(false); alert("Profil sahifasi") }}>
                <div className="profile-dropdown-icon text-blue">
                  <User size={20} />
                </div>
                <div className="profile-dropdown-text">
                  <h5>Shaxsiy Profil</h5>
                  <p>Ma'lumotlaringizni tahrirlash</p>
                </div>
              </div>
              
              <div className="profile-dropdown-item" onClick={() => { setShowProfileMenu(false); alert("Sozlamalar") }}>
                <div className="profile-dropdown-icon text-orange">
                  <Settings size={20} />
                </div>
                <div className="profile-dropdown-text">
                  <h5>Sozlamalar</h5>
                  <p>Platformaning barcha sozlamalari</p>
                </div>
              </div>

              {user && (user.role === 'admin' || user.role === 'student') && (
                <div className="profile-dropdown-item" onClick={() => { 
                  setShowProfileMenu(false); 
                  if (user.role === 'admin') {
                    navigate("/settings");
                  } else if (user.role === 'student') {
                    navigate("/courses");
                  }
                }}>
                  <div className="profile-dropdown-icon text-green">
                    <CreditCard size={20} />
                  </div>
                  <div className="profile-dropdown-text">
                    <h5>To'lov va obunalar</h5>
                    <p>Tariflar va hisob-kitoblar</p>
                  </div>
                </div>
              )}

              <div className="profile-dropdown-divider"></div>

              <div className="profile-dropdown-item logout-item" onClick={() => { setShowProfileMenu(false); logout(); }}>
                <div className="profile-dropdown-icon text-red">
                  <LogOut size={20} />
                </div>
                <div className="profile-dropdown-text">
                  <h5>Tizimdan chiqish</h5>
                  <p>Hisobdan xavfsiz chiqib ketish</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
