import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Plus, Video, FileText, LayoutList, ChevronDown, ChevronRight, Settings, Image as ImageIcon, File, MonitorPlay, MessageSquare, Table, Edit3, Trash2 } from 'lucide-react';
import './CourseBuilder.css';

const CourseBuilder = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  
  const [course, setCourse] = useState(null);
  const [modules, setModules] = useState([]);
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeModule, setActiveModule] = useState(null);
  const [activeLesson, setActiveLesson] = useState(null);

  // Forms states
  const [showModuleForm, setShowModuleForm] = useState(false);
  const [showLessonForm, setShowLessonForm] = useState(false);
  const [newModuleTitle, setNewModuleTitle] = useState('');
  const [newLessonTitle, setNewLessonTitle] = useState('');

  // Expand/Collapse modules
  const [expandedModules, setExpandedModules] = useState({});

  useEffect(() => {
    fetchCourseDetails();
    fetchModulesAndLessons();
  }, [id]);

  const fetchCourseDetails = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/courses/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        setCourse(await response.json());
      } else {
        setCourse({ id, title: "Kursni Tahrirlash" }); // fallback
      }
    } catch(err) {
       setCourse({ id, title: "Kursni Tahrirlash" });
    }
  };

  const fetchModulesAndLessons = async () => {
    try {
      const token = localStorage.getItem('token');
      const [modRes, lesRes] = await Promise.all([
        fetch(`http://localhost:8000/api/v1/lessons/course/${id}/modules`, { headers: { 'Authorization': `Bearer ${token}` } }),
        fetch(`http://localhost:8000/api/v1/lessons/course/${id}`, { headers: { 'Authorization': `Bearer ${token}` } })
      ]);
      
      let mods = [];
      let less = [];
      if (modRes.ok) mods = await modRes.json();
      if (lesRes.ok) less = await lesRes.json();
      
      setModules(mods);
      setLessons(less);
      
      // Auto expand all
      const exp = {};
      mods.forEach(m => exp[m.id] = true);
      setExpandedModules(exp);
      
      if (less.length > 0) setActiveLesson(less[0]);

    } catch (err) {
      console.error('Xatolik:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddModule = async () => {
    if(!newModuleTitle.trim()) return;
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/lessons/modules`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ course_id: id, title: newModuleTitle, order: modules.length + 1 })
      });
      if (res.ok) {
        setNewModuleTitle('');
        setShowModuleForm(false);
        fetchModulesAndLessons();
      }
    } catch(err) { console.error(err); }
  };

  const handleAddLesson = async () => {
    if(!newLessonTitle.trim() || !activeModule) return;
    try {
      const token = localStorage.getItem('token');
      const modLessons = lessons.filter(l => l.module_id === activeModule);
      const res = await fetch(`http://localhost:8000/api/v1/lessons/`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          course_id: id, 
          module_id: activeModule,
          title: newLessonTitle, 
          lesson_type: 'video',
          order: modLessons.length + 1 
        })
      });
      if (res.ok) {
        setNewLessonTitle('');
        setShowLessonForm(false);
        const newL = await res.json();
        setActiveLesson(newL);
        fetchModulesAndLessons();
      }
    } catch(err) { console.error(err); }
  };

  const toggleModule = (modId) => {
    setExpandedModules(prev => ({...prev, [modId]: !prev[modId]}));
  };

  const handleSaveLesson = async () => {
    if(!activeLesson) return;
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/lessons/${activeLesson.id}`, {
        method: 'PUT',
        headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' },
        body: JSON.stringify(activeLesson)
      });
      if (res.ok) {
        alert("Saqlandi!");
        fetchModulesAndLessons();
      }
    } catch(err) { console.error(err); }
  };

  if (loading) return <div className="cb-loading">Yuklanmoqda...</div>;

  return (
    <div className="cb-container">
      {/* SIDEBAR */}
      <div className="cb-sidebar">
        <div className="cb-sidebar-header">
          <h2 onClick={() => navigate('/courses')} style={{cursor: 'pointer'}}>{course?.title || 'Course'}</h2>
        </div>
        
        <div className="cb-search">
          <input type="text" placeholder="Search..." />
        </div>

        <div className="cb-modules">
          {modules.map(mod => (
            <div key={mod.id} className="cb-module-group">
              <div className="cb-module-header" onClick={() => toggleModule(mod.id)}>
                <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
                  {expandedModules[mod.id] ? <ChevronDown size={16}/> : <ChevronRight size={16}/>}
                  <span>{mod.title}</span>
                </div>
                <Settings size={14} className="cb-icon-muted" />
              </div>
              
              {expandedModules[mod.id] && (
                <div className="cb-lessons-list">
                  {lessons.filter(l => l.module_id === mod.id).map(lesson => (
                    <div 
                      key={lesson.id} 
                      className={`cb-lesson-item ${activeLesson?.id === lesson.id ? 'active' : ''}`}
                      onClick={() => setActiveLesson(lesson)}
                    >
                      <div className="cb-lesson-icon">
                        {lesson.lesson_type === 'video' ? <MonitorPlay size={14}/> : <FileText size={14}/>}
                      </div>
                      <span className="cb-lesson-title">{lesson.title}</span>
                    </div>
                  ))}
                  
                  {showLessonForm && activeModule === mod.id ? (
                    <div className="cb-add-inline">
                      <input 
                        type="text" 
                        autoFocus
                        placeholder="Lesson title..." 
                        value={newLessonTitle}
                        onChange={e => setNewLessonTitle(e.target.value)}
                        onKeyDown={e => e.key === 'Enter' && handleAddLesson()}
                      />
                      <button onClick={handleAddLesson}>Add</button>
                    </div>
                  ) : (
                    <div className="cb-add-btn" onClick={() => { setActiveModule(mod.id); setShowLessonForm(true); }}>
                      + Add lesson
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
          
          {showModuleForm ? (
            <div className="cb-add-inline" style={{marginTop: '15px'}}>
              <input 
                type="text" 
                autoFocus
                placeholder="Module title..." 
                value={newModuleTitle}
                onChange={e => setNewModuleTitle(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleAddModule()}
              />
              <button onClick={handleAddModule}>Add</button>
            </div>
          ) : (
            <div className="cb-add-module-btn" onClick={() => setShowModuleForm(true)}>
              + Add module
            </div>
          )}
        </div>
      </div>

      {/* MAIN EDITOR */}
      <div className="cb-main">
        {activeLesson ? (
          <>
            <div className="cb-main-header">
              <div className="cb-breadcrumb">
                {modules.find(m => m.id === activeLesson.module_id)?.title} / {activeLesson.lesson_type === 'video' ? 'Lecture' : 'Text'}
              </div>
              <div className="cb-main-actions">
                <button className="cb-publish-btn" onClick={handleSaveLesson}>Publish lesson</button>
                <button className="cb-icon-btn"><Plus size={18}/></button>
                <button className="cb-icon-btn"><Trash2 size={18}/></button>
              </div>
            </div>

            <div className="cb-editor-container">
              <input 
                className="cb-editor-title" 
                value={activeLesson.title} 
                onChange={e => setActiveLesson({...activeLesson, title: e.target.value})}
                placeholder="Lesson Title"
              />

              <div className="cb-cover-area">
                <div className="cb-cover-placeholder">
                  {activeLesson.video_url ? (
                    <div style={{color: '#fff', fontSize: '18px'}}>Video: {activeLesson.video_url}</div>
                  ) : (
                    <MonitorPlay size={48} color="rgba(255,255,255,0.8)" />
                  )}
                  <button className="cb-cover-edit-btn" onClick={() => {
                    const url = prompt("Video URL kiriting:", activeLesson.video_url || "");
                    if(url !== null) setActiveLesson({...activeLesson, video_url: url, lesson_type: 'video'});
                  }}>
                    <Edit3 size={16}/> Edit video
                  </button>
                </div>
              </div>

              <div className="cb-toolbar">
                <div className="cb-tool"><div className="cb-tool-icon"><FileText size={18}/></div><span>Text</span></div>
                <div className="cb-tool"><div className="cb-tool-icon"><Video size={18}/></div><span>Video</span></div>
                <div className="cb-tool"><div className="cb-tool-icon"><ImageIcon size={18}/></div><span>Image</span></div>
                <div className="cb-tool active"><div className="cb-tool-icon"><File size={18} color="#FF5F00"/></div><span style={{color: '#FF5F00'}}>File</span></div>
                <div className="cb-tool"><div className="cb-tool-icon"><MonitorPlay size={18}/></div><span>Presentation</span></div>
                <div className="cb-tool"><div className="cb-tool-icon"><Table size={18}/></div><span>Table</span></div>
              </div>

              <div className="cb-content-editor">
                <textarea 
                  placeholder="Type '/' for commands or start writing..."
                  value={activeLesson.content || ''}
                  onChange={e => setActiveLesson({...activeLesson, content: e.target.value})}
                ></textarea>
              </div>
            </div>
          </>
        ) : (
          <div className="cb-empty-state">
            <LayoutList size={48} color="#ccc" />
            <h3>Dars tanlanmagan</h3>
            <p>Chap menyudan modul yoki dars tanlang</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CourseBuilder;
