import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { PlayCircle, Shield, CheckCircle, ArrowRight } from 'lucide-react';
import { AuthContext } from '../context/auth-context';
import './Landing.css';

const Landing = () => {
  const { user } = useContext(AuthContext);
  return (
    <div className="landing-page">
      {}
      <nav className="landing-navbar">
        <Link to="/" className="landing-logo">
          <div className="landing-logo-icon">e</div>
          exode
        </Link>

        <div className="landing-auth-buttons">
          {user ? (
            <Link to="/dashboard" className="btn-login">Dashboard</Link>
          ) : (
            <>
              <Link to="/login" className="btn-demo">Log In</Link>
              <Link to="/register" className="btn-login">Get a demo</Link>
            </>
          )}
        </div>
      </nav>

      {}
      <section className="hero-section">
        <div className="hero-badge">
          <span className="hero-badge-dot"></span>
          Why Exode?
        </div>
        <h1 className="hero-title">
          Everything you need <span className="hero-title-highlight">for an<br/>online school</span>
        </h1>
        <p className="hero-subtitle">
          11 tools in a single platform — from a course builder to installments and marketing. No third-party services.
        </p>
        <div className="hero-buttons">
          <Link to="/register" className="btn-primary-large">Try for free</Link>
          <a href="#pricing" className="btn-secondary-large">Pricing</a>
        </div>
      </section>

      {}
      <section className="features-section">
        <div className="features-header">
          <div>
            <div className="features-tag">01 — content</div>
            <h2 className="features-title">Create and teach</h2>
          </div>
          <p className="features-desc">
            Build a course from blocks, hand out assignments and protect video — no developers, no third-party services.
          </p>
        </div>

        <div className="features-grid">
          {}
          <div className="feature-card card-light-orange">
            <div className="mockup-container">
              <div className="course-blocks">
                <div className="c-block cb-1">Module 1</div>
                <div className="c-block cb-2">Video lesson</div>
                <div className="c-block cb-3">Quiz</div>
                <div className="c-block cb-4">Module 2</div>
                <div className="c-block cb-5">Lecture</div>
              </div>
            </div>
            <div className="feature-card-content">
              <h3 className="feature-card-title">Course Builder</h3>
              <p className="feature-card-desc">Create and structure courses with the Exode visual builder.</p>
              <Link to="/register" className="feature-link">Learn more <ArrowRight size={16} className="ml-1" /></Link>
            </div>
          </div>

          {}
          <div className="feature-card card-light-purple">
            <div className="mockup-container">
              <div className="hw-mockup">
                <div className="hw-title">#3 Tell us about CRM</div>
                <div className="hw-option active">
                  <div className="hw-radio active"></div>
                  Software for clients
                </div>
                <div className="hw-option">
                  <div className="hw-radio"></div>
                  Contact database
                </div>
                <div className="hw-option">
                  <div className="hw-radio"></div>
                  Sales funnel
                </div>
              </div>
            </div>
            <div className="feature-card-content">
              <h3 className="feature-card-title">Homework</h3>
              <p className="feature-card-desc">Create tests, graded assignments and exams on the Exode platform.</p>
              <Link to="/register" className="feature-link">Learn more <ArrowRight size={16} className="ml-1" /></Link>
            </div>
          </div>

          {}
          <div className="feature-card card-dark">
            <div className="mockup-container">
              <div className="protection-mockup">
                <div className="lock-circle">
                  <Shield size={28} />
                </div>
              </div>
            </div>
            <div className="feature-card-content">
              <h3 className="feature-card-title">Content Protection</h3>
              <p className="feature-card-desc">Protect video lessons and course materials from unauthorized distribution.</p>
            </div>
          </div>
        </div>
      </section>

      {}
      <section className="how-it-works">
        <h2 className="hiw-title">How it works</h2>
        <div className="hiw-grid">
          <div className="hiw-step">
            <div className="hiw-number">01</div>
            <h4 className="hiw-step-title">Sign Up</h4>
            <p className="hiw-step-desc">Create your school profile in minutes without any coding.</p>
          </div>
          <div className="hiw-step">
            <div className="hiw-number">02</div>
            <h4 className="hiw-step-title">Upload Content</h4>
            <p className="hiw-step-desc">Use our drag-and-drop builder to upload videos and create quizzes.</p>
          </div>
          <div className="hiw-step">
            <div className="hiw-number">03</div>
            <h4 className="hiw-step-title">Invite Students</h4>
            <p className="hiw-step-desc">Share links or import your existing student database directly.</p>
          </div>
          <div className="hiw-step">
            <div className="hiw-number">04</div>
            <h4 className="hiw-step-title">Start Earning</h4>
            <p className="hiw-step-desc">Accept payments and track analytics in your personal dashboard.</p>
          </div>
        </div>
      </section>

      {}
      <section id="pricing" className="pricing-section">
        <div className="pricing-header">
          <h2 className="pricing-title">Maktablar va ta'lim markazlari uchun tariflar</h2>
          <p className="pricing-desc">O'z biznesingiz hajmi va ehtiyojlariga qarab eng mos tarifni tanlang.</p>
        </div>
        <div className="pricing-grid">
          {}
          <div className="pricing-card">
            <h3 className="plan-name">Boshlang'ich</h3>
            <div className="plan-price">Bepul</div>
            <p className="plan-desc">Yangi boshlayotgan o'qituvchilar va kichik kurslar uchun ideal.</p>
            <ul className="plan-features">
              <li><CheckCircle size={18} className="text-orange" /> 50 tagacha o'quvchi</li>
              <li><CheckCircle size={18} className="text-orange" /> Asosiy kurs konstruktori</li>
              <li><CheckCircle size={18} className="text-orange" /> Bepul sub-domen</li>
            </ul>
            <Link to="/register" className="btn-plan-outline">Boshlash</Link>
          </div>

          {/* Pro Plan */}
          <div className="pricing-card popular">
            <div className="popular-badge">Eng mashhur</div>
            <h3 className="plan-name">Professional</h3>
            <div className="plan-price">$49 <span>/oy</span></div>
            <p className="plan-desc">Faol o'sayotgan o'quv markazlari va maktablar uchun.</p>
            <ul className="plan-features">
              <li><CheckCircle size={18} className="text-orange" /> 500 tagacha o'quvchi</li>
              <li><CheckCircle size={18} className="text-orange" /> Uy vazifalari va testlar</li>
              <li><CheckCircle size={18} className="text-orange" /> Shaxsiy domen (Custom domain)</li>
              <li><CheckCircle size={18} className="text-orange" /> Telegram orqali to'lovlar</li>
            </ul>
            <Link to="/register" className="btn-plan-solid">Boshlash</Link>
          </div>

          {/* Enterprise Plan */}
          <div className="pricing-card">
            <h3 className="plan-name">Biznes</h3>
            <div className="plan-price">Maxsus</div>
            <p className="plan-desc">Katta hajmdagi ta'lim muassasalari uchun to'liq yechim.</p>
            <ul className="plan-features">
              <li><CheckCircle size={18} className="text-orange" /> Cheklanmagan o'quvchilar</li>
              <li><CheckCircle size={18} className="text-orange" /> Videolarni himoyalash</li>
              <li><CheckCircle size={18} className="text-orange" /> White-label tizim</li>
              <li><CheckCircle size={18} className="text-orange" /> Shaxsiy menejer va yordam</li>
            </ul>
            <Link to="/register" className="btn-plan-outline">Aloqaga chiqish</Link>
          </div>
        </div>
      </section>

      {}
      <section className="launch-banner">
        <h2 className="launch-title">Launch your school<br/>in an hour</h2>
        <Link to="/register" className="btn-white-large">Start for free</Link>
      </section>

      {}
      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-brand">
            <Link to="/" className="landing-logo">
              <div className="landing-logo-icon">e</div>
              exode
            </Link>
            <p className="footer-desc">
              All-in-one platform for creators and educators to launch online schools effortlessly.
            </p>
          </div>
          <div className="footer-links">
            <div className="footer-col">
              <h4>Product</h4>
              <ul>
                <li><Link to="#">Features</Link></li>
                <li><Link to="#">Pricing</Link></li>
                <li><Link to="#">Updates</Link></li>
              </ul>
            </div>
            <div className="footer-col">
              <h4>Resources</h4>
              <ul>
                <li><Link to="#">Help Center</Link></li>
                <li><Link to="#">Blog</Link></li>
                <li><Link to="#">Community</Link></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          &copy; {new Date().getFullYear()} Exode Education. All rights reserved.
        </div>
      </footer>
    </div>
  );
};

const ChevronDownIcon = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="6 9 12 15 18 9"></polyline>
  </svg>
);

export default Landing;
