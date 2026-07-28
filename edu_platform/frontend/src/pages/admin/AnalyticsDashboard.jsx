import React, { useState, useEffect } from 'react';
import { TrendingUp, Users, BookOpen, Target } from 'lucide-react';
import './AnalyticsDashboard.css';

const AnalyticsDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/analytics/dashboard');
      if (res.ok) {
        const json = await res.json();
        setData(json);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formatMoney = (amount) => {
    return new Intl.NumberFormat('uz-UZ').format(amount) + " so'm";
  };

  if (loading) return <div className="p-8 text-center">Yuklanmoqda...</div>;
  if (!data) return <div className="p-8 text-center text-danger">Ma'lumot topilmadi</div>;

  // Calculate max revenue for CSS chart height scaling
  const maxRevenue = Math.max(...data.monthly_data.map(m => m.revenue));

  return (
    <div className="analytics-dashboard">
      <div className="analytics-header">
        <h1>Analitika va Hisobotlar</h1>
        <p>Maktabingizning asosiy ko'rsatkichlari (MVP)</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card card">
          <div className="stat-icon income"><TrendingUp size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">Umumiy Tushum</p>
            <h3 className="stat-value">{formatMoney(data.total_revenue)}</h3>
          </div>
        </div>
        
        <div className="stat-card card">
          <div className="stat-icon users"><Users size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">Faol O'quvchilar</p>
            <h3 className="stat-value">{data.active_students} ta</h3>
          </div>
        </div>

        <div className="stat-card card">
          <div className="stat-icon courses"><BookOpen size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">Jami Kurslar</p>
            <h3 className="stat-value">{data.courses_count} ta</h3>
          </div>
        </div>

        <div className="stat-card card">
          <div className="stat-icon success"><Target size={24} /></div>
          <div className="stat-info">
            <p className="stat-label">Kursni Tugatish</p>
            <h3 className="stat-value">{data.completion_rate}%</h3>
          </div>
        </div>
      </div>

      <div className="charts-section">
        <div className="chart-card card">
          <h3>Oylik Tushum (Sof CSS Chart)</h3>
          <div className="css-bar-chart">
            {data.monthly_data.map(month => {
              const heightPercent = (month.revenue / maxRevenue) * 100;
              return (
                <div key={month.name} className="bar-group">
                  <div className="bar-tooltip">{formatMoney(month.revenue)}</div>
                  <div className="bar" style={{height: `${heightPercent}%`}}></div>
                  <div className="bar-label">{month.name}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;
