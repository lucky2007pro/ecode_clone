import React from 'react';
import { CreditCard } from 'lucide-react';

const Payments = () => {
  return (
    <div className="page-container">
      <div className="page-header" style={{ marginBottom: '20px' }}>
        <h1>To'lovlar</h1>
        <p className="text-muted">Maktab bo'yicha barcha kirim va chiqim operatsiyalari</p>
      </div>

      <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
        <CreditCard size={48} style={{ margin: '0 auto', marginBottom: '16px', opacity: 0.5 }} />
        <h2>To'lovlar</h2>
        <p className="text-muted">To'lov integratsiyalari (Payme, Click, Uzum) hozircha ishlab chiqilmoqda. Tez orada!</p>
      </div>
    </div>
  );
};

export default Payments;
