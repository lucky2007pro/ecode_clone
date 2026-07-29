import React, { useContext, useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Bell, UserCircle, Settings, User, CreditCard, LogOut, ChevronDown } from 'lucide-react';
import { AuthContext } from '../context/auth-context';
import { timeAgo } from '../utils/timeAgo';
import { api } from '../api';
import './Header.css';

const Header = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [showNotifications, setShowNotifications] = useState(false);
  const [showProfileMenu, setShowProfileMenu] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const [notifications, setNotifications] = useState([]);
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

  useEffect(() => {
    let cancelled = false;
    const fetchNotifications = async () => {
      try {
        const data = await api('/notifications/');
        if (!cancelled) {
          setUnreadCount(data.unread_count);
          setNotifications(data.results);
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchNotifications();
    const interval = setInterval(fetchNotifications, 30000);
    return () => { cancelled = true; clearInterval(interval); };
  }, []);

  const handleReadAll = async () => {
    try {
      await api('/notifications/read-all', { method: 'POST' });
      setUnreadCount(0);
      setNotifications(notifications.map(n => ({ ...n, is_read: true })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenNotification = async (notification) => {
    if (!notification.is_read) {
      try {
        await api(`/notifications/${notification.id}/read`, { method: 'POST' });
        setUnreadCount(Math.max(unreadCount - 1, 0));
        setNotifications(notifications.map(n => n.id === notification.id ? { ...n, is_read: true } : n));
      } catch (err) {
        console.error(err);
      }
    }
    setShowNotifications(false);
    navigate('/notifications');
  };

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
            {unreadCount > 0 && <span className="badge">{unreadCount > 99 ? '99+' : unreadCount}</span>}
          </button>

          {showNotifications && (
            <div className="notifications-dropdown card">
              <h4>Bildirishnomalar</h4>
              {notifications.length === 0 && (
                <p style={{ padding: '10px', color: '#9ca3af', fontSize: '13px' }}>Hozircha bildirishnomalar yo'q</p>
              )}
              {notifications.slice(0, 5).map(notification => (
                <div
                  key={notification.id}
                  className={`notification-item ${notification.is_read ? '' : 'unread'}`}
                  onClick={() => handleOpenNotification(notification)}
                >
                  {notification.title}
                  <span className="time">{timeAgo(notification.created_at)}</span>
                </div>
              ))}
              {unreadCount > 0 && (
                <button className="notif-read-all" onClick={handleReadAll}>
                  Hammasini o'qilgan deb belgilash
                </button>
              )}
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
              <div className="profile-dropdown-item" onClick={() => { setShowProfileMenu(false); navigate('/settings'); }}>
                <div className="profile-dropdown-icon text-blue">
                  <User size={20} />
                </div>
                <div className="profile-dropdown-text">
                  <h5>Shaxsiy Profil</h5>
                  <p>Ma'lumotlaringizni tahrirlash</p>
                </div>
              </div>

              <div className="profile-dropdown-item" onClick={() => { setShowProfileMenu(false); navigate('/settings'); }}>
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
