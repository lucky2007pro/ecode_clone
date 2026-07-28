import React, { useState, useContext } from 'react';
import { Send, CheckCircle } from 'lucide-react';
import { AuthContext } from '../../context/AuthContext';
import { api } from '../../api';
import './HomeworkForm.css';

const HomeworkForm = ({ lessonId }) => {
  const { user } = useContext(AuthContext);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!text.trim() || !user) return;

    setLoading(true);
    setError('');
    try {
      await api('/homeworks/', {
        method: 'POST',
        body: {
          lesson_id: lessonId,
          student_id: user.id,
          submission_text: text
        }
      });

      setSubmitted(true);
    } catch (err) {
      setError(err.message || "Vazifani yuborishda xatolik yuz berdi");
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
        
        {error && <p style={{ color: 'var(--danger)', marginTop: '8px', fontSize: '13px' }}>{error}</p>}

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
