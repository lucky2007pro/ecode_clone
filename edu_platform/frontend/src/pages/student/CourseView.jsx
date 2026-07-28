import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PlayCircle, CheckCircle, Lock, ArrowLeft, HelpCircle, MessageCircle, CreditCard, BookOpen, Users, BarChart2, ChevronDown } from 'lucide-react';
import { AuthContext } from '../../context/AuthContext';
import HomeworkForm from './HomeworkForm';
import QuizView from './QuizView';
import './CourseView.css';

const CourseView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);
  const [course, setCourse] = useState(null);
  const [modules, setModules] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [activeLesson, setActiveLesson] = useState(null);
  const [expandedModules, setExpandedModules] = useState({});
  const [plans, setPlans] = useState([]);
  const [botLink, setBotLink] = useState(null);
  const [loading, setLoading] = useState(true);
  const [enrolled, setEnrolled] = useState(false);
  const [activeCourseTab, setActiveCourseTab] = useState('lessons');

  useEffect(() => {
    fetchCourseDetails();
    fetchLessons();
    fetchPlans();
    fetchBotSettings();
    checkEnrollment();
  }, [id, user]);

  const checkEnrollment = async () => {
    if (!user) return;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/enrollments/user/${user.id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const enrollments = await response.json();
        const isEnrolled = enrollments.some(e => e.course_id === id);
        setEnrolled(isEnrolled || user.role === 'admin' || user.role === 'manager' || user.role === 'teacher');
      }
    } catch (err) { console.error(err); }
  };

  const fetchPlans = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/payments/plans/${id}`);
      if(res.ok) setPlans(await res.json());
    } catch(err) { console.error(err); }
  };

  const fetchBotSettings = async () => {
    try {
      const schoolId = "00000000-0000-0000-0000-000000000000";
      const res = await fetch(`http://localhost:8000/api/v1/bot/${schoolId}/get-invite`, {
        method: 'POST'
      });
      if(res.ok) {
        const data = await res.json();
        if(data.invite_link) setBotLink(data.invite_link);
      }
    } catch(err) { console.error(err); }
  };

  const fetchCourseDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8000/api/v1/courses/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const courses = await res.json();
        const found = courses.find(c => c.id === id);
        if (found) setCourse(found);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const fetchLessons = async () => {
    try {
      const token = localStorage.getItem('token');
      const [modRes, lesRes] = await Promise.all([
        fetch(`http://localhost:8000/api/v1/lessons/course/${id}/modules`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`http://localhost:8000/api/v1/lessons/course/${id}`, { headers: { 'Authorization': `Bearer ${token}` } })
      ]);
      
      if (modRes.ok) {
        const mods = await modRes.json();
        setModules(mods);
        const exp = {};
        mods.forEach(m => exp[m.id] = true);
        setExpandedModules(exp);
      }
      
      if (lesRes.ok) {
        const data = await lesRes.json();
        setLessons(data);
        if (data.length > 0) setActiveLesson(data[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleModule = (modId) => {
    setExpandedModules(prev => ({...prev, [modId]: !prev[modId]}));
  };

  const handlePurchase = async () => {
    if (!window.confirm("Kursni xarid qilishni xohlaysizmi? Balansingizdan pul yechib olinadi.")) return;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/enrollments/`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: user.id,
          course_id: id
        })
      });
      if (response.ok) {
        alert("Kurs muvaffaqiyatli sotib olindi!");
        setEnrolled(true);
        window.location.reload();
      } else {
        const errorData = await response.json();
        alert(`Xatolik: ${errorData.detail}`);
      }
    } catch (err) { console.error(err); }
  };

  if (loading) return <div className="loading-state"><div className="spinner"></div></div>;

  return (
    <div className="course-view-layout">
      {/* Mini Sidebar on the Far Left */}
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
              {enrolled ? (
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
                          {lessons.filter(l => l.module_id === mod.id).map(lesson => (
                            <div 
                              key={lesson.id} 
                              className={`lesson-nav-item-new ${activeLesson?.id === lesson.id ? 'active' : ''}`}
                              onClick={() => setActiveLesson(lesson)}
                              style={{ padding: '8px 12px', marginBottom: '4px' }}
                            >
                              <div className="lesson-nav-info-new">
                                <span className="lesson-title-new" style={{fontSize: '13px'}}>{lesson.title}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                  
                  {/* Standalone lessons without modules */}
                  {lessons.filter(l => !l.module_id).length > 0 && (
                    <div style={{marginTop: '15px'}}>
                      <h4 style={{fontSize: '13px', color: '#64748b', marginBottom: '10px', textTransform: 'uppercase', letterSpacing: '0.5px'}}>Boshqa Darslar</h4>
                      {lessons.filter(l => !l.module_id).map(lesson => (
                        <div 
                          key={lesson.id} 
                          className={`lesson-nav-item-new ${activeLesson?.id === lesson.id ? 'active' : ''}`}
                          onClick={() => setActiveLesson(lesson)}
                        >
                          <div className="lesson-nav-info-new">
                            <span className="lesson-title-new">{lesson.title}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </>
              ) : (
                <div style={{ padding: '20px', textAlign: 'center', color: '#64748b' }}>
                  <Lock size={40} style={{ margin: '0 auto', marginBottom: '10px', color: '#cbd5e1' }} />
                  <p>Darslarni ko'rish uchun kursni sotib oling.</p>
                </div>
              )}
              
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
                  <h3 className="course-info-card-title">Sotib olish</h3>
                  <div style={{ marginTop: '12px' }}>
                    <div style={{padding: '12px', background: '#f8fafc', borderRadius: '8px', marginBottom: '8px', border: '1px solid #e2e8f0'}}>
                      <div style={{fontWeight: '600', color: '#0f172a', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px'}}>
                        <CreditCard size={14} /> To'liq kurs to'lovi
                      </div>
                      <div style={{fontSize: '14px', color: '#3b82f6', fontWeight: 'bold', marginTop: '4px'}}>
                        {course?.price ? course.price.toLocaleString() : '0'} UZS
                      </div>
                    </div>
                    <button className="btn-primary full-width mt-2" onClick={handlePurchase}>Sotib olish</button>
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="course-main-content">
            {activeLesson ? (
              activeLesson.lesson_type === 'quiz' ? (
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
                  <HomeworkForm lessonId={activeLesson.id} />
                  
                  <div className="lesson-footer">
                    <button className="btn-primary">
                      <CheckCircle size={18} style={{marginRight: '8px'}} /> Darsni tugatish
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
      ) : (
        <div className="course-main-content" style={{ flex: 1, padding: '40px' }}>
          <div className="empty-state card" style={{ height: '100%', justifyContent: 'center' }}>
            <h2>{activeCourseTab.charAt(0).toUpperCase() + activeCourseTab.slice(1)} sahifasi</h2>
            <p className="text-muted">Bu bo'lim tez orada ishga tushadi.</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default CourseView;
