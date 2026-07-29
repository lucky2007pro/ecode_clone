import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { BookOpen, CheckCircle, BarChart } from 'lucide-react';
import { api } from '../../api';
import { AuthContext } from '../../context/auth-context';

const cardThemes = [
  'linear-gradient(135deg, #FF8C00 0%, #FF5F00 100%)',
  'linear-gradient(135deg, #A855F7 0%, #7E22CE 100%)',
  'linear-gradient(135deg, #10B981 0%, #059669 100%)',
  'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
  'linear-gradient(135deg, #F97316 0%, #EA580C 100%)',
  'linear-gradient(135deg, #EC4899 0%, #BE185D 100%)',
];

const StudentDashboard = () => {
  const { user } = useContext(AuthContext);
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMyCourses = async () => {
      if (!user) return;
      try {
        const enrollments = await api(`/enrollments/user/${user.id}`);

        const coursePromises = enrollments.map(async (enrollment) => {
          try {
            const courseData = await api(`/courses/${enrollment.course_id}`);
            return { ...courseData, enrollmentStatus: enrollment.status, progress: enrollment.progress };
          } catch { return null; }
        });

        const myCoursesData = await Promise.all(coursePromises);
        setCourses(myCoursesData.filter(c => c !== null));
      } catch (err) {
        console.error("Kurslarni yuklashda xatolik:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchMyCourses();
  }, [user]);

  return (
    <div className="page-container">
      <div className="page-header" style={{ marginBottom: '24px' }}>
        <h1>Mening Kabinetim</h1>
        <p className="text-muted">Kurslardagi jarayon va vazifalar</p>
      </div>

      {}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
        <div className="card glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ width: '50px', height: '50px', borderRadius: '12px', background: 'rgba(59, 130, 246, 0.1)', color: '#3B82F6', display: 'flex', alignItems: 'center', justifyItems: 'center', justifyContent: 'center' }}>
            <BookOpen size={24} />
          </div>
          <div>
            <h3 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>{courses.length}</h3>
            <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '14px' }}>Faol Kurslar</p>
          </div>
        </div>

        <div className="card glass-panel" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ width: '50px', height: '50px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.1)', color: '#10B981', display: 'flex', alignItems: 'center', justifyItems: 'center', justifyContent: 'center' }}>
            <CheckCircle size={24} />
          </div>
          <div>
            <h3 style={{ fontSize: '24px', margin: '0 0 5px 0' }}>{courses.filter(c => c.progress === 100).length}</h3>
            <p style={{ margin: 0, color: 'var(--text-muted)', fontSize: '14px' }}>Tugatilgan Kurslar</p>
          </div>
        </div>
      </div>

      <h2 style={{ fontSize: '20px', marginBottom: '16px' }}>Mening Kurslarim</h2>

      {loading ? (
        <div className="loading-state">
          <p>Yuklanmoqda...</p>
        </div>
      ) : courses.length === 0 ? (
        <div className="card glass-panel" style={{ padding: '40px', textAlign: 'center' }}>
          <BookOpen size={48} style={{ margin: '0 auto 15px', color: 'var(--text-muted)', opacity: 0.5 }} />
          <h3>Siz hali hech qanday kursga yozilmagansiz</h3>
          <p className="text-muted" style={{ marginTop: '10px' }}>Kurslar bo'limiga o'tib, o'zingizga qiziqarli kurslarni tanlang va o'rganishni boshlang.</p>
          <button className="btn-primary" style={{ marginTop: '20px' }} onClick={() => navigate('/courses')}>
            Kurslarni ko'rish
          </button>
        </div>
      ) : (
        <div className="courses-grid-new" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '24px' }}>
          {courses.map((course, index) => {
            const theme = cardThemes[index % cardThemes.length];
            return (
              <div
                key={course.id}
                className="course-card-new"
                onClick={() => navigate(`/courses/${course.id}`)}
                style={{ cursor: 'pointer', background: 'var(--bg-primary)', borderRadius: '16px', overflow: 'hidden', border: '1px solid var(--border-color)', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)' }}
              >
                <div
                  className="course-card-top"
                  style={{ background: theme, height: '120px', position: 'relative' }}
                >
                </div>
                <div className="course-card-bottom" style={{ padding: '20px' }}>
                  <h3 className="course-title" style={{ fontSize: '16px', margin: '0 0 10px 0', fontWeight: '600' }}>{course.title}</h3>
                  <div style={{ marginTop: '15px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '5px' }}>
                      <span>O'zlashtirish</span>
                      <span>{Math.round(course.progress || 0)}%</span>
                    </div>
                    <div style={{ height: '6px', width: '100%', background: '#e2e8f0', borderRadius: '3px', overflow: 'hidden' }}>
                      <div style={{ height: '100%', width: `${Math.round(course.progress || 0)}%`, background: '#3b82f6', borderRadius: '3px' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default StudentDashboard;
