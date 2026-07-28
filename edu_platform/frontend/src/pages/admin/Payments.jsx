import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../../context/AuthContext';
import { CreditCard, TrendingUp, TrendingDown, Clock, Search, Filter } from 'lucide-react';

const Payments = () => {
  const { school, user } = useContext(AuthContext);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (school) {
      fetchTransactions();
    }
  }, [school]);

  const fetchTransactions = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/payments/transactions/${school.id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setTransactions(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading-state"><div className="spinner"></div></div>;

  return (
    <div className="payments-container">
      <div className="page-header" style={{ marginBottom: '20px' }}>
        <h1>To'lovlar va Tranzaksiyalar</h1>
        <p className="text-muted">Maktab bo'yicha barcha kirim va chiqim operatsiyalari</p>
      </div>

      <div className="transactions-card card">
        <div className="transactions-header" style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div className="search-box" style={{ display: 'flex', alignItems: 'center', background: '#f8fafc', padding: '8px 12px', borderRadius: '8px', border: '1px solid #e2e8f0', width: '300px' }}>
            <Search size={18} className="text-muted" style={{ marginRight: '8px' }} />
            <input type="text" placeholder="Tranzaksiya izlash..." style={{ border: 'none', background: 'transparent', outline: 'none', width: '100%' }} />
          </div>
          <button className="btn-secondary" style={{ display: 'flex', alignItems: 'center' }}>
            <Filter size={18} style={{marginRight: '8px'}} /> Filtr
          </button>
        </div>

        <div className="table-responsive">
          <table className="data-table mt-4" style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #e2e8f0', textAlign: 'left' }}>
                <th style={{ padding: '12px' }}>Sana</th>
                <th style={{ padding: '12px' }}>Tavsif</th>
                <th style={{ padding: '12px' }}>Turi</th>
                <th style={{ padding: '12px' }}>Miqdor (UZS)</th>
                <th style={{ padding: '12px' }}>Holat</th>
              </tr>
            </thead>
            <tbody>
              {transactions.length > 0 ? transactions.map(t => (
                <tr key={t.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <Clock size={16} className="text-muted" />
                      {new Date(t.created_at).toLocaleString('uz-UZ')}
                    </div>
                  </td>
                  <td style={{ fontWeight: '500', padding: '12px' }}>{t.description}</td>
                  <td style={{ padding: '12px' }}>
                    {t.type === 'in' ? (
                      <span className="badge" style={{ background: '#dcfce7', color: '#166534', padding: '4px 8px', borderRadius: '12px', display: 'inline-flex', alignItems: 'center', fontSize: '12px' }}>
                        <TrendingUp size={14} style={{marginRight: '4px'}} /> Kirim
                      </span>
                    ) : (
                      <span className="badge" style={{ background: '#fee2e2', color: '#991b1b', padding: '4px 8px', borderRadius: '12px', display: 'inline-flex', alignItems: 'center', fontSize: '12px' }}>
                        <TrendingDown size={14} style={{marginRight: '4px'}} /> Chiqim
                      </span>
                    )}
                  </td>
                  <td style={{ fontWeight: 'bold', padding: '12px', color: t.type === 'in' ? '#16a34a' : '#ef4444' }}>
                    {t.type === 'in' ? '+' : '-'}{t.amount.toLocaleString()}
                  </td>
                  <td style={{ padding: '12px' }}>
                    <span className="badge" style={{ background: '#dcfce7', color: '#166534', padding: '4px 8px', borderRadius: '12px', fontSize: '12px' }}>Muvaffaqiyatli</span>
                  </td>
                </tr>
              )) : (
                <tr>
                  <td colSpan="5" style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>
                    <CreditCard size={48} style={{ margin: '0 auto', marginBottom: '16px', opacity: 0.5 }} />
                    <p>Hozircha tranzaksiyalar yo'q</p>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Payments;
