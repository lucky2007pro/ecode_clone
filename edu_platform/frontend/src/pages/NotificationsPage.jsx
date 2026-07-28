import React, { useState, useEffect } from 'react';
import { BellOff, CheckCheck } from 'lucide-react';
import { api } from '../api';
import { timeAgo } from '../components/Header';
import './NotificationsPage.css';

const NotificationsPage = () => {
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const data = await api('/notifications/');
      setNotifications(data.results);
      setUnreadCount(data.unread_count);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleReadAll = async () => {
    try {
      await api('/notifications/read-all', { method: 'POST' });
      setUnreadCount(0);
      setNotifications(notifications.map(n => ({ ...n, is_read: true })));
    } catch (err) {
      console.error(err);
    }
  };

  const handleRead = async (notification) => {
    if (notification.is_read) return;
    try {
      await api(`/notifications/${notification.id}/read`, { method: 'POST' });
      setUnreadCount(Math.max(unreadCount - 1, 0));
      setNotifications(notifications.map(n => n.id === notification.id ? { ...n, is_read: true } : n));
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) return <div className="p-8 text-center">Yuklanmoqda...</div>;

  return (
    <div className="notifications-page">
      <div className="notifications-page-header">
        <h1>Bildirishnomalar</h1>
        {unreadCount > 0 && (
          <button className="btn-primary" onClick={handleReadAll}>
            <CheckCheck size={18} /> Hammasini o'qilgan deb belgilash
          </button>
        )}
      </div>

      {notifications.length === 0 ? (
        <div className="card text-center p-8">
          <BellOff size={48} className="icon-muted mx-auto mb-4" />
          <h3>Hozircha bildirishnomalar yo'q</h3>
        </div>
      ) : (
        <div className="notifications-list">
          {notifications.map(notification => (
            <div
              key={notification.id}
              className={`notification-row card ${notification.is_read ? '' : 'unread'}`}
              onClick={() => handleRead(notification)}
            >
              <div className="notification-row-text">
                <h4>{notification.title}</h4>
                {notification.body && <p className="text-muted">{notification.body}</p>}
              </div>
              <span className="time">{timeAgo(notification.created_at)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default NotificationsPage;
