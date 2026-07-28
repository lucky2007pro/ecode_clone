import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PlayCircle, CheckCircle, Lock, ArrowLeft, HelpCircle, MessageCircle, CreditCard, BookOpen, Users, BarChart2, ChevronDown } from 'lucide-react';
import HomeworkForm from './HomeworkForm';
import QuizView from './QuizView';
import './CourseView.css';

const CourseView = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [activeLesson, setActiveLesson] = useState(null);
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
  }, [id]);

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
      setCourse({ id, title: "O'quv Kursi" });
    } catch (err) {
      console.error(err);
    }
  };

  const fetchLessons = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/lessons/course/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setLessons(data);
        if (data.length > 0) setActiveLesson(data[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
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
              <h2>{course?.title}</h2>
            </div>
            
            <div className="lesson-nav">
              {lessons.map((lesson, index) => (
                <div 
                  key={lesson.id} 
                  className={`lesson-nav-item-new ${activeLesson?.id === lesson.id ? 'active' : ''}`}
                  onClick={() => setActiveLesson(lesson)}
                >
                  <div className="lesson-nav-info-new">
                    <span className="lesson-title-new">{lesson.title}</span>
                    <span className="lesson-date-new">Dars sanasi: {lesson.created_at ? new Date(lesson.created_at).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'long', year: 'numeric' }) : '25 Iyul, 2026'}</span>
                  </div>
                  <div className="lesson-nav-icon-new">
                    <ChevronDown size={18} />
                  </div>
                </div>
              ))}
              
              <div className="course-info-card">
                <h3 className="course-info-card-title">Kurs Haqida</h3>
                <p className="course-info-card-text">Bu kurs orqali siz yangi bilimlarni o'zlashtirasiz.</p>
                {botLink && (
                  <a href={botLink} target="_blank" rel="noreferrer" className="btn-primary full-width mt-4" style={{display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px', background: '#0088cc', fontSize: '13px', padding: '8px'}}>
                    <MessageCircle size={16} /> Guruhga qo'shilish
                  </a>
                )}
              </div>
              
              {!enrolled && (
                <div className="course-info-card mt-4">
                  <h3 className="course-info-card-title">Tarifni yangilash</h3>
                  <p className="course-info-card-text">Siz bu kursga bepul obuna bo'lgansiz. Agar boshqa reja kerak bo'lsa tanlang:</p>
                  <div style={{ marginTop: '12px' }}>
                    {plans.map(plan => (
                      <div key={plan.id} style={{padding: '12px', background: '#f8fafc', borderRadius: '8px', marginBottom: '8px', border: '1px solid #e2e8f0', cursor: 'pointer'}} onClick={() => alert("To'lov sahifasiga o'tish (Tez Kunda)")}>
                        <div style={{fontWeight: '600', color: '#0f172a', display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px'}}>
                          <CreditCard size={14} /> {plan.name}
                        </div>
                        <div style={{fontSize: '14px', color: '#3b82f6', fontWeight: 'bold', marginTop: '4px'}}>
                          {plan.price} so'm
                        </div>
                      </div>
                    ))}
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
