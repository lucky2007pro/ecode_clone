import React, { useState, useEffect, useContext } from 'react';
import { CreditCard, ArrowUpRight, ArrowDownRight, Search } from 'lucide-react';
import { api } from '../../api';
import { AuthContext } from '../../context/auth-context';

const Payments = () => {
  const { school } = useContext(AuthContext);
  const [transactions, setTransactions] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  const [selectedUserId, setSelectedUserId] = useState('');
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [topupLoading, setTopupLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, [school]);

  const fetchData = async () => {
    if (!school?.id) return;
    setLoading(true);
    try {
      const [txRes, usersRes] = await Promise.allSettled([
        api('/payments/transactions'),
        api(`/schools/${school.id}/users`)
      ]);

      if (txRes.status === 'fulfilled' && Array.isArray(txRes.value)) {
        setTransactions(txRes.value);
      }

      if (usersRes.status === 'fulfilled' && Array.isArray(usersRes.value)) {
        const allUsers = usersRes.value;
        const studentOnly = allUsers.filter(u => u.role && u.role.toString().toLowerCase() === 'student');
        setStudents(studentOnly.length > 0 ? studentOnly : allUsers);
      }
    } catch (err) {
      console.error("Ma'lumotlarni yuklashda xatolik:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleTopup = async (e) => {
    e.preventDefault();
    if (!selectedUserId || !amount || parseFloat(amount) <= 0) {
      alert("Foydalanuvchi va to'g'ri summa kiriting.");
      return;
    }
    setTopupLoading(true);
    try {
      await api('/payments/topup', {
        method: 'POST',
        body: {
          user_id: selectedUserId,
          amount: parseFloat(amount),
          description: description || "Balans to'ldirish"
        }
      });
      alert("Balans muvaffaqiyatli to'ldirildi!");
      setSelectedUserId('');
      setAmount('');
      setDescription('');
      fetchData();
    } catch (err) {
      alert(err.message || "Xatolik yuz berdi");
    } finally {
      setTopupLoading(false);
    }
  };

  return (
    <div className="page-container">
      <div className="page-header" style={{ marginBottom: '24px' }}>
        <h1>To'lovlar va Balans</h1>
        <p className="text-muted">Maktab bo'yicha barcha kirim va chiqim operatsiyalari</p>
      </div>

      <div className="payments-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px' }}>

        {}
        <div className="card glass-panel" style={{ height: 'fit-content' }}>
          <h2 style={{ fontSize: '18px', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CreditCard size={20} className="text-primary" /> Balansni to'ldirish
          </h2>
          <form onSubmit={handleTopup}>
            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontSize: '13px', fontWeight: '500' }}>O'quvchini tanlang</label>
              <select
                value={selectedUserId}
                onChange={e => setSelectedUserId(e.target.value)}
                style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-color)', background: 'var(--bg-primary)', color: 'var(--text-primary)' }}
                required
              >
                <option value="">-- Tanlang --</option>
                {students.map(s => (
                  <option key={s.id} value={s.id}>{s.full_name || s.email} (Balans: {Number(s.balance || 0).toLocaleString('uz-UZ')})</option>
                ))}
              </select>
            </div>
            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontSize: '13px', fontWeight: '500' }}>Summa (UZS)</label>
              <input
                type="number"
                value={amount}
                onChange={e => setAmount(e.target.value)}
                placeholder="Masalan, 150000"
                style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-color)', background: 'var(--bg-primary)', color: 'var(--text-primary)' }}
                required
              />
            </div>
            <div className="form-group" style={{ marginBottom: '16px' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontSize: '13px', fontWeight: '500' }}>Izoh (Ixtiyoriy)</label>
              <input
                type="text"
                value={description}
                onChange={e => setDescription(e.target.value)}
                placeholder="Naqd pul orqali to'landi..."
                style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid var(--border-color)', background: 'var(--bg-primary)', color: 'var(--text-primary)' }}
              />
            </div>
            <button type="submit" className="btn-primary full-width" disabled={topupLoading}>
              {topupLoading ? 'Yuklanmoqda...' : "Balansni to'ldirish"}
            </button>
          </form>
        </div>

        {}
        <div className="card glass-panel">
          <h2 style={{ fontSize: '18px', marginBottom: '16px' }}>Tranzaksiyalar tarixi</h2>

          {loading ? (
            <div style={{ padding: '40px', textAlign: 'center' }}>Yuklanmoqda...</div>
          ) : transactions.length === 0 ? (
            <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
              <CreditCard size={48} style={{ margin: '0 auto', marginBottom: '10px', opacity: 0.3 }} />
              <p>Hozircha hech qanday tranzaksiya yo'q.</p>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border-color)', textAlign: 'left', color: 'var(--text-muted)' }}>
                    <th style={{ padding: '12px 8px', fontWeight: '500' }}>Sana</th>
                    <th style={{ padding: '12px 8px', fontWeight: '500' }}>Tur</th>
                    <th style={{ padding: '12px 8px', fontWeight: '500' }}>Summa</th>
                    <th style={{ padding: '12px 8px', fontWeight: '500' }}>Izoh</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map(tx => {
                    const formatDate = (d) => {
                      if (!d) return '-';
                      try {
                        const s = String(d);
                        const iso = s.endsWith('Z') ? s : s + 'Z';
                        const dateObj = new Date(iso);
                        return isNaN(dateObj.getTime()) ? s : dateObj.toLocaleString('uz-UZ');
                      } catch {
                        return String(d);
                      }
                    };

                    return (
                      <tr key={tx.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                        <td style={{ padding: '12px 8px' }}>
                          {formatDate(tx.created_at)}
                        </td>
                        <td style={{ padding: '12px 8px' }}>
                          {tx.type === 'in' ? (
                            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: '#10b981', background: 'rgba(16, 185, 129, 0.1)', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>
                              <ArrowDownRight size={14} /> Kirim
                            </span>
                          ) : (
                            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', color: '#ef4444', background: 'rgba(239, 68, 68, 0.1)', padding: '4px 8px', borderRadius: '4px', fontSize: '12px' }}>
                              <ArrowUpRight size={14} /> Chiqim
                            </span>
                          )}
                        </td>
                        <td style={{ padding: '12px 8px', fontWeight: '600' }}>
                          {Number(tx.amount || 0).toLocaleString('uz-UZ')} UZS
                        </td>
                        <td style={{ padding: '12px 8px', color: 'var(--text-muted)', fontSize: '13px' }}>
                          {tx.description || '-'}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default Payments;
