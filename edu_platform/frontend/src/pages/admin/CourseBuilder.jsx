import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Plus, Video, FileText, CheckSquare, Save, ArrowLeft, CreditCard } from 'lucide-react';
import './CourseBuilder.css';

const CourseBuilder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // New lesson form state
  const [showForm, setShowForm] = useState(false);
  const [uploadingVideo, setUploadingVideo] = useState(false);
  const [newLesson, setNewLesson] = useState({
    title: '',
    lesson_type: 'video',
    video_url: '',
    content: '',
  });

  // Payment plans state
  const [plans, setPlans] = useState([]);
  const [newPlan, setNewPlan] = useState({ name: '', plan_type: 'one_time', price: 0, months: 1 });
  const [showPlanForm, setShowPlanForm] = useState(false);

  useEffect(() => {
    fetchCourseDetails();
    fetchLessons();
    fetchPlans();
  }, [id]);

  const fetchCourseDetails = async () => {
    // We would normally fetch specific course details here
    // For now, we'll just set a mock title if we can't find it
    setCourse({ id, title: "Kursni Tahrirlash" });
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
      }
    } catch (err) {
      console.error('Darslarni yuklashda xatolik:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddLesson = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const payload = {
        ...newLesson,
        course_id: id,
        order: lessons.length + 1
      };
      
      const response = await fetch('http://localhost:8000/api/v1/lessons/', {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });
      
      if (response.ok) {
        setShowForm(false);
        setNewLesson({ title: '', lesson_type: 'video', video_url: '', content: '' });
        fetchLessons(); // Reload lessons
      }
    } catch (err) {
      console.error('Dars qo\'shishda xatolik:', err);
    }
  };

  const fetchPlans = async () => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/payments/plans/${id}`);
      if(res.ok) setPlans(await res.json());
    } catch(err) { console.error(err); }
  };

  const handleAddPlan = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...newPlan, course_id: id };
      const response = await fetch('http://localhost:8000/api/v1/payments/plans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (response.ok) {
        setShowPlanForm(false);
        setNewPlan({ name: '', plan_type: 'one_time', price: 0, months: 1 });
        fetchPlans();
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleVideoUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadingVideo(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/api/v1/videos/upload', {
        method: 'POST',
        body: formData
      });
      if (response.ok) {
        const data = await response.json();
        setNewLesson({...newLesson, video_url: data.video_url});
        alert(data.message); // Kinescope ga yuklanganini ko'rsatamiz
      } else {
        alert("Video yuklashda xatolik yuz berdi");
      }
    } catch(err) {
      console.error('Upload error', err);
    } finally {
      setUploadingVideo(false);
    }
  };

  const getLessonIcon = (type) => {
    switch(type) {
      case 'video': return <Video size={20} className="icon-video" />;
      case 'text': return <FileText size={20} className="icon-text" />;
      case 'quiz': return <CheckSquare size={20} className="icon-quiz" />;
      default: return <FileText size={20} />;
    }
  };

  if (loading) return <div className="loading">Yuklanmoqda...</div>;

  return (
    <div className="course-builder">
      <div className="builder-header">
        <button className="btn-icon" onClick={() => navigate('/courses')}>
          <ArrowLeft size={20} />
        </button>
        <div>
          <h1>Kurs Konstruktori</h1>
          <p>{course?.title}</p>
        </div>
      </div>

      <div className="builder-content">
        <div className="lessons-list">
          <h2>Darslar Dasturi</h2>
          
          {lessons.length === 0 ? (
            <div className="empty-lessons">
              <p>Bu kursda hali darslar yo'q. Birinchi darsni qo'shing.</p>
            </div>
          ) : (
            <div className="lessons-container">
              {lessons.map((lesson, index) => (
                <div key={lesson.id} className="lesson-item card">
                  <div className="lesson-drag-handle">{index + 1}</div>
                  <div className="lesson-info">
                    <div className="lesson-title-row">
                      {getLessonIcon(lesson.lesson_type)}
                      <h3>{lesson.title}</h3>
                    </div>
                    {lesson.lesson_type === 'video' && lesson.video_url && (
                      <span className="lesson-meta">{lesson.video_url}</span>
                    )}
                  </div>
                  <div className="lesson-actions">
                    <button className="btn-outline btn-sm">Tahrirlash</button>
                  </div>
                </div>
              ))}
            </div>
          )}

          {!showForm ? (
            <button className="btn-outline add-lesson-btn" onClick={() => setShowForm(true)}>
              <Plus size={20} /> Yangi Dars Qo'shish
            </button>
          ) : (
            <div className="add-lesson-form card">
              <h3>Yangi Dars</h3>
              <form onSubmit={handleAddLesson}>
                <div className="form-group">
                  <label>Dars Nomi</label>
                  <input 
                    type="text" 
                    value={newLesson.title}
                    onChange={(e) => setNewLesson({...newLesson, title: e.target.value})}
                    required
                    placeholder="Masalan: 1-dars. Kirish"
                  />
                </div>
                
                <div className="form-group">
                  <label>Dars Turi</label>
                  <select 
                    value={newLesson.lesson_type}
                    onChange={(e) => setNewLesson({...newLesson, lesson_type: e.target.value})}
                  >
                    <option value="video">Video Dars</option>
                    <option value="text">Matnli Dars (Longread)</option>
                    <option value="quiz">Test / Quiz</option>
                  </select>
                </div>

                {newLesson.lesson_type === 'video' && (
                  <div className="form-group">
                    <label>Video Yuklash (Kinescope)</label>
                    <div style={{display: 'flex', gap: '10px', alignItems: 'center'}}>
                      <input 
                        type="file" 
                        accept="video/*"
                        onChange={handleVideoUpload}
                        disabled={uploadingVideo}
                      />
                      {uploadingVideo && <span className="text-muted text-sm">Yuklanmoqda... Kuting...</span>}
                    </div>
                    <label style={{marginTop: '15px'}}>Yoki to'g'ridan-to'g'ri URL (YouTube, Vimeo, Kinescope URL)</label>
                    <input 
                      type="url" 
                      value={newLesson.video_url}
                      onChange={(e) => setNewLesson({...newLesson, video_url: e.target.value})}
                      placeholder="https://..."
                    />
                  </div>
                )}

                <div className="form-group">
                  <label>Qo'shimcha Matn (Markdown)</label>
                  <textarea 
                    rows="4"
                    value={newLesson.content}
                    onChange={(e) => setNewLesson({...newLesson, content: e.target.value})}
                    placeholder="Dars uchun tavsif yoki matnli materiallar..."
                  ></textarea>
                </div>

                <div className="form-actions">
                  <button type="button" className="btn-outline" onClick={() => setShowForm(false)}>Bekor qilish</button>
                  <button type="submit" className="btn-primary"><Save size={18} style={{marginRight: '8px'}}/> Saqlash</button>
                </div>
              </form>
            </div>
          )}
        </div>
        
        <div className="builder-sidebar">
          <div className="card" style={{marginBottom: '20px'}}>
            <h3>To'lov Rejalari</h3>
            <p className="text-muted" style={{fontSize: '14px', marginBottom: '16px'}}>
              O'quvchilar kursni qanday sotib olishlarini sozlang
            </p>
            
            {plans.map(plan => (
              <div key={plan.id} style={{padding: '10px', background: '#f8fafc', borderRadius: '6px', marginBottom: '10px', border: '1px solid #e2e8f0'}}>
                <div style={{fontWeight: '600'}}>{plan.name}</div>
                <div style={{fontSize: '14px', color: '#64748b', display: 'flex', justifyContent: 'space-between', marginTop: '5px'}}>
                  <span>{plan.price} so'm</span>
                  <span>{plan.plan_type === 'installment' ? `${plan.months} oy muddatli` : (plan.plan_type === 'subscription' ? 'Oylik obuna' : 'Bir martalik')}</span>
                </div>
              </div>
            ))}

            {!showPlanForm ? (
              <button className="btn-outline full-width" onClick={() => setShowPlanForm(true)}>
                <Plus size={16} style={{marginRight: '5px'}}/> Reja qo'shish
              </button>
            ) : (
              <form onSubmit={handleAddPlan} style={{marginTop: '15px'}}>
                <div className="form-group">
                  <input type="text" placeholder="Nomi (Masalan: VIP Ta'rif)" required value={newPlan.name} onChange={e => setNewPlan({...newPlan, name: e.target.value})} style={{padding: '8px', fontSize: '14px'}}/>
                </div>
                <div className="form-group">
                  <select value={newPlan.plan_type} onChange={e => setNewPlan({...newPlan, plan_type: e.target.value})} style={{padding: '8px', fontSize: '14px'}}>
                    <option value="one_time">Bir martalik to'lov</option>
                    <option value="installment">Bo'lib-bo'lib to'lash (Nasiya)</option>
                    <option value="subscription">Oylik abonent to'lovi</option>
                  </select>
                </div>
                <div className="form-group">
                  <input type="number" placeholder="Narxi (so'm)" required value={newPlan.price} onChange={e => setNewPlan({...newPlan, price: parseFloat(e.target.value) || 0})} style={{padding: '8px', fontSize: '14px'}}/>
                </div>
                {newPlan.plan_type === 'installment' && (
                  <div className="form-group">
                    <input type="number" placeholder="Necha oy?" required value={newPlan.months} onChange={e => setNewPlan({...newPlan, months: parseInt(e.target.value) || 1})} style={{padding: '8px', fontSize: '14px'}}/>
                  </div>
                )}
                <div style={{display: 'flex', gap: '10px'}}>
                  <button type="button" className="btn-outline" style={{padding: '5px 10px'}} onClick={() => setShowPlanForm(false)}>Bekor qilish</button>
                  <button type="submit" className="btn-primary" style={{padding: '5px 10px'}}>Saqlash</button>
                </div>
              </form>
            )}
          </div>

          <div className="card">
            <h3>Kurs Sozlamalari</h3>
            <p className="text-muted" style={{fontSize: '14px', marginBottom: '16px'}}>
              Bu yerdan kursning narxi, tavsifi va muqovasini o'zgartirishingiz mumkin (Tez kunda).
            </p>
            <button className="btn-primary full-width">Kursni Nashr Etish</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseBuilder;
