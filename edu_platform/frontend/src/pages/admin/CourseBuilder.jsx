import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Plus, Video, FileText, LayoutList, ChevronDown, ChevronRight, Settings, Image as ImageIcon, File, MonitorPlay, MessageSquare, Table, Edit3, Trash2 } from 'lucide-react';
import { api, API_ORIGIN } from '../../api';
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
  const [error, setError] = useState('');
  const [uploading, setUploading] = useState(false);
  const [activeTool, setActiveTool] = useState('Text');
  const videoInputRef = useRef(null);
  const imageInputRef = useRef(null);
  const fileInputRef = useRef(null);
  const presentationInputRef = useRef(null);
  const contentRef = useRef(null);

  // Expand/Collapse modules
  const [expandedModules, setExpandedModules] = useState({});

  useEffect(() => {
    fetchCourseDetails();
    fetchModulesAndLessons();
  }, [id]);

  const fetchCourseDetails = async () => {
    try {
      setCourse(await api(`/courses/${id}`));
    } catch(err) {
      setError(err.message || "Kurs ma'lumotlarini yuklashda xatolik");
    }
  };

  const fetchModulesAndLessons = async () => {
    try {
      const [mods, less] = await Promise.all([
        api(`/lessons/course/${id}/modules`).catch(() => []),
        api(`/lessons/course/${id}`).catch(() => [])
      ]);

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
    setError('');
    try {
      await api(`/lessons/modules`, {
        method: 'POST',
        body: { course_id: id, title: newModuleTitle, order: modules.length + 1 }
      });
      setNewModuleTitle('');
      setShowModuleForm(false);
      fetchModulesAndLessons();
    } catch(err) { setError(err.message || 'Serverga ulanishda xatolik'); }
  };

  const handleAddLesson = async () => {
    if(!newLessonTitle.trim() || !activeModule) return;
    setError('');
    try {
      const modLessons = lessons.filter(l => l.module_id === activeModule);
      const newL = await api(`/lessons/`, {
        method: 'POST',
        body: {
          course_id: id,
          module_id: activeModule,
          title: newLessonTitle,
          lesson_type: 'video',
          order: modLessons.length + 1
        }
      });
      setNewLessonTitle('');
      setShowLessonForm(false);
      setActiveLesson(newL);
      fetchModulesAndLessons();
    } catch(err) { setError(err.message || 'Serverga ulanishda xatolik'); }
  };

  const toggleModule = (modId) => {
    setExpandedModules(prev => ({...prev, [modId]: !prev[modId]}));
  };

  const handleDeleteLesson = async () => {
    if (!activeLesson) return;
    if (!window.confirm(`"${activeLesson.title}" darsini o'chirishga ishonchingiz komilmi?`)) return;
    setError('');
    try {
      await api(`/lessons/${activeLesson.id}`, { method: 'DELETE' });
      setActiveLesson(null);
      fetchModulesAndLessons();
    } catch(err) { setError(err.message || "Darsni o'chirishda xatolik"); }
  };

  const handleSaveLesson = async () => {
    if(!activeLesson) return;
    try {
      await api(`/lessons/${activeLesson.id}`, {
        method: 'PUT',
        body: activeLesson
      });
      alert("Saqlandi!");
      fetchModulesAndLessons();
    } catch(err) { console.error(err); }
  };

  const insertToContent = (snippet) => {
    setActiveLesson(prev => ({ ...prev, content: `${prev.content || ''}\n${snippet}\n` }));
  };

  const handleVideoUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file || !activeLesson) return;
    setError('');
    setUploading(true);
    try {
      try {
        // Kinescope sozlangan bo'lsa — to'g'ridan-to'g'ri u yerga yuklaymiz
        const initData = await api('/videos/upload/init', {
          method: 'POST',
          body: { filename: file.name, title: activeLesson.title, filesize: file.size },
        });
        const { Upload } = await import('tus-js-client');
        await new Promise((resolve, reject) => {
          const upload = new Upload(file, {
            uploadUrl: initData.upload_url,
            chunkSize: 10 * 1024 * 1024,
            retryDelays: [0, 3000, 5000, 10000],
            metadata: { filename: file.name, filetype: file.type },
            onError: reject,
            onSuccess: resolve,
          });
          upload.start();
        });
        const videoUrl = initData.video_id ? `https://kinescope.io/embed/${initData.video_id}` : initData.upload_url;
        setActiveLesson({ ...activeLesson, video_url: videoUrl, lesson_type: 'video' });
        setError("Video Kinescope'ga yuklandi. Saqlash uchun 'Publish lesson'ni bosing.");
      } catch (kinescopeErr) {
        // Kinescope sozlanmagan bo'lsa — lokal serverga yuklaymiz
        if (!String(kinescopeErr.message).includes('sozlanmagan')) throw kinescopeErr;
        const form = new FormData();
        form.append('file', file);
        const res = await api('/videos/upload', { method: 'POST', body: form });
        setActiveLesson({ ...activeLesson, video_url: `${API_ORIGIN}${res.video_url}`, lesson_type: 'video' });
        setError("");
      }
    } catch (err) {
      setError(err.message || 'Video yuklashda xatolik');
    } finally {
      setUploading(false);
      event.target.value = '';
    }
  };

  const handleAssetUpload = async (event, kind) => {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file || !activeLesson) return;
    setError('');
    setUploading(true);
    try {
      const form = new FormData();
      form.append('file', file);
      const res = await api('/videos/upload/asset', { method: 'POST', body: form });
      const url = `${API_ORIGIN}${res.url}`;
      insertToContent(kind === 'Image' ? `![${res.filename}](${url})` : `[${res.filename}](${url})`);
    } catch (err) {
      setError(err.message || 'Fayl yuklashda xatolik');
    } finally {
      setUploading(false);
    }
  };

  const handleToolClick = (tool) => {
    setActiveTool(tool);
    if (tool === 'Text') {
      contentRef.current?.focus();
    } else if (tool === 'Video') {
      videoInputRef.current?.click();
    } else if (tool === 'Image') {
      imageInputRef.current?.click();
    } else if (tool === 'File') {
      fileInputRef.current?.click();
    } else if (tool === 'Presentation') {
      presentationInputRef.current?.click();
    } else if (tool === 'Table') {
      insertToContent('| Ustun 1 | Ustun 2 |\n| --- | --- |\n|  |  |');
      contentRef.current?.focus();
    }
  };

  const TOOLS = [
    { name: 'Text', icon: <FileText size={18}/> },
    { name: 'Video', icon: <Video size={18}/> },
    { name: 'Image', icon: <ImageIcon size={18}/> },
    { name: 'File', icon: <File size={18}/> },
    { name: 'Presentation', icon: <MonitorPlay size={18}/> },
    { name: 'Table', icon: <Table size={18}/> },
  ];

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
          {error && <div style={{color: '#b91c1c', background: '#fee2e2', padding: '10px', borderRadius: '8px', marginBottom: '12px', fontSize: '13px'}}>{error}</div>}
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
                <button className="cb-icon-btn" onClick={handleDeleteLesson}><Trash2 size={18}/></button>
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
                    activeLesson.video_url.includes('kinescope') ? (
                      <div style={{color: '#fff', fontSize: '18px'}}>Video: {activeLesson.video_url}</div>
                    ) : (
                      <video controls src={activeLesson.video_url} style={{maxWidth: '100%', maxHeight: '100%'}} />
                    )
                  ) : (
                    <MonitorPlay size={48} color="rgba(255,255,255,0.8)" />
                  )}
                  <button className="cb-cover-edit-btn" onClick={() => videoInputRef.current?.click()} disabled={uploading}>
                    <Edit3 size={16}/> {uploading ? 'Uploading...' : 'Upload video'}
                  </button>
                  <input ref={videoInputRef} type="file" accept="video/*" hidden onChange={handleVideoUpload} />
                  <input ref={imageInputRef} type="file" accept="image/*" hidden onChange={e => handleAssetUpload(e, 'Image')} />
                  <input ref={fileInputRef} type="file" hidden onChange={e => handleAssetUpload(e, 'File')} />
                  <input ref={presentationInputRef} type="file" accept=".pdf,.ppt,.pptx,.key,.odp" hidden onChange={e => handleAssetUpload(e, 'Presentation')} />
                </div>
              </div>

              <div className="cb-toolbar">
                {TOOLS.map(tool => (
                  <div
                    key={tool.name}
                    className={`cb-tool ${activeTool === tool.name ? 'active' : ''}`}
                    onClick={() => handleToolClick(tool.name)}
                    style={{cursor: 'pointer'}}
                  >
                    <div className="cb-tool-icon">{tool.icon}</div>
                    <span style={activeTool === tool.name ? {color: '#FF5F00'} : undefined}>{tool.name}</span>
                  </div>
                ))}
              </div>

              <div className="cb-content-editor">
                <textarea
                  ref={contentRef}
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
