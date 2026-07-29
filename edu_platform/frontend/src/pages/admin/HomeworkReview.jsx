import React, { useState, useEffect } from 'react';
import { Check, X, AlertCircle } from 'lucide-react';
import { api } from '../../api';
import './HomeworkReview.css';

const HomeworkReview = () => {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  const [activeSubmission, setActiveSubmission] = useState(null);
  const [grade, setGrade] = useState('');
  const [feedback, setFeedback] = useState('');
  const [status, setStatus] = useState('Approved');

  useEffect(() => {
    fetchSubmissions();
  }, []);

  const fetchSubmissions = async () => {
    try {
      const data = await api('/homeworks/');
      setSubmissions(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleGradeSubmit = async (e) => {
    e.preventDefault();
    try {
      await api(`/homeworks/${activeSubmission.id}/grade`, {
        method: 'POST',
        body: {
          grade: parseInt(grade),
          status: status,
          feedback: feedback
        }
      });
      setActiveSubmission(null);
      fetchSubmissions();
    } catch (err) {
      console.error(err);
    }
  };

  const openGradeModal = (sub) => {
    setActiveSubmission(sub);
    setGrade(sub.grade || '');
    setFeedback(sub.feedback || '');
    setStatus(sub.status !== 'Sent for Review' ? sub.status : 'Approved');
  };

  const getStatusBadge = (statusStr) => {
    switch(statusStr) {
      case 'Approved': return <span className="badge badge-success">Qabul qilindi</span>;
      case 'Rejected': return <span className="badge badge-danger">Rad etildi</span>;
      default: return <span className="badge badge-warning">Kutilmoqda</span>;
    }
  };

  return (
    <div className="homework-review">
      <div className="review-header">
        <h1>Uy Vazifalarini Tekshirish</h1>
        <p>O'quvchilar yuborgan vazifalarni tekshiring va baholang</p>
      </div>

      {loading ? (
        <div className="p-8 text-center text-muted">Yuklanmoqda...</div>
      ) : submissions.length === 0 ? (
        <div className="empty-state card">
          <AlertCircle size={48} className="icon-muted" />
          <h3>Vazifalar yo'q</h3>
          <p>Hozircha tekshirilmagan vazifalar mavjud emas.</p>
        </div>
      ) : (
        <div className="submissions-grid">
          {submissions.map(sub => (
            <div key={sub.id} className="submission-card card">
              <div className="sub-header">
                <span className="text-muted text-sm">Dars ID: {sub.lesson_id}</span>
                {getStatusBadge(sub.status)}
              </div>
              <div className="sub-body">
                <p className="sub-text">{sub.submission_text}</p>
              </div>
              <div className="sub-footer">
                <div className="sub-meta">
                  {sub.grade !== null && <strong>Baho: {sub.grade}</strong>}
                </div>
                <button
                  className="btn-outline btn-sm"
                  onClick={() => openGradeModal(sub)}
                >
                  Tekshirish
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {}
      {activeSubmission && (
        <div className="modal-overlay">
          <div className="modal-content card">
            <h3>Vazifani Baholash</h3>
            <div className="student-submission-box">
              <p>{activeSubmission.submission_text}</p>
            </div>

            <form onSubmit={handleGradeSubmit}>
              <div className="form-group">
                <label>Holati</label>
                <div className="status-toggle">
                  <button
                    type="button"
                    className={`toggle-btn ${status === 'Approved' ? 'active-success' : ''}`}
                    onClick={() => setStatus('Approved')}
                  >
                    <Check size={16} /> Qabul qilish
                  </button>
                  <button
                    type="button"
                    className={`toggle-btn ${status === 'Rejected' ? 'active-danger' : ''}`}
                    onClick={() => setStatus('Rejected')}
                  >
                    <X size={16} /> Rad etish
                  </button>
                </div>
              </div>

              <div className="form-group">
                <label>Baho (0-100 yoki 1-5)</label>
                <input
                  type="number"
                  value={grade}
                  onChange={(e) => setGrade(e.target.value)}
                  placeholder="Masalan: 5 yoki 100"
                  required
                />
              </div>

              <div className="form-group">
                <label>Fikr / Xatolar</label>
                <textarea
                  rows="3"
                  value={feedback}
                  onChange={(e) => setFeedback(e.target.value)}
                  placeholder="O'quvchiga tavsiya yoki fikringiz..."
                ></textarea>
              </div>

              <div className="modal-actions">
                <button type="button" className="btn-outline" onClick={() => setActiveSubmission(null)}>Bekor qilish</button>
                <button type="submit" className="btn-primary">Saqlash</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomeworkReview;
