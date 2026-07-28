import React, { useState } from 'react';
import { Send, CheckCircle } from 'lucide-react';
import './HomeworkForm.css';

const HomeworkForm = ({ lessonId }) => {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      // Assume student ID is decoded from token in a real app, for MVP we pass a mocked one or backend reads from token
      // Wait, backend requires student_id in schema. Let's assume backend extracts it from Depends(get_current_user) in future.
      // For MVP without JWT decode in frontend, let's just mock student_id:
      const mockStudentId = "00000000-0000-0000-0000-000000000000"; // Fake UUID

      const response = await fetch('http://localhost:8000/api/v1/homeworks/', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          lesson_id: lessonId,
          student_id: mockStudentId,
          submission_text: text
        })
      });

      if (response.ok) {
        setSubmitted(true);
      }
    } catch (err) {
      console.error("Uy vazifasini yuborishda xatolik", err);
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <div className="homework-success card">
        <CheckCircle size={32} className="success-icon" />
        <h3>Vazifa yuborildi!</h3>
        <p>Kuratorlar tez orada tekshirib baholaydilar.</p>
      </div>
    );
  }

  return (
    <div className="homework-form-container card">
      <h3>Uy Vazifasi</h3>
      <p className="text-muted" style={{marginBottom: '16px'}}>Dars bo'yicha amaliy vazifani shu yerga yozing yoki fayl havolasini (masalan Github, Google Drive) qoldiring.</p>
      
      <form onSubmit={handleSubmit}>
        <textarea
          className="homework-textarea"
          rows="5"
          placeholder="Javobingizni shu yerga yozing..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        ></textarea>
        
        <div className="form-footer">
          <button type="submit" className="btn-primary" disabled={loading || !text.trim()}>
            {loading ? 'Yuborilmoqda...' : <><Send size={18} style={{marginRight: '8px'}} /> Yuborish</>}
          </button>
        </div>
      </form>
    </div>
  );
};

export default HomeworkForm;
