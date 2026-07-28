import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { api } from '../../api';
import './Auth.css';

const Register = () => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    telegram: '',
    password: '',
    subdomain: '',
    roleType: '',
    courseFormat: '',
    role: 'admin' // Default to admin for this flow
  });
  const [otpCode, setOtpCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleNext = () => {
    setError('');
    if (step < 3) {
      setStep(step + 1);
    }
  };

  const handleBack = () => {
    setError('');
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSelectOption = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const handleSendOtp = async () => {
    setLoading(true);
    setError('');

    try {
      await api('/users/register/send-otp', {
        method: 'POST',
        body: {
          full_name: formData.full_name,
          email: formData.email,
          password: formData.password,
          role: formData.role,
          subdomain: formData.subdomain,
          school_name: formData.subdomain
        },
      });
      setStep(4);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOtp = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const payload = { 
        full_name: formData.full_name,
        email: formData.email,
        password: formData.password,
        role: formData.role,
        subdomain: formData.subdomain,
        school_name: formData.subdomain,
        otp_code: otpCode 
      };
      
      await api('/users/register/verify', {
        method: 'POST',
        body: payload,
      });

      alert("Muvaffaqiyatli ro'yxatdan o'tdingiz!");
      navigate('/login');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Progress calculations (Step 4 is OTP, not in progress bar)
  const displayStep = step > 3 ? 3 : step;
  const progressPercentage = Math.round((displayStep / 3) * 100);

  return (
    <div className="auth-container" style={{ backgroundColor: '#F9FAFB', backgroundImage: 'none', padding: '20px' }}>
      <div className="wizard-card" style={{ maxWidth: '600px' }}>
        
        {/* Progress Bar */}
        <div className="wizard-header">
          <div className="wizard-progress-bar">
            <span>Step: {displayStep} / 3</span>
            <span>{progressPercentage}%</span>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${progressPercentage}%` }}></div>
          </div>
        </div>
        
        {error && (
          <div style={{ color: 'red', marginBottom: '16px', fontSize: '14px', textAlign: 'center', background: 'rgba(239, 68, 68, 0.1)', padding: '10px', borderRadius: '8px' }}>
            {error}
          </div>
        )}

        {/* STEP 1 */}
        {step === 1 && (
          <div className="wizard-step">
            <h2 className="wizard-title">
              <span>Fill in the form</span> and activate<br />7 days of free access
            </h2>
            
            <div style={{ marginTop: '30px' }}>
              <div className="wizard-form-group">
                <label>First and last name</label>
                <input 
                  type="text" 
                  name="full_name"
                  className="wizard-input" 
                  placeholder="John Doe" 
                  value={formData.full_name}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="wizard-form-group">
                <label>Email (OTP tasdiqlash uchun)</label>
                <input 
                  type="email" 
                  name="email"
                  className="wizard-input" 
                  placeholder="john@example.com" 
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px' }}>
                <div className="wizard-form-group">
                  <label>Subdomain (Maktab nomi)</label>
                  <input 
                    type="text" 
                    name="subdomain"
                    className="wizard-input" 
                    placeholder="najottalim" 
                    value={formData.subdomain}
                    onChange={handleChange}
                    required
                  />
                </div>
                
                <div className="wizard-form-group">
                  <label>Parol</label>
                  <input 
                    type="password" 
                    name="password"
                    className="wizard-input" 
                    placeholder="••••••••" 
                    value={formData.password}
                    onChange={handleChange}
                    required
                  />
                </div>
              </div>

              <div className="wizard-form-group">
                <label>Telegram</label>
                <div className="wizard-input-group">
                  <div className="wizard-input-prefix">@</div>
                  <input 
                    type="text" 
                    name="telegram"
                    className="wizard-input" 
                    placeholder="username" 
                    value={formData.telegram}
                    onChange={handleChange}
                  />
                </div>
              </div>

              <button className="wizard-btn-primary" onClick={handleNext}>
                Continue
              </button>
              
              <div style={{ textAlign: 'center', marginTop: '15px' }}>
                <Link to="/login" style={{ color: '#6B7280', fontSize: '14px', textDecoration: 'none' }}>Already have an account? Log in</Link>
              </div>
            </div>
          </div>
        )}

        {/* STEP 2 */}
        {step === 2 && (
          <div className="wizard-step">
            <h2 className="wizard-title" style={{ textAlign: 'left', fontSize: '24px' }}>
              Choose the option that suits you
            </h2>
            
            <div style={{ marginTop: '30px' }}>
              {[
                "I own an online school",
                "I'm an individual expert / teacher",
                "I'm a producer",
                "Corporate training",
                "Other"
              ].map((option, idx) => (
                <button
                  key={idx}
                  className={`wizard-option ${formData.roleType === option ? 'selected' : ''}`}
                  onClick={() => handleSelectOption('roleType', option)}
                >
                  {option}
                </button>
              ))}

              <div className="wizard-actions">
                <button className="wizard-btn-secondary" onClick={handleBack}>
                  Back
                </button>
                <button className="wizard-btn-primary" style={{ marginTop: 0 }} onClick={handleNext}>
                  Continue
                </button>
              </div>
            </div>
          </div>
        )}

        {/* STEP 3 */}
        {step === 3 && (
          <div className="wizard-step">
            <h2 className="wizard-title" style={{ textAlign: 'left', fontSize: '24px' }}>
              Do you have an online course, and in what format?
            </h2>
            
            <div style={{ marginTop: '30px' }}>
              {[
                "I have an online course, in recorded lessons format",
                "I have an online course, but in Zoom format",
                "I'm planning to start",
                "My courses are offline",
                "Other"
              ].map((option, idx) => (
                <button
                  key={idx}
                  className={`wizard-option ${formData.courseFormat === option ? 'selected' : ''}`}
                  onClick={() => handleSelectOption('courseFormat', option)}
                >
                  {option}
                </button>
              ))}

              <div className="wizard-actions">
                <button className="wizard-btn-secondary" onClick={handleBack}>
                  Back
                </button>
                <button className="wizard-btn-primary" style={{ marginTop: 0 }} onClick={handleSendOtp} disabled={loading}>
                  {loading ? "Jo'natilmoqda..." : "Send request (Get OTP)"}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* STEP 4: OTP Verification */}
        {step === 4 && (
          <div className="wizard-step">
            <h2 className="wizard-title" style={{ fontSize: '24px' }}>
              Email tasdiqlash
            </h2>
            <p style={{ textAlign: 'center', color: '#6B7280', marginTop: '10px' }}>
              <b>{formData.email}</b> manziliga yuborilgan 6 xonali kodni kiriting.
            </p>
            
            <form onSubmit={handleVerifyOtp} style={{ marginTop: '30px' }}>
              <div className="wizard-form-group">
                <label>Tasdiqlash kodi</label>
                <input 
                  type="text" 
                  className="wizard-input" 
                  placeholder="123456" 
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  required
                  style={{ textAlign: 'center', fontSize: '24px', letterSpacing: '4px' }}
                />
              </div>

              <button type="submit" className="wizard-btn-primary" disabled={loading}>
                {loading ? "Tasdiqlanmoqda..." : "Tasdiqlash"}
              </button>
            </form>
          </div>
        )}

      </div>
    </div>
  );
};

export default Register;
