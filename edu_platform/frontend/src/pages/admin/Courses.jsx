import React, { useState, useEffect, useContext, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, X } from 'lucide-react';
import { AuthContext } from '../../context/auth-context';
import { api } from '../../api';
import './CoursesCatalog.css';

const cardThemes = [
  'linear-gradient(135deg, #FF8C00 0%, #FF5F00 100%)',
  'linear-gradient(135deg, #A855F7 0%, #7E22CE 100%)',
  'linear-gradient(135deg, #10B981 0%, #059669 100%)',
  'linear-gradient(135deg, #3B82F6 0%, #2563EB 100%)',
  'linear-gradient(135deg, #F97316 0%, #EA580C 100%)',
  'linear-gradient(135deg, #EC4899 0%, #BE185D 100%)',
];

const CoursesCatalog = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newCourse, setNewCourse] = useState({ title: '', description: '', price: 0 });
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const fetchCourses = useCallback(async () => {
    try {
      let data = await api('/courses/');

      if (user && user.role === 'teacher') {
        try {
          const enrollData = await api(`/enrollments/user/${user.id}`);
          const assignedCourseIds = enrollData.map(e => e.course_id);
          data = data.filter(c => assignedCourseIds.includes(c.id));
        } catch (err) {
          console.error('Biriktirilgan kurslarni yuklashda xatolik:', err);
        }
      }

      setCourses(data);
    } catch (err) {
      console.error('Kurslarni yuklashda xatolik:', err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    if (user) {
      fetchCourses();
    }
  }, [user, fetchCourses]);

  const handleCreateCourse = async (e) => {
    e.preventDefault();
    try {
      const slug = newCourse.title.toLowerCase().trim().replace(/[^a-z0-9]+/g, '-');

      const data = await api('/courses/', {
        method: 'POST',
        body: { ...newCourse, slug }
      });

      setCourses([...courses, data]);
      setShowModal(false);
      setNewCourse({ title: '', description: '', price: 0 });
    } catch (err) {
      console.error("Kurs qo'shishda xatolik:", err);
    }
  };

  return (
    <div className="courses-catalog-new">
      <div className="catalog-header-new">
        <h1 className="catalog-title">Course catalog</h1>

        <div className="catalog-actions">
          {user && (user.role === 'admin' || user.role === 'manager') && (
            <button className="add-course-btn" onClick={() => setShowModal(true)}>
              <Plus size={20} />
            </button>
          )}
        </div>
      </div>

      {loading ? (
        <div className="loading-state">
          <p>Yuklanmoqda...</p>
        </div>
      ) : courses.length === 0 ? (
        <div className="empty-state">
          <h3>Hozircha kurslar yo'q</h3>
          {user && (user.role === 'admin' || user.role === 'manager') && (
            <p>Tepadagi '+' tugmasi orqali kurs qo'shing.</p>
          )}
        </div>
      ) : (
        <div className="courses-grid-new">
          {courses.map((course, index) => {
            const theme = cardThemes[index % cardThemes.length];
            return (
              <div
                key={course.id}
                className="course-card-new"
                onClick={() => navigate(`/courses/${course.id}`)}
              >
                <div
                  className="course-card-top"
                  style={{ background: theme }}
                >
                </div>
                <div className="course-card-bottom">
                  <h3 className="course-title">{course.title}</h3>
                  <div className="course-info">
                    <span className="lessons-count">{course.lessons_count || 0} lessons</span>
                    <span className="lessons-count" style={{ fontWeight: 600 }}>
                      {Number(course.price) > 0 ? `${Number(course.price).toLocaleString('uz-UZ')} so'm` : 'Bepul'}
                    </span>
                    {user && (user.role === 'admin' || user.role === 'teacher' || user.role === 'manager') && (
                      <button
                        className="edit-btn"
                        onClick={(e) => { e.stopPropagation(); navigate(`/admin/courses/${course.id}/builder`); }}
                      >
                        Builder
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Yangi Kurs</h2>
              <button className="icon-btn-close" onClick={() => setShowModal(false)}>
                <X size={20} />
              </button>
            </div>
            <form onSubmit={handleCreateCourse}>
              <div className="form-group">
                <label>Kurs Nomi</label>
                <input type="text" value={newCourse.title} onChange={e => setNewCourse({...newCourse, title: e.target.value})} required />
              </div>
              <div className="form-group">
                <label>Tavsif</label>
                <textarea value={newCourse.description} onChange={e => setNewCourse({...newCourse, description: e.target.value})} />
              </div>
              <div className="form-group">
                <label>Narxi (so'm)</label>
                <input type="number" value={newCourse.price} onChange={e => setNewCourse({...newCourse, price: parseFloat(e.target.value) || 0})} />
              </div>
              <button type="submit" className="submit-btn">Yaratish</button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default CoursesCatalog;
