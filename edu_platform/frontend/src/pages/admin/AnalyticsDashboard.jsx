import React, { useState, useEffect } from 'react';
import { TrendingUp, Users, CheckCircle, BookOpen } from 'lucide-react';
import { api } from '../../api';
import './AnalyticsDashboard.css';

const AnalyticsDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const json = await api('/analytics/dashboard');
      setData(json);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center">Yuklanmoqda...</div>;
  if (!data) return <div className="p-8 text-center text-danger">Ma'lumot topilmadi</div>;

  const metrics = data.metrics || {};
  const months = data.monthly_activity || [];
  const completion = data.completion_status || { not_started: 0, in_progress: 0, completed: 0 };
  const topCourses = data.top_courses || [];
  // Bo'sh ma'lumotda -Infinity bo'lmasligi uchun minimal qiymat 1
  const maxValue = Math.max(...months.map(m => m.value), 1);

  return (
    <div className="analytics-dashboard">
      <div className="analytics-header">
        <h1>Analitika va Hisobotlar</h1>
        <p>Maktabingizning asosiy ko'rsatkichlari</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card card">
          <div className="stat-icon users"><Users size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">O'quvchilar</p>
            <h3 className="stat-value">{metrics.people_count ?? 0} ta</h3>
          </div>
        </div>

        <div className="stat-card card">
          <div className="stat-icon success"><CheckCircle size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">Tugatganlar</p>
            <h3 className="stat-value">{metrics.completed_count ?? 0} ta</h3>
          </div>
        </div>

        <div className="stat-card card">
          <div className="stat-icon income"><TrendingUp size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">Faollik</p>
            <h3 className="stat-value">{metrics.active_percent ?? 0}%</h3>
          </div>
        </div>

        <div className="stat-card card">
          <div className="stat-icon courses"><BookOpen size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">Top kurslar</p>
            <h3 className="stat-value">{topCourses.length} ta</h3>
          </div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-card card">
          <h3>Oylik faollik</h3>
          <div className="css-bar-chart">
            {months.map(month => {
              const heightPercent = (month.value / maxValue) * 100;
              return (
                <div key={month.name} className="bar-group">
                  <div className="bar-tooltip">{month.value}</div>
                  <div className="bar" style={{ height: `${heightPercent}%` }}></div>
                  <div className="bar-label">{month.name}</div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="chart-card card">
          <h3>Tugatish holati</h3>
          <p>Boshlanmagan: {completion.not_started}%</p>
          <p>Jarayonda: {completion.in_progress}%</p>
          <p>Tugatilgan: {completion.completed}%</p>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
