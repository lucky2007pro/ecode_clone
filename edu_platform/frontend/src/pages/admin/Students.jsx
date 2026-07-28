import React, { useState, useEffect, useContext } from 'react';
import { Users, Plus, X, UserCheck, Shield } from 'lucide-react';
import { AuthContext } from '../../context/AuthContext';

const Students = () => {
  const { school, user } = useContext(AuthContext);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [showProfileModal, setShowProfileModal] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [newUser, setNewUser] = useState({ full_name: '', email: '', password: '', role: 'student' });
  const [error, setError] = useState('');

  useEffect(() => {
    if (school) {
      fetchStudents();
    }
  }, [school]);

  const fetchStudents = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/schools/${school.id}/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setStudents(data);
      }
    } catch (err) {
      console.error("Xatolik:", err);
    } finally {
      setLoading(false);
    }
  };

  const [allCourses, setAllCourses] = useState([]);
  const [userCourses, setUserCourses] = useState([]);
  const [modalTab, setModalTab] = useState('info'); // 'info' or 'courses'
  const [selectedCourseId, setSelectedCourseId] = useState('');

  const fetchAllCourses = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/courses/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setAllCourses(data);
      }
    } catch (err) {
      console.error("Kurslarni yuklashda xatolik:", err);
    }
  };

  const fetchUserCourses = async (userId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/enrollments/user/${userId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setUserCourses(data);
      }
    } catch (err) {
      console.error("Foydalanuvchi kurslarini yuklashda xatolik:", err);
    }
  };

  useEffect(() => {
    fetchAllCourses();
  }, []);

  const handleAssignCourse = async () => {
    if (!selectedCourseId || !selectedStudent) return;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/enrollments/', {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: selectedStudent.id, course_id: selectedCourseId })
      });
      if (response.ok) {
        // Refresh the user's courses
        fetchUserCourses(selectedStudent.id);
        setSelectedCourseId('');
      } else {
        const data = await response.json();
        alert(data.detail || "Xatolik yuz berdi");
      }
    } catch (err) {
      alert("Serverga ulanishda xatolik");
    }
  };

  const handleUnassignCourse = async (enrollmentId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/enrollments/${enrollmentId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        fetchUserCourses(selectedStudent.id);
      } else {
        alert("O'chirishda xatolik yuz berdi");
      }
    } catch (err) {
      alert("Serverga ulanishda xatolik");
    }
  };

  // Faqat o'quvchiga hali biriktirilmagan kurslar ro'yxatini chiqaramiz
  const availableCourses = allCourses.filter(c => !userCourses.some(uc => uc.course_id === c.id));

  const handleCreateStudent = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/schools/${school.id}/users`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newUser)
      });
      
      if (response.ok) {
        const data = await response.json();
        setStudents([...students, data]);
        setShowModal(false);
        setNewUser({ full_name: '', email: '', password: '', role: 'student' });
      } else {
        const errData = await response.json();
        setError(errData.detail || 'Xatolik yuz berdi');
      }
    } catch (err) {
      setError("Serverga ulanishda xatolik");
    }
  };

  const getRoleStyle = (role) => {
    switch(role) {
      case 'admin': return { bg: '#fee2e2', color: '#991b1b', label: 'Admin' };
      case 'manager': return { bg: '#f3e8ff', color: '#6b21a8', label: 'Menejer' };
      case 'accountant': return { bg: '#dcfce7', color: '#166534', label: 'Buxgalter' };
      case 'teacher': return { bg: '#e0f2fe', color: '#075985', label: "O'qituvchi" };
      case 'curator': return { bg: '#fef3c7', color: '#92400e', label: 'Kurator' };
      case 'student':
      default: return { bg: '#e0e7ff', color: '#3730a3', label: "O'quvchi" };
    }
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>O'quvchilar boshqaruvi</h1>
          <p>Maktabingizdagi barcha o'quvchilar va xodimlar ro'yxati</p>
        </div>
        {(!user || user.role !== 'teacher') && (
          <button className="btn-primary" onClick={() => setShowModal(true)}>
            <Plus size={18} style={{ marginRight: '8px' }} /> O'quvchi Qo'shish
          </button>
        )}
      </div>

      <div className="card glass-panel" style={{ padding: '20px' }}>
        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px' }}>Yuklanmoqda...</div>
        ) : students.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#6b7280' }}>
            <Users size={48} style={{ opacity: 0.5, marginBottom: '10px' }} />
            <h3>Hozircha o'quvchilar yo'q</h3>
          </div>
        ) : (
          <>
            <style>
              {`
                .student-row:hover { background-color: #f9fafb; cursor: pointer; }
              `}
            </style>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e5e7eb' }}>
                  <th style={{ padding: '12px', color: '#6b7280' }}>Ism Familiya</th>
                  <th style={{ padding: '12px', color: '#6b7280' }}>Email</th>
                  <th style={{ padding: '12px', color: '#6b7280' }}>Rol</th>
                  <th style={{ padding: '12px', color: '#6b7280' }}>Holat</th>
                </tr>
              </thead>
              <tbody>
              {students.map((student) => (
                <tr 
                  key={student.id} 
                  className="student-row"
                  style={{ borderBottom: '1px solid #e5e7eb' }}
                  onClick={() => {
                    setSelectedStudent(student);
                    setModalTab('info');
                    fetchUserCourses(student.id);
                    setShowProfileModal(true);
                  }}
                >
                  <td style={{ padding: '12px', fontWeight: '500' }}>{student.full_name}</td>
                  <td style={{ padding: '12px', color: '#6b7280' }}>{student.email}</td>
                  <td style={{ padding: '12px' }}>
                    <span style={{ 
                      padding: '4px 8px', borderRadius: '4px', fontSize: '12px',
                      background: getRoleStyle(student.role).bg,
                      color: getRoleStyle(student.role).color,
                      fontWeight: '500'
                    }}>
                      {getRoleStyle(student.role).label}
                    </span>
                  </td>
                  <td style={{ padding: '12px', color: '#059669' }}>
                    <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}><UserCheck size={16} /> Faol</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          </>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="modal-content card" style={{ width: '400px', padding: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
              <h2>Yangi O'quvchi / Xodim</h2>
              <button className="icon-btn" onClick={() => setShowModal(false)}><X size={20} /></button>
            </div>
            
            {error && <div style={{ padding: '10px', background: '#fee2e2', color: '#b91c1c', borderRadius: '8px', marginBottom: '15px' }}>{error}</div>}
            
            <form onSubmit={handleCreateStudent}>
              <div className="form-group" style={{ marginBottom: '15px' }}>
                <label>To'liq Ism</label>
                <input type="text" value={newUser.full_name} onChange={e => setNewUser({...newUser, full_name: e.target.value})} required style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #e5e7eb' }} />
              </div>
              <div className="form-group" style={{ marginBottom: '15px' }}>
                <label>Email</label>
                <input type="email" value={newUser.email} onChange={e => setNewUser({...newUser, email: e.target.value})} required style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #e5e7eb' }} />
              </div>
              <div className="form-group" style={{ marginBottom: '15px' }}>
                <label>Vaqtinchalik Parol</label>
                <input type="text" value={newUser.password} onChange={e => setNewUser({...newUser, password: e.target.value})} required style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #e5e7eb' }} />
              </div>
              <div className="form-group" style={{ marginBottom: '20px' }}>
                <label>Rol</label>
                <select value={newUser.role} onChange={e => setNewUser({...newUser, role: e.target.value})} style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
                  <option value="student">O'quvchi</option>
                  <option value="curator">Kurator / Mentor</option>
                  <option value="teacher">O'qituvchi</option>
                  <option value="manager">Menejer</option>
                  <option value="accountant">Buxgalter</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <button type="submit" className="btn-primary" style={{ width: '100%' }}>Qo'shish</button>
            </form>
          </div>
        </div>
      )}

      {showProfileModal && selectedStudent && (
        <div className="modal-overlay" style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="modal-content card" style={{ width: '500px', padding: '0', overflow: 'hidden' }}>
            <div style={{ padding: '24px', borderBottom: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
                <div style={{ width: '50px', height: '50px', borderRadius: '50%', backgroundColor: getRoleStyle(selectedStudent.role).bg, color: getRoleStyle(selectedStudent.role).color, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', fontWeight: 'bold' }}>
                  {selectedStudent.full_name.charAt(0).toUpperCase()}
                </div>
                <div>
                  <h2 style={{ margin: 0, fontSize: '18px' }}>{selectedStudent.full_name}</h2>
                  <span style={{ 
                      padding: '2px 6px', borderRadius: '4px', fontSize: '11px',
                      background: getRoleStyle(selectedStudent.role).bg,
                      color: getRoleStyle(selectedStudent.role).color,
                      fontWeight: '500', display: 'inline-block', marginTop: '4px'
                    }}>
                      {getRoleStyle(selectedStudent.role).label}
                  </span>
                </div>
              </div>
              <button className="icon-btn" onClick={() => setShowProfileModal(false)}><X size={20} /></button>
            </div>
            
            <div style={{ padding: '24px' }}>
              <div style={{ display: 'flex', gap: '20px', borderBottom: '1px solid #e5e7eb', marginBottom: '20px' }}>
                <button 
                  onClick={() => setModalTab('info')}
                  style={{ padding: '10px 0', border: 'none', background: 'none', borderBottom: modalTab === 'info' ? '2px solid var(--primary-color)' : '2px solid transparent', color: modalTab === 'info' ? 'var(--primary-color)' : '#6b7280', fontWeight: '600', cursor: 'pointer' }}>
                  Ma'lumotlar
                </button>
                <button 
                  onClick={() => setModalTab('courses')}
                  style={{ padding: '10px 0', border: 'none', background: 'none', borderBottom: modalTab === 'courses' ? '2px solid var(--primary-color)' : '2px solid transparent', color: modalTab === 'courses' ? 'var(--primary-color)' : '#6b7280', fontWeight: '600', cursor: 'pointer' }}>
                  Kurslar
                </button>
              </div>

              {modalTab === 'info' && (
                <div>
                  <div className="form-group" style={{ marginBottom: '15px' }}>
                    <label>Email</label>
                    <input type="text" value={selectedStudent.email} disabled style={{ width: '100%', padding: '10px', borderRadius: '8px', border: '1px solid #e5e7eb', backgroundColor: '#f9fafb' }} />
                  </div>
                  <p style={{ color: '#6b7280', fontSize: '13px', textAlign: 'center', marginTop: '30px' }}>
                    Foydalanuvchi ma'lumotlarini tahrirlash funksiyasi tayyorlanmoqda.
                  </p>
                </div>
              )}

              {modalTab === 'courses' && (
                <div>
                  <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
                    <select 
                      value={selectedCourseId} 
                      onChange={e => setSelectedCourseId(e.target.value)} 
                      style={{ flex: 1, padding: '10px', borderRadius: '8px', border: '1px solid #e5e7eb' }}
                    >
                      <option value="">-- Kursni tanlang --</option>
                      {availableCourses.map(c => (
                        <option key={c.id} value={c.id}>{c.title}</option>
                      ))}
                    </select>
                    <button className="btn-primary" onClick={handleAssignCourse} disabled={!selectedCourseId || availableCourses.length === 0}>
                      Biriktirish
                    </button>
                  </div>
                  
                  <h4>Biriktirilgan kurslar:</h4>
                  {userCourses.length === 0 ? (
                    <p style={{ color: '#6b7280', fontSize: '14px' }}>Hozircha kurslar biriktirilmagan.</p>
                  ) : (
                    <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                      {userCourses.map(uc => {
                        const courseObj = allCourses.find(c => c.id === uc.course_id);
                        return (
                          <li key={uc.id} style={{ padding: '12px', border: '1px solid #e5e7eb', borderRadius: '8px', marginBottom: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                            <span style={{ fontWeight: '500' }}>{courseObj ? courseObj.title : 'Noma\'lum kurs'}</span>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                              <span style={{ fontSize: '12px', color: '#10b981', background: '#d1fae5', padding: '2px 8px', borderRadius: '12px' }}>{uc.status}</span>
                              <button 
                                onClick={() => handleUnassignCourse(uc.id)}
                                style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', display: 'flex', alignItems: 'center' }}
                                title="Kursni olib tashlash"
                              >
                                <X size={16} />
                              </button>
                            </div>
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Students;
