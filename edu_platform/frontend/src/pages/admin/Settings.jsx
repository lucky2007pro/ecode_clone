import React, { useState, useEffect, useContext } from 'react';
import { Palette, Globe, User, Save, CheckCircle, Target, MessageCircle, Key, Briefcase, CreditCard } from 'lucide-react';
import { AuthContext } from '../../context/AuthContext';
import { api } from '../../api';
import './Settings.css';

const Settings = () => {
  const { user, school, refreshUser } = useContext(AuthContext);
  const [activeTab, setActiveTab] = useState('school');
  const [schoolData, setSchoolData] = useState({ name: school?.name || '', custom_domain: school?.custom_domain || '', primary_color: school?.primary_color || '#3b82f6' });
  const [userData, setUserData] = useState({ full_name: user?.full_name || '', email: user?.email || '' });
  const [marketingData, setMarketingData] = useState({ facebook_pixel_id: '', google_analytics_id: '', yandex_metrika_id: '' });
  const [botData, setBotData] = useState({ bot_token: '', private_channel_id: '', invite_link: '' });
  const [kommoData, setKommoData] = useState({ subdomain: '', client_id: '', client_secret: '', access_token: '' });
  const [apiKeyName, setApiKeyName] = useState('');
  const [generatedKey, setGeneratedKey] = useState(null);
  const [saved, setSaved] = useState(false);
  const [profileError, setProfileError] = useState('');
  const [plans, setPlans] = useState([]);
  const [subscription, setSubscription] = useState(null);
  const [subLoading, setSubLoading] = useState(false);
  const [subMessage, setSubMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    if (activeTab === 'subscription') {
      (async () => {
        try {
          const [plansData, subData] = await Promise.all([
            api('/payments/plans'),
            api('/payments/school-subscription'),
          ]);
          setPlans(plansData || []);
          setSubscription(subData);
        } catch (err) { console.error(err); }
      })();
    }
  }, [activeTab]);

  const handleSubscribe = async (planId) => {
    setSubLoading(true);
    setSubMessage({ type: '', text: '' });
    try {
      const sub = await api('/payments/subscribe', { method: 'POST', body: { plan_id: planId } });
      setSubscription(sub);
      setSubMessage({ type: 'success', text: 'Obuna muvaffaqiyatli faollashtirildi!' });
      await refreshUser();
    } catch (err) {
      setSubMessage({ type: 'error', text: err.message || "To'lovda xatolik yuz berdi" });
    }
    setSubLoading(false);
  };

  useEffect(() => {
    if (school) {
      setSchoolData({ name: school.name, custom_domain: school.custom_domain || '', primary_color: school.primary_color || '#3b82f6' });
    }
    if (user) {
      setUserData({ full_name: user.full_name, email: user.email });
    }
  }, [school, user]);

  const schoolId = school?.id;

  // When color changes, apply to the CSS variable dynamically for the preview
  const handleColorChange = (e) => {
    const color = e.target.value;
    setSchoolData({ ...schoolData, primary_color: color });
    document.documentElement.style.setProperty('--accent-primary', color);
    
    // Calculate a hover color slightly darker
    document.documentElement.style.setProperty('--accent-hover', color + 'dd');
  };

  const handleSaveSchool = async (e) => {
    e.preventDefault();
    if (!schoolId) return;
    try {
      await api(`/schools/${schoolId}`, {
        method: 'PUT',
        body: schoolData
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSaveMarketing = async (e) => {
    e.preventDefault();
    try {
      await api(`/marketing/${schoolId}`, {
        method: 'PUT',
        body: marketingData
      });
      setSaved(true); setTimeout(() => setSaved(false), 3000);
    } catch(err) { console.error(err); }
  };

  const handleSaveBot = async (e) => {
    e.preventDefault();
    try {
      await api(`/bot/${schoolId}`, {
        method: 'PUT',
        body: botData
      });
      setSaved(true); setTimeout(() => setSaved(false), 3000);
    } catch(err) { console.error(err); }
  };

  const generateApiKey = async (e) => {
    e.preventDefault();
    try {
      const data = await api(`/keys/keys/${schoolId}`, {
        method: 'POST',
        body: { name: apiKeyName || 'New API Key' }
      });
      setGeneratedKey(data.api_key);
    } catch(err) { console.error(err); }
  };

  const handleSaveKommo = async (e) => {
    e.preventDefault();
    try {
      await api(`/crm/settings/${schoolId}`, {
        method: 'PUT',
        body: kommoData
      });
      setSaved(true); setTimeout(() => setSaved(false), 3000);
    } catch(err) { console.error(err); }
  };

  const handleSaveProfile = async (e) => {
    e.preventDefault();
    if (!user) return;
    setProfileError('');
    try {
      await api(`/users/${user.id}`, {
        method: 'PUT',
        body: { full_name: userData.full_name }
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      setProfileError(err.message || "Saqlashda xatolik yuz berdi");
    }
  };

  return (
    <div className="settings-container">
      <div className="settings-header">
        <h1>Sozlamalar</h1>
        <p>Maktabingiz brendi va shaxsiy profilingizni moslashtiring</p>
      </div>

      <div className="settings-layout">
        <div className="settings-sidebar card">
          <button 
            className={`settings-tab ${activeTab === 'school' ? 'active' : ''}`}
            onClick={() => setActiveTab('school')}
          >
            <Palette size={18} />
            Maktab Brendingi
          </button>
          <button 
            className={`settings-tab ${activeTab === 'marketing' ? 'active' : ''}`}
            onClick={() => setActiveTab('marketing')}
          >
            <Target size={18} />
            Marketing (Piksellar)
          </button>
          <button 
            className={`settings-tab ${activeTab === 'bot' ? 'active' : ''}`}
            onClick={() => setActiveTab('bot')}
          >
            <MessageCircle size={18} />
            Telegram Bot
          </button>
          <button 
            className={`settings-tab ${activeTab === 'kommo' ? 'active' : ''}`}
            onClick={() => setActiveTab('kommo')}
          >
            <Briefcase size={18} />
            Kommo CRM
          </button>
          <button 
            className={`settings-tab ${activeTab === 'api' ? 'active' : ''}`}
            onClick={() => setActiveTab('api')}
          >
            <Key size={18} />
            API Kalitlar
          </button>
          <button 
            className={`settings-tab ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            <User size={18} />
            Mening Profilim
          </button>
          {user && user.role === 'admin' && (
            <button 
              className={`settings-tab ${activeTab === 'subscription' ? 'active' : ''}`}
              onClick={() => setActiveTab('subscription')}
            >
              <CreditCard size={18} />
              Platforma Obunasi
            </button>
          )}
        </div>

        <div className="settings-content">
          {activeTab === 'school' && (
            <div className="card settings-panel">
              <div className="panel-header">
                <h2>Maktab Brendingi</h2>
                <p className="text-muted">Maktabingiz ko'rinishini va domenini o'zgartiring</p>
              </div>

              {saved && (
                <div className="alert-success">
                  <CheckCircle size={18} /> Saqlandi!
                </div>
              )}

              <form onSubmit={handleSaveSchool} className="settings-form">
                <div className="form-group">
                  <label>Maktab Nomi</label>
                  <input 
                    type="text" 
                    value={schoolData.name} 
                    onChange={(e) => setSchoolData({...schoolData, name: e.target.value})}
                  />
                </div>

                <div className="form-group">
                  <label>Maxsus Domen (Custom Domain)</label>
                  <div className="input-group">
                    <Globe size={18} className="input-icon" />
                    <input 
                      type="text" 
                      placeholder="masalan: academy.uz"
                      value={schoolData.custom_domain} 
                      onChange={(e) => setSchoolData({...schoolData, custom_domain: e.target.value})}
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label>Asosiy Rang (Primary Color)</label>
                  <div className="color-picker-wrapper">
                    <input 
                      type="color" 
                      value={schoolData.primary_color} 
                      onChange={handleColorChange}
                      className="color-picker"
                    />
                    <span className="color-value">{schoolData.primary_color}</span>
                  </div>
                  <p className="text-sm text-muted mt-2">Bu rang platformaning barcha tugmalari va faol elementlarida qo'llaniladi.</p>
                </div>

                <div className="form-actions">
                  <button type="submit" className="btn-primary">
                    <Save size={18} style={{marginRight: '8px'}} /> Saqlash
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'profile' && (
            <div className="card settings-panel">
              <div className="panel-header">
                <h2>Mening Profilim</h2>
                <p className="text-muted">Shaxsiy ma'lumotlaringizni tahrirlang</p>
              </div>
              
              {saved && <div className="alert-success"><CheckCircle size={18} /> Saqlandi!</div>}
              {profileError && <div style={{ color: '#b91c1c', background: '#fee2e2', padding: '10px', borderRadius: '8px', marginBottom: '12px', fontSize: '13px' }}>{profileError}</div>}
              <form className="settings-form" onSubmit={handleSaveProfile}>
                <div className="form-group">
                  <label>To'liq Ism</label>
                  <input 
                    type="text" 
                    value={userData.full_name} 
                    onChange={(e) => setUserData({...userData, full_name: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Email</label>
                  <input 
                    type="email" 
                    value={userData.email} 
                    disabled
                  />
                  <p className="text-sm text-muted mt-1">Email manzilini o'zgartirish uchun yordam markaziga murojaat qiling.</p>
                </div>
                
                <div className="form-actions">
                  <button type="submit" className="btn-primary">
                    <Save size={18} style={{marginRight: '8px'}} /> Saqlash
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'subscription' && (
            <div className="card settings-panel">
              <div className="panel-header">
                <h2>Platforma Obunasi</h2>
                <p className="text-muted">Maktabingiz uchun oylik tarifni boshqaring</p>
              </div>
              <div style={{ marginTop: '20px' }}>
                {subMessage.text && (
                  <div style={{
                    padding: '10px 14px', borderRadius: '8px', marginBottom: '16px', fontSize: '13px',
                    ...(subMessage.type === 'success'
                      ? { color: '#166534', background: '#dcfce7', border: '1px solid #bbf7d0' }
                      : { color: '#b91c1c', background: '#fee2e2', border: '1px solid #fecaca' })
                  }}>
                    {subMessage.text}
                  </div>
                )}

                <div style={{ display: 'flex', gap: '16px', marginBottom: '24px', flexWrap: 'wrap' }}>
                  <div style={{ flex: 1, minWidth: '180px', padding: '16px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                    <p className="text-muted" style={{ margin: 0, fontSize: '13px' }}>Joriy balans</p>
                    <h3 style={{ margin: '4px 0 0' }}>{(user?.balance || 0).toLocaleString()} UZS</h3>
                  </div>
                  <div style={{ flex: 1, minWidth: '180px', padding: '16px', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                    <p className="text-muted" style={{ margin: 0, fontSize: '13px' }}>Joriy obuna</p>
                    {subscription ? (
                      <>
                        <h3 style={{ margin: '4px 0 0' }}>{subscription.plan_name}</h3>
                        <p className="text-muted" style={{ margin: '2px 0 0', fontSize: '12px' }}>
                          {subscription.status === 'active' ? 'Faol' : subscription.status} · {new Date(subscription.expires_at).toLocaleDateString()} gacha
                        </p>
                      </>
                    ) : (
                      <p style={{ margin: '4px 0 0', color: '#f59e0b', fontSize: '14px' }}>Obuna faol emas</p>
                    )}
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
                  {plans.map((plan) => {
                    const isRecommended = plan.id === 'standard';
                    const isCurrent = subscription && subscription.plan_name === plan.name;
                    return (
                      <div key={plan.id} style={{
                        padding: '20px', borderRadius: '10px', background: '#fff', position: 'relative',
                        border: isRecommended ? '2px solid #3b82f6' : '1px solid #e2e8f0'
                      }}>
                        {isRecommended && (
                          <span style={{
                            position: 'absolute', top: '-10px', left: '50%', transform: 'translateX(-50%)',
                            background: '#3b82f6', color: '#fff', fontSize: '11px', padding: '2px 10px',
                            borderRadius: '999px', whiteSpace: 'nowrap'
                          }}>
                            Tavsiya etiladi
                          </span>
                        )}
                        <h3 style={{ margin: 0 }}>{plan.name}</h3>
                        <p style={{ margin: '8px 0 12px', fontSize: '20px', fontWeight: 600 }}>
                          {plan.price.toLocaleString()} <span className="text-muted" style={{ fontSize: '13px', fontWeight: 400 }}>UZS/oy</span>
                        </p>
                        <ul style={{ margin: '0 0 16px', paddingLeft: '18px', color: '#475569', fontSize: '13px', lineHeight: '1.8' }}>
                          {plan.features.filter((f) => f !== 'Tavsiya etiladi').map((f) => <li key={f}>{f}</li>)}
                        </ul>
                        <button
                          className="btn-primary"
                          style={{ width: '100%', opacity: (subLoading || isCurrent) ? 0.6 : 1 }}
                          disabled={subLoading || isCurrent}
                          onClick={() => handleSubscribe(plan.id)}
                        >
                          {isCurrent ? 'Faol obuna' : 'Tanlash'}
                        </button>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'marketing' && (
            <div className="card settings-panel">
              <div className="panel-header">
                <h2>Marketing va Piksellar</h2>
                <p className="text-muted">Sotuv voronkasini kuzatish uchun analitika vositalarini ulang</p>
              </div>
              
              {saved && <div className="alert-success"><CheckCircle size={18} /> Saqlandi!</div>}
              <form className="settings-form" onSubmit={handleSaveMarketing}>
                <div className="form-group">
                  <label>Facebook Pixel ID</label>
                  <input 
                    type="text" placeholder="Masalan: 1234567890"
                    value={marketingData.facebook_pixel_id} 
                    onChange={(e) => setMarketingData({...marketingData, facebook_pixel_id: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Google Analytics (G-Tag)</label>
                  <input 
                    type="text" placeholder="Masalan: G-XXXXXXX"
                    value={marketingData.google_analytics_id} 
                    onChange={(e) => setMarketingData({...marketingData, google_analytics_id: e.target.value})}
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-primary">Saqlash</button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'bot' && (
            <div className="card settings-panel">
              <div className="panel-header">
                <h2>Telegram Bot Integratsiyasi</h2>
                <p className="text-muted">O'quvchilarni to'lovdan so'ng avtomatik yopiq kanalga qo'shish</p>
              </div>
              
              {saved && <div className="alert-success"><CheckCircle size={18} /> Saqlandi!</div>}
              <form className="settings-form" onSubmit={handleSaveBot}>
                <div className="form-group">
                  <label>Bot Token (@BotFather'dan olingan)</label>
                  <input 
                    type="password" placeholder="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
                    value={botData.bot_token} 
                    onChange={(e) => setBotData({...botData, bot_token: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Yopiq kanal/guruh ID si</label>
                  <input 
                    type="text" placeholder="Masalan: -100123456789"
                    value={botData.private_channel_id} 
                    onChange={(e) => setBotData({...botData, private_channel_id: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Foydalanuvchilarga ko'rinadigan taklifnoma linki</label>
                  <input 
                    type="text" placeholder="https://t.me/+AbCdEfGhIjKlMnOp"
                    value={botData.invite_link} 
                    onChange={(e) => setBotData({...botData, invite_link: e.target.value})}
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-primary">Saqlash</button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'kommo' && (
            <div className="card settings-panel">
              <div className="panel-header">
                <h2>Kommo CRM Integratsiyasi</h2>
                <p className="text-muted">Barcha Lead va Kontaktlarni avtomatik tarzda Kommo dagi voronkaga yo'naltiring</p>
              </div>
              
              {saved && <div className="alert-success"><CheckCircle size={18} /> Saqlandi!</div>}
              <form className="settings-form" onSubmit={handleSaveKommo}>
                <div className="form-group">
                  <label>Subdomain (masalan: myacademy.kommo.com)</label>
                  <input 
                    type="text" placeholder="myacademy"
                    value={kommoData.subdomain}
                    onChange={(e) => setKommoData({...kommoData, subdomain: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Integration ID (Client ID)</label>
                  <input 
                    type="text" placeholder="..."
                    value={kommoData.client_id}
                    onChange={(e) => setKommoData({...kommoData, client_id: e.target.value})}
                  />
                </div>
                <div className="form-group">
                  <label>Secret Key (Client Secret)</label>
                  <input 
                    type="password" placeholder="..."
                    value={kommoData.client_secret}
                    onChange={(e) => setKommoData({...kommoData, client_secret: e.target.value})}
                  />
                </div>
                <div className="form-actions" style={{display: 'flex', gap: '10px'}}>
                  <button type="submit" className="btn-primary"><Save size={18} style={{marginRight: '8px'}} /> Saqlash</button>
                  <button type="button" className="btn-outline" onClick={() => alert("Kommo ga yo'naltirilmoqda...")}>
                    <Globe size={18} style={{marginRight: '8px'}} /> Kommo Avtorizatsiyasi
                  </button>
                </div>
              </form>
            </div>
          )}

          {activeTab === 'api' && (
            <div className="card settings-panel">
              <div className="panel-header">
                <h2>Ochiq API (Developer Keys)</h2>
                <p className="text-muted">Tashqi tizimlar bilan integratsiya (CRM, 1C, ERP) qilish uchun API kalitlar yarating</p>
              </div>
              
              <form className="settings-form" onSubmit={generateApiKey}>
                <div className="form-group">
                  <label>Ilova / Integratsiya Nomi</label>
                  <input 
                    type="text" placeholder="Masalan: Mening amoCRM integratsiyam"
                    value={apiKeyName} 
                    onChange={(e) => setApiKeyName(e.target.value)}
                    required
                  />
                </div>
                <div className="form-actions">
                  <button type="submit" className="btn-primary">Yangi Kalit Yaratish</button>
                </div>
              </form>

              {generatedKey && (
                <div className="alert-success mt-4" style={{marginTop: '20px', padding: '15px', borderRadius: '8px', background: '#dcfce7', color: '#166534', border: '1px solid #bbf7d0'}}>
                  <strong>Sizning yangi maxfiy kalitingiz:</strong> <br/>
                  <code style={{fontSize: '1.2rem', padding: '5px', background: '#fff', display: 'inline-block', marginTop: '10px'}}>{generatedKey}</code>
                  <p className="text-sm mt-2">Iltimos, uni darhol nusxalab oling. Bu kalit boshqa ko'rsatilmaydi!</p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;
