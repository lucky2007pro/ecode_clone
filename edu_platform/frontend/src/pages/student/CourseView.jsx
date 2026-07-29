import React, { useState, useEffect, useContext, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PlayCircle, CheckCircle, Lock, ArrowLeft, MessageCircle, CreditCard, BookOpen, Users, BarChart2, ChevronDown } from 'lucide-react';
import { AuthContext } from '../../context/auth-context';
import { api } from '../../api';
import HomeworkForm from './HomeworkForm';
import QuizView from './QuizView';
import Chat from './Chat';
import './CourseView.css';

const CourseView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, school, refreshUser } = useContext(AuthContext);
  const [course, setCourse] = useState(null);
  const [modules, setModules] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [activeLesson, setActiveLesson] = useState(null);
  const [expandedModules, setExpandedModules] = useState({});
  const [botLink, setBotLink] = useState(null);
  const [loading, setLoading] = useState(true);
  const [enrolled, setEnrolled] = useState(false);
  const [activeCourseTab, setActiveCourseTab] = useState('lessons');
  const [completedLessons, setCompletedLessons] = useState([]);
  const [courseStudents, setCourseStudents] = useState([]);
  const [quizResults, setQuizResults] = useState([]);
  const [quizTitles, setQuizTitles] = useState({});

  const fetchCourseStudents = useCallback(async () => {
    try {
      const data = await api(`/enrollments/course/${id}`);
      setCourseStudents(data);
    } catch (err) { console.error(err); }
  }, [id]);

  const fetchMyAnalytics = useCallback(async () => {
    try {
      const results = await api('/quizzes/results/my');
      const quizLessons = lessons.filter(l => l.lesson_type === 'quiz');
      const quizzes = await Promise.all(
        quizLessons.map(l => api(`/quizzes/lesson/${l.id}`).catch(() => null))
      );
      const titles = {};
      quizzes.forEach(q => { if (q) titles[q.id] = q.title; });
      setQuizTitles(titles);
      setQuizResults(results.filter(r => titles[r.quiz_id] !== undefined));
    } catch (err) { console.error(err); }
  }, [lessons]);

  useEffect(() => {
    if (activeCourseTab === 'students') fetchCourseStudents();
    if (activeCourseTab === 'analytics') fetchMyAnalytics();
  }, [activeCourseTab, id, lessons, fetchCourseStudents, fetchMyAnalytics]);

  const completedCount = lessons.filter(l => completedLessons.includes(l.id)).length;
  const completionPercent = lessons.length > 0 ? Math.round(completedCount * 100 / lessons.length) : 0;

  const firstThreeLessonIds = lessons.slice(0, 3).map(l => l.id);

  useEffect(() => {
    if (!user) return;
    try {
      setCompletedLessons(JSON.parse(localStorage.getItem(`completed_lessons_${user.id}`)) || []);
    } catch { setCompletedLessons([]); }
  }, [user]);

  const handleCompleteLesson = () => {
    if (!user || !activeLesson) return;
    const updated = [...new Set([...completedLessons, activeLesson.id])];
    setCompletedLessons(updated);
    localStorage.setItem(`completed_lessons_${user.id}`, JSON.stringify(updated));
  };

  const checkEnrollment = useCallback(async () => {
    if (!user) return;
    try {
      const enrollments = await api(`/enrollments/user/${user.id}`);
      const isEnrolled = enrollments.some(e => e.course_id === id);
      setEnrolled(isEnrolled || user.role === 'admin' || user.role === 'manager' || user.role === 'teacher');
    } catch (err) { console.error(err); }
  }, [id, user]);

  const fetchBotSettings = useCallback(async () => {
    try {
      if (!school?.id) return;
      const data = await api(`/bot/${school.id}/get-invite`, { method: 'POST' });
      if (data.invite_link) setBotLink(data.invite_link);
    } catch(err) { console.error(err); }
  }, [school]);

  const fetchCourseDetails = useCallback(async () => {
    try {
      const courses = await api('/courses/');
      const found = courses.find(c => c.id === id);
      if (found) setCourse(found);
    } catch (err) {
      console.error(err);
    }
  }, [id]);

  const fetchLessons = useCallback(async () => {
    try {
      const [mods, data] = await Promise.all([
        api(`/lessons/course/${id}/modules`).catch(() => []),
        api(`/lessons/course/${id}`).catch(() => [])
      ]);

      setModules(mods);
      const exp = {};
      mods.forEach(m => exp[m.id] = true);
      setExpandedModules(exp);

      setLessons(data);
      if (data.length > 0) setActiveLesson(data[0]);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    fetchCourseDetails();
    fetchLessons();
    fetchBotSettings();
    checkEnrollment();
  }, [id, user, school, fetchCourseDetails, fetchLessons, fetchBotSettings, checkEnrollment]);

  const toggleModule = (modId) => {
    setExpandedModules(prev => ({...prev, [modId]: !prev[modId]}));
  };

  const handlePurchase = async () => {
    const price = Number(course?.price) || 0;
    const msg = price > 0
      ? `Kurs narxi ${price.toLocaleString('uz-UZ')} so'm. Balansingizdan yechilsinmi?`
      : "Bu bepul kursga yozilmoqchimisiz?";
    if (!window.confirm(msg)) return;
    try {
      await api('/enrollments/purchase', {
        method: 'POST',
        body: { course_id: id }
      });
      await refreshUser();
      alert(price > 0 ? "Kurs muvaffaqiyatli sotib olindi!" : "Kursga muvaffaqiyatli yozildingiz!");
      setEnrolled(true);
      window.location.reload();
    } catch (err) {
      const m = err.message || '';
      if (m.includes('yetarli emas')) {
        alert(`${m}\n\nIltimos, admin yoki menejerga murojaat qilib balansingizni to'ldiring.`);
      } else {
        alert(`Xatolik: ${m}`);
      }
    }
  };

  if (loading) return <div className="loading-state"><div className="spinner"></div></div>;

  return (
    <div className="course-view-layout">
      {}
      <div className="course-mini-sidebar">
        <button className="back-btn-mini" onClick={() => navigate('/courses')}>
          <ArrowLeft size={20} />
        </button>
        <div className="mini-sidebar-menu">
          <div className={`mini-tab ${activeCourseTab === 'lessons' ? 'active' : ''}`} onClick={() => setActiveCourseTab('lessons')}>
            <BookOpen size={20} />
            <span>Darslar</span>
          </div>
          <div className={`mini-tab ${activeCourseTab === 'chat' ? 'active' : ''}`} onClick={() => setActiveCourseTab('chat')}>
            <MessageCircle size={20} />
            <span>Chat</span>
          </div>
          <div className={`mini-tab ${activeCourseTab === 'students' ? 'active' : ''}`} onClick={() => setActiveCourseTab('students')}>
            <Users size={20} />
            <span>Talabalar</span>
          </div>
          <div className={`mini-tab ${activeCourseTab === 'payments' ? 'active' : ''}`} onClick={() => setActiveCourseTab('payments')}>
            <CreditCard size={20} />
            <span>To'lovlar</span>
          </div>
          <div className={`mini-tab ${activeCourseTab === 'analytics' ? 'active' : ''}`} onClick={() => setActiveCourseTab('analytics')}>
            <BarChart2 size={20} />
            <span>Analitika</span>
          </div>
        </div>
      </div>

      {activeCourseTab === 'lessons' ? (
        <>
          <div className="course-sidebar glass-panel">
            <div className="sidebar-header">
              <h2>{course?.title || "O'quv Kursi"}</h2>
            </div>

            <div className="lesson-nav">
                <>
                  {modules.map(mod => (
                    <div key={mod.id} style={{marginBottom: '10px'}}>
                      <div
                        className="module-header-new"
                        onClick={() => toggleModule(mod.id)}
                        style={{
                          display: 'flex', justifyContent: 'space-between', padding: '10px 15px',
                          background: '#fff', borderRadius: '8px', cursor: 'pointer', border: '1px solid #e2e8f0',
                          fontWeight: '600', fontSize: '14px', color: '#1e293b'
                        }}
                      >
                        <span>{mod.title}</span>
                        <ChevronDown size={18} style={{ transform: expandedModules[mod.id] ? 'rotate(180deg)' : 'rotate(0deg)', transition: '0.2s' }} />
                      </div>

                      {expandedModules[mod.id] && (
                        <div style={{paddingLeft: '10px', marginTop: '5px'}}>
                          {lessons.filter(l => l.module_id === mod.id).map(lesson => {
                            const isLocked = !enrolled && !firstThreeLessonIds.includes(lesson.id);
                            return (
                              <div
                                key={lesson.id}
                                className={`lesson-nav-item-new ${activeLesson?.id === lesson.id ? 'active' : ''} ${isLocked ? 'locked' : ''}`}
                                onClick={() => setActiveLesson(lesson)}
                                style={{ padding: '8px 12px', marginBottom: '4px', opacity: isLocked ? 0.7 : 1 }}
                              >
                                <div className="lesson-nav-info-new" style={{display: 'flex', alignItems: 'center', gap: '6px', justifyContent: 'space-between', width: '100%'}}>
                                  <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
                                    {completedLessons.includes(lesson.id) && <CheckCircle size={14} color="#10b981" />}
                                    <span className="lesson-title-new" style={{fontSize: '13px'}}>{lesson.title}</span>
                                  </div>
                                  {isLocked && <Lock size={14} color="#94a3b8" />}
                                </div>
                              </div>
                            );
                          })}
                        </div>
                      )}
                    </div>
                  ))}

                  {/* Standalone lessons without modules */}
                  {lessons.filter(l => !l.module_id).length > 0 && (
                    <div style={{marginTop: '15px'}}>
                      <h4 style={{fontSize: '13px', color: '#64748b', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.5px'}}>Boshqa Darslar</h4>
                      {lessons.filter(l => !l.module_id).map(lesson => {
                        const isLocked = !enrolled && !firstThreeLessonIds.includes(lesson.id);
                        return (
                          <div
                            key={lesson.id}
                            className={`lesson-nav-item-new ${activeLesson?.id === lesson.id ? 'active' : ''} ${isLocked ? 'locked' : ''}`}
                            onClick={() => setActiveLesson(lesson)}
                            style={{ opacity: isLocked ? 0.7 : 1 }}
                          >
                            <div className="lesson-nav-info-new" style={{display: 'flex', alignItems: 'center', gap: '6px', justifyContent: 'space-between', width: '100%'}}>
                              <div style={{display: 'flex', alignItems: 'center', gap: '6px'}}>
                                {completedLessons.includes(lesson.id) && <CheckCircle size={14} color="#10b981" />}
                                <span className="lesson-title-new">{lesson.title}</span>
                              </div>
                              {isLocked && <Lock size={14} color="#94a3b8" />}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </>

              <div className="course-info-card mt-4">
                <h3 className="course-info-card-title">Kurs Haqida</h3>
                <p className="course-info-card-text">{course?.description || "Bu kurs orqali siz yangi bilimlarni o'zlashtirasiz."}</p>
                {botLink && enrolled && (
                  <a href={botLink} target="_blank" rel="noreferrer" className="btn-primary full-width mt-4" style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', background: '#0088cc', fontSize: '13px', padding: '8px'}}>
                    <MessageCircle size={16} /> Guruhga qo'shilish
                  </a>
                )}
              </div>

              {(!enrolled && user && user.role === 'student') && (
                <div className="course-info-card mt-4">
                  <h3 className="course-info-card-title">{Number(course?.price) > 0 ? 'Kursni sotib olish' : 'Kursga yozilish'}</h3>
                  <div style={{ marginTop: '12px' }}>
                    <div style={{padding: '12px', background: '#f8fafc', borderRadius: '8px', marginBottom: '8px', border: '1px solid #e2e8f0'}}>
                      <div style={{fontWeight: '600', color: '#0f172a', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px'}}>
                        <CreditCard size={14} /> {Number(course?.price) > 0 ? `${Number(course.price).toLocaleString('uz-UZ')} so'm` : 'Bepul'}
                      </div>
                      <div style={{fontSize: '13px', color: '#64748b', marginTop: '4px'}}>
                        {Number(course?.price) > 0
                          ? `To'lov balansingizdan yechiladi. Balans: ${Number(user.balance || 0).toLocaleString('uz-UZ')} so'm`
                          : "Bu kursga bepul yozilishingiz mumkin."}
                      </div>
                    </div>
                    <button className="btn-primary full-width mt-2" onClick={handlePurchase}>
                      {Number(course?.price) > 0 ? 'Sotib olish' : 'Kursga yozilish'}
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="course-main-content">
            {activeLesson ? (
              !enrolled && !firstThreeLessonIds.includes(activeLesson.id) ? (
                <div className="empty-state">
                  <Lock size={48} className="icon-muted" style={{ marginBottom: '15px' }} />
                  <h3>Bu dars yopiq</h3>
                  <p>Davomini ko'rish uchun kursni sotib oling.</p>
                  {(user && user.role === 'student') && (
                    <button className="btn-primary mt-4" onClick={handlePurchase}>
                      {Number(course?.price) > 0 ? 'Sotib olish' : 'Kursga yozilish'}
                    </button>
                  )}
                </div>
              ) : activeLesson.lesson_type === 'quiz' ? (
                <QuizView lessonId={activeLesson.id} />
              ) : (
                <div className="active-lesson-container">
                  <h1 className="lesson-main-title">{activeLesson.title}</h1>

                  {activeLesson.lesson_type === 'video' && activeLesson.video_url && (
                    <div className="video-player-wrapper card">
                      <div className="video-aspect-ratio">
                        <iframe
                          src={activeLesson.video_url.replace("watch?v=", "embed/")}
                          frameBorder="0"
                          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                          allowFullScreen
                          className="lesson-video"
                        ></iframe>
                      </div>
                    </div>
                  )}

                  {(activeLesson.content || activeLesson.lesson_type === 'text') && (
                    <div className="lesson-text-content card">
                      {activeLesson.content ? (
                        <p>{activeLesson.content}</p>
                      ) : (
                        <p className="text-muted">Bu dars uchun matn kiritilmagan.</p>
                      )}
                    </div>
                  )}

                  {/* Uy vazifasi yuborish formasi */}
                  {enrolled && <HomeworkForm lessonId={activeLesson.id} />}

                  <div className="lesson-footer">
                    <button
                      className="btn-primary"
                      onClick={handleCompleteLesson}
                      disabled={completedLessons.includes(activeLesson.id)}
                      style={completedLessons.includes(activeLesson.id) ? { background: '#10b981', cursor: 'default' } : undefined}
                    >
                      <CheckCircle size={18} style={{marginRight: '8px'}} />
                      {completedLessons.includes(activeLesson.id) ? 'Tugatilgan' : 'Darsni tugatish'}
                    </button>
                  </div>
                </div>
              )
            ) : (
              <div className="empty-state">
                <PlayCircle size={48} className="icon-muted" />
                <h3>Dars tanlanmadi</h3>
                <p>Chap tomondan darsni tanlang.</p>
              </div>
            )}
          </div>
        </>
      ) : activeCourseTab === 'chat' ? (
        <div className="course-main-content" style={{ flex: 1, padding: '24px' }}>
          <Chat courseId={id} />
        </div>
      ) : activeCourseTab === 'students' ? (
        <div className="course-main-content" style={{ flex: 1, padding: '24px' }}>
          <div className="cv-tab-container">
            <div className="course-info-card" style={{ marginTop: 0 }}>
              <h3 className="course-info-card-title">Kurs talabalari ({courseStudents.filter(s => s.role === 'student').length})</h3>
              {courseStudents.filter(s => s.role === 'student').length === 0 ? (
                <p className="course-info-card-text">Bu kursga hali hech kim yozilmagan.</p>
              ) : (
                courseStudents.filter(s => s.role === 'student').map(s => (
                  <div key={s.id} className="cv-student-row">
                    <div className="cv-student-info">
                      <span className="cv-student-name">{s.full_name || "Noma'lum"}</span>
                      <span className="cv-student-status">{s.status === 'active' ? 'Faol' : s.status}</span>
                    </div>
                    <div className="cv-progress-track" style={{ flex: 1, maxWidth: '220px' }}>
                      <div className="cv-progress-fill" style={{ width: `${Math.min(100, Math.round(s.progress))}%` }}></div>
                    </div>
                    <span className="cv-percent">{Math.round(s.progress)}%</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      ) : activeCourseTab === 'payments' ? (
        <div className="course-main-content" style={{ flex: 1, padding: '24px' }}>
          <div className="cv-tab-container">
            <div className="course-info-card" style={{ marginTop: 0 }}>
              <h3 className="course-info-card-title">Kurs to'lovi</h3>
              <p className="course-info-card-text">
                Kurs narxi: <b>{course?.price > 0 ? `${Number(course.price).toLocaleString('uz-UZ')} so'm` : 'Bepul'}</b>
              </p>
              <div style={{ marginTop: '12px', padding: '12px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <div style={{ fontWeight: '600', color: '#0f172a', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px' }}>
                  <CreditCard size={14} /> Balansdan to'lov
                </div>
                <div style={{ fontSize: '13px', color: '#64748b', marginTop: '4px' }}>
                  Kurs to'lovi balansingizdan yechiladi. Balans: {Number(user?.balance || 0).toLocaleString('uz-UZ')} so'm
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="course-main-content" style={{ flex: 1, padding: '24px' }}>
          <div className="cv-tab-container">
            <div className="course-info-card" style={{ marginTop: 0 }}>
              <h3 className="course-info-card-title">Darslarni o'zlashtirish</h3>
              <p className="course-info-card-text">
                {lessons.length} ta darsdan {completedCount} tasi tugatilgan ({completionPercent}%)
              </p>
              <div className="cv-progress-track" style={{ marginTop: '10px' }}>
                <div className="cv-progress-fill" style={{ width: `${completionPercent}%` }}></div>
              </div>
            </div>
            <div className="course-info-card">
              <h3 className="course-info-card-title">Test natijalarim</h3>
              {quizResults.length === 0 ? (
                <p className="course-info-card-text">Bu kursda hali test topshirmagansiz.</p>
              ) : (
                quizResults.map(r => (
                  <div key={r.id} className="cv-student-row">
                    <div className="cv-student-info">
                      <span className="cv-student-name">{quizTitles[r.quiz_id] || 'Test'}</span>
                      <span className="cv-student-status">{new Date(r.created_at + (r.created_at.endsWith('Z') ? '' : 'Z')).toLocaleDateString('uz-UZ')}</span>
                    </div>
                    <span className="cv-percent">{r.score}/{r.total} ({r.total > 0 ? Math.round(r.score * 100 / r.total) : 0}%)</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CourseView;
