import React from 'react';

const StudentDashboard = () => {
  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Mening Kabinetim</h1>
        <p>Kurslardagi jarayon va vazifalar</p>
      </div>
      <div className="card glass-panel">
        <div className="content-placeholder" style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
          O'quvchi statistikasi tez orada qo'shiladi...
        </div>
      </div>
    </div>
  );
};

export default StudentDashboard;
