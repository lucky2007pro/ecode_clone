const { useState, useEffect } = React;

// --- MOCK & REAL DATA ---
const ONBOARDING_ROLES = [
  { id: "school_owner", title: "Onlayn maktab egasiman", icon: "🏫" },
  { id: "expert_teacher", title: "Individual ekspert/o'qituvchiman", icon: "👨‍🏫" },
  { id: "producer", title: "Prodyuserman", icon: "🎬" },
  { id: "corporate_hr", title: "Korporativ o'qitish", icon: "🏢" },
  { id: "other", title: "Boshqa", icon: "⚡" }
];

const FEATURES_LIST = [
  { id: "all", hash: "#/features", title: "Barcha imkoniyatlar", desc: "Bitta platformada 11 ta vosita", icon: "📑", badge: "11 ta vosita" },
  { id: "course-builder", hash: "#/features/course-builder", title: "Kurs konstruktori", desc: "Video, matn, testlar — vizual muharrir", icon: "🎛️", badge: "Kinescope API" },
  { id: "homework", hash: "#/features/homework", title: "Uy vazifalari", desc: "Testlar, topshiriqlar va avto-tekshirish", icon: "📝", badge: "7 xil vazifa" },
  { id: "payments", hash: "#/features/payments", title: "To'lovlarni qabul qilish", desc: "Payme, Click, Uzum va rossiya kartalari", icon: "💳", badge: "Payme & Click" },
  { id: "installments", hash: "#/features/installments", title: "Bo'lib-bo'lib to'lash", desc: "Avto-yechib olish va bosqichma-bosqich...", icon: "🔄", badge: "Auto-debit" },
  { id: "customization", hash: "#/features/customization", title: "Maktab kastomizatsiyasi", desc: "O'z brendingiz, ranglar va domen", icon: "🎨", badge: "White-Label" },
  { id: "analytics", hash: "#/features/analytics", title: "Analitika", desc: "Daromad, faollik va o'quvchi xulqi", icon: "📈", badge: "Real-time" },
  { id: "messenger", hash: "#/features/messenger", title: "Messendjer", desc: "Platforma ichida o'quvchilar bilan suhbat", icon: "💬", badge: "WebSocket" },
  { id: "marketing", hash: "#/features/marketing", title: "Marketing va sotuv", desc: "Piksellar, UTM, jo'natmalar va tripvayrlar", icon: "📢", badge: "FB Pixel & GA4" },
  { id: "docs", hash: "#/docs", title: "API hujjatlar", desc: "Hujjatlar va integratsiyalar", icon: "💻", badge: "OpenAPI 3.0" }
];

const INITIAL_COURSES = [
  {
    id: "c1",
    title: "Python & FastAPI Microservices Masterclass",
    slug: "fastapi-microservices",
    description: "Multi-tenant backend arxitekturasi, RabbitMQ Event-Driven, Kinescope va Kommo CRM integratsiyasi.",
    price: 1200000,
    monthly_price: 400000,
    cover: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80",
    modules_count: 5,
    lessons_count: 32,
    students: 142,
    telegram_invite_link: "https://t.me/+ExodeClosedGroupDemo123",
    modules: [
      {
        id: "m1",
        title: "1-Modul: Mikroservislar Arxitekturasi va Event Broker",
        lessons: [
          {
            id: "l1",
            title: "FastAPI + asyncpg sozlash",
            duration: "18:40",
            video_id: "kinescope-v101",
            is_free: true,
            homework: {
              id: "hw1",
              title: "1-Dars bo'yicha amaliy vazifa",
              type: "test",
              instructions: "Quyidagi test va mantiqiy savollarga javob bering.",
              questions: [
                { id: "q1", text: "FastAPI ilovasida async ORM sifatida qaysi kutubxona ishlatiladi?", options: ["psycopg2", "asyncpg / SQLAlchemy 2.0", "sqlite3"], correct: 1 }
              ]
            }
          }
        ]
      }
    ]
  }
];

// --- MAIN APP ---
function App() {
  const [route, setRoute] = useState(window.location.hash || "#/");
  const [currentUser, setCurrentUser] = useState(null);
  const [activeCourseId, setActiveCourseId] = useState("c1");
  const [activeLesson, setActiveLesson] = useState(INITIAL_COURSES[0].modules[0].lessons[0]);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [toast, setToast] = useState(null);

  useEffect(() => {
    const handleHashChange = () => {
      setRoute(window.location.hash || "#/");
      setIsDropdownOpen(false);
    };
    window.addEventListener("hashchange", handleHashChange);
    return () => window.removeEventListener("hashchange", handleHashChange);
  }, []);

  const navigate = (hash) => {
    window.location.hash = hash;
    setRoute(hash);
    setIsDropdownOpen(false);
  };

  const showNotification = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(null), 4000);
  };

  return (
    <div>
      <div className="bg-glow"></div>

      {/* TOAST NOTIFICATION */}
      {toast && (
        <div style={{
          position: "fixed", bottom: 25, right: 25, zIndex: 9999,
          background: "rgba(16, 185, 129, 0.95)", color: "white", padding: "14px 28px",
          borderRadius: 14, boxShadow: "0 10px 40px rgba(0,0,0,0.6)", display: "flex", gap: 10, alignItems: "center",
          fontWeight: 600
        }}>
          ✓ {toast}
        </div>
      )}

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="nav-brand" onClick={() => navigate("#/")}>
          <div className="brand-icon">⚡</div>
          <span>exode<span className="text-gradient">.biz</span></span>
        </div>

        <ul className="nav-links">
          <li style={{ position: "relative" }}>
            <span
              className={`nav-link ${route.includes("#/features") || route === "#/docs" ? "active" : ""}`}
              onClick={() => setIsDropdownOpen(!isDropdownOpen)}
              style={{ display: "flex", alignItems: "center", gap: 6, cursor: "pointer" }}
            >
              Imkoniyatlar {isDropdownOpen ? "▲" : "▼"}
            </span>

            {isDropdownOpen && (
              <div
                className="glass-panel"
                style={{
                  position: "absolute",
                  top: "120%",
                  left: "-100px",
                  width: "680px",
                  padding: "1.5rem",
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "1rem",
                  zIndex: 1000,
                  boxShadow: "0 25px 60px rgba(0,0,0,0.8)",
                  border: "1px solid rgba(255,255,255,0.15)",
                  background: "#0c1322"
                }}
              >
                {FEATURES_LIST.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => navigate(item.hash)}
                    style={{
                      display: "flex",
                      alignItems: "flex-start",
                      gap: "12px",
                      padding: "12px",
                      borderRadius: "12px",
                      cursor: "pointer",
                      transition: "all 0.2s",
                      background: route === item.hash ? "rgba(99, 102, 241, 0.2)" : "transparent"
                    }}
                  >
                    <div style={{ width: 42, height: 42, borderRadius: 10, background: "rgba(99, 102, 241, 0.15)", border: "1px solid rgba(99, 102, 241, 0.3)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "1.2rem", flexShrink: 0 }}>
                      {item.icon}
                    </div>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: "0.95rem", color: "var(--text-main)" }}>{item.title}</div>
                      <div style={{ fontSize: "0.8rem", color: "var(--text-muted)", marginTop: 2 }}>{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </li>

          <li><span className={`nav-link ${route === "#/courses" ? "active" : ""}`} onClick={() => navigate("#/courses")}>Kurslar Catalog</span></li>
          <li><span className={`nav-link ${route === "#/pricing" ? "active" : ""}`} onClick={() => navigate("#/pricing")}>Tariflar & Bo'lib to'lash</span></li>
          <li><span className={`nav-link ${route === "#/dashboard" ? "active" : ""}`} onClick={() => navigate("#/dashboard")}>Dashboard</span></li>
        </ul>

        <div style={{ display: "flex", gap: 10 }}>
          {currentUser ? (
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span className="badge badge-success">👤 {currentUser.name} ({currentUser.role})</span>
              <button className="btn btn-secondary btn-sm" onClick={() => { setCurrentUser(null); showNotification("Tizimdan chiqdingiz"); }}>Chiqish</button>
            </div>
          ) : (
            <>
              <button className="btn btn-secondary btn-sm" onClick={() => navigate("#/login")}>Kirish</button>
              <button className="btn btn-primary btn-sm" onClick={() => navigate("#/register")}>Maktab ochish</button>
            </>
          )}
        </div>
      </nav>

      {/* PAGE ROUTING */}
      {route === "#/" && <HomePage navigate={navigate} />}
      {route === "#/features" && <AllFeaturesPage navigate={navigate} />}
      {route === "#/features/course-builder" && <FeatureCourseBuilderPage navigate={navigate} />}
      {route === "#/features/homework" && <FeatureHomeworkPage navigate={navigate} />}
      {route === "#/features/payments" && <FeaturePaymentsPage navigate={navigate} />}
      {route === "#/features/installments" && <FeatureInstallmentsPage navigate={navigate} />}
      {route === "#/features/customization" && <FeatureCustomizationPage navigate={navigate} />}
      {route === "#/features/analytics" && <FeatureAnalyticsPage navigate={navigate} />}
      {route === "#/features/messenger" && <FeatureMessengerPage navigate={navigate} />}
      {route === "#/features/marketing" && <FeatureMarketingPage navigate={navigate} />}
      {route === "#/docs" && <FeatureDocsPage navigate={navigate} />}

      {route === "#/login" && <LoginPage navigate={navigate} setCurrentUser={setCurrentUser} showNotification={showNotification} />}
      {route === "#/register" && <RegisterPage navigate={navigate} setCurrentUser={setCurrentUser} showNotification={showNotification} />}
      {route === "#/courses" && <CoursesPage navigate={navigate} setActiveCourseId={setActiveCourseId} />}
      {route.startsWith("#/courses/") && <CourseDetailPage courseId={route.split("#/courses/")[1] || activeCourseId} activeLesson={activeLesson} setActiveLesson={setActiveLesson} showNotification={showNotification} />}
      {route === "#/pricing" && <PricingPage navigate={navigate} showNotification={showNotification} />}
      {route === "#/dashboard" && <DashboardPage navigate={navigate} currentUser={currentUser} showNotification={showNotification} />}

      {/* FOOTER */}
      <footer style={{ borderTop: "1px solid var(--border-glass)", padding: "3rem 0", marginTop: "5rem", textAlign: "center", color: "var(--text-dim)" }}>
        <div className="container">
          <p>© 2026 Exode.biz — Onlayn Maktab va Kurslar Platformasi. Barcha huquqlar himoyalangan.</p>
        </div>
      </footer>
    </div>
  );
}

// --- EXACT REGISTRATION PERSONA SELECTION MATCHING USER IMAGE ---
function RegisterPage({ navigate, setCurrentUser, showNotification }) {
  const [selectedRole, setSelectedRole] = useState("school_owner");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [subdomain, setSubdomain] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();
    const roleTitle = ONBOARDING_ROLES.find(r => r.id === selectedRole)?.title || selectedRole;
    const user = { name, email, role: selectedRole, school_id: "school-" + Date.now() };
    setCurrentUser(user);
    showNotification(`Tabriklaymiz! ${roleTitle} sifatida maktabingiz (${subdomain}.exode.biz) yaratildi!`);
    navigate("#/dashboard");
  };

  return (
    <div className="container" style={{ maxWidth: 620, marginTop: "2rem" }}>
      <div className="glass-panel" style={{ padding: "2.5rem" }}>
        <h2 style={{ textAlign: "center", fontSize: "2rem", marginBottom: 6 }}>Sizga to'g'ri keladigan variantni tanlang</h2>
        <p style={{ textAlign: "center", color: "var(--text-muted)", marginBottom: 24 }}>Platformani vazifangizga moslab 2 daqiqada ishga tushiring</p>
        
        {/* EXACT PERSONA SELECTION CARDS MATCHING USER IMAGE */}
        <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 28 }}>
          {ONBOARDING_ROLES.map(role => (
            <div
              key={role.id}
              onClick={() => setSelectedRole(role.id)}
              style={{
                padding: "1rem 1.25rem",
                borderRadius: "14px",
                background: selectedRole === role.id ? "rgba(99, 102, 241, 0.15)" : "rgba(255, 255, 255, 0.03)",
                border: selectedRole === role.id ? "2px solid var(--primary)" : "1px solid var(--border-glass)",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                gap: 14,
                fontSize: "1.05rem",
                fontWeight: 600,
                color: selectedRole === role.id ? "var(--text-main)" : "var(--text-muted)",
                transition: "all 0.2s ease"
              }}
            >
              <span style={{ fontSize: "1.3rem" }}>{role.icon}</span>
              <span>{role.title}</span>
              {selectedRole === role.id && <span style={{ marginLeft: "auto", color: "var(--primary)" }}>✓</span>}
            </div>
          ))}
        </div>

        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label className="form-label">F.I.SH (To'liq Ismingiz)</label>
            <input type="text" className="form-input" placeholder="Hojiakbar Rahimov" required value={name} onChange={e => setName(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Email Manzilingiz</label>
            <input type="email" className="form-input" placeholder="hojiakbar@exode.biz" required value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Maktab Subdomeni</label>
            <div style={{ display: "flex", alignItems: "center" }}>
              <input type="text" className="form-input" placeholder="it-academy" required value={subdomain} onChange={e => setSubdomain(e.target.value.toLowerCase().replace(/\s+/g, '-'))} style={{ borderRadius: "14px 0 0 14px" }} />
              <span style={{ background: "rgba(255,255,255,0.05)", padding: "0.85rem 1rem", border: "1px solid var(--border-glass)", borderLeft: 0, borderRadius: "0 14px 14px 0", color: "var(--text-muted)", fontSize: "0.9rem" }}>.exode.biz</span>
            </div>
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: "100%", justifyContent: "center", marginTop: 12, padding: "0.9rem" }}>
            Davom etish ({ONBOARDING_ROLES.find(r => r.id === selectedRole)?.title})
          </button>
        </form>
      </div>
    </div>
  );
}

// --- DEDICATED FEATURE PAGES ---
function AllFeaturesPage({ navigate }) {
  return (
    <div className="container">
      <div style={{ textAlign: "center", marginBottom: "3rem" }}>
        <span className="badge badge-primary" style={{ marginBottom: 12 }}>Bitta platformada 11 ta vosita</span>
        <h2>Exode.biz Barcha Imkoniyatlari</h2>
      </div>
      <div className="grid-3">
        {FEATURES_LIST.slice(1).map(item => (
          <div key={item.id} className="glass-panel glass-panel-interactive" style={{ padding: "2rem", cursor: "pointer" }} onClick={() => navigate(item.hash)}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
              <div className="brand-icon" style={{ fontSize: "1.5rem" }}>{item.icon}</div>
              <span className="badge badge-primary">{item.badge}</span>
            </div>
            <h3>{item.title}</h3>
            <p style={{ color: "var(--text-muted)", marginTop: 8, fontSize: "0.95rem" }}>{item.desc}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

function FeatureCourseBuilderPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-primary">Vizual Muharrir</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>Kurs Konstruktori</h1>
        <p style={{ fontSize: "1.2rem", color: "var(--text-muted)" }}>Video, matn, testlar va fayllardan iborat kurslarni bir necha daqiqada vizual konstruktor orqali noldan yarating.</p>
      </div>
    </div>
  );
}

function FeatureHomeworkPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-success">7 xil vazifa turi</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>Uy Vazifalari va Testlar</h1>
        <p style={{ fontSize: "1.2rem", color: "var(--text-muted)" }}>Testlar, moslashtirish, mantiqiy tanlov, matnli topshiriqlar va fayl yuklash.</p>
      </div>
    </div>
  );
}

function FeaturePaymentsPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-warning">Payme & Click & Uzum</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>To'lovlarni Qabul Qilish</h1>
      </div>
    </div>
  );
}

function FeatureInstallmentsPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-primary">Auto-debit Subscription</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>Bo'lib-bo'lib To'lash</h1>
      </div>
    </div>
  );
}

function FeatureCustomizationPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-success">White-Label & Custom Domain</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>Maktab Kastomizatsiyasi</h1>
      </div>
    </div>
  );
}

function FeatureAnalyticsPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-warning">Real-time Dashbord</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>Ta'lim va Sotuv Analitikasi</h1>
      </div>
    </div>
  );
}

function FeatureMessengerPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-primary">WebSocket Live Chat</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>Platforma Ichidagi Messendjer</h1>
      </div>
    </div>
  );
}

function FeatureMarketingPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-success">FB Pixel & GA4 & UTM</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>Marketing va Sotuv Vositalari</h1>
      </div>
    </div>
  );
}

function FeatureDocsPage({ navigate }) {
  return (
    <div className="container">
      <div className="glass-panel" style={{ padding: "3rem" }}>
        <span className="badge badge-primary">FastAPI Swagger / OpenAPI 3.0</span>
        <h1 style={{ fontSize: "2.8rem", margin: "12px 0" }}>API Hujjatlar va Integratsiyalar</h1>
      </div>
    </div>
  );
}

function HomePage({ navigate }) {
  return (
    <div>
      <section className="hero">
        <span className="badge badge-primary" style={{ marginBottom: 16 }}>🚀 Bitta platformada 11 ta vosita</span>
        <h1 className="hero-title">O'z Onlayn Maktabingizni <br /><span className="text-gradient">Exode.biz bilan Barpo Eting</span></h1>
        <p className="hero-desc">
          Kinescope video xavfsizligi, Kommo CRM avto-lidi, Payme/Click/Uzum to'lovlari, Uy vazifalari va Telegram yopiq guruh avto-kirish imkoniyati.
        </p>
        <div style={{ display: "flex", gap: 16, justifyContent: "center" }}>
          <button className="btn btn-primary" onClick={() => navigate("#/register")}>Maktab Yaratish (14 kun bepul)</button>
          <button className="btn btn-secondary" onClick={() => navigate("#/features")}>Barcha Imkoniyatlarni Ko'rish</button>
        </div>
      </section>
    </div>
  );
}

function LoginPage({ navigate, setCurrentUser, showNotification }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();
    const user = { name: email.split("@")[0] || "Foydalanuvchi", email, role: "admin", school_id: "s1" };
    setCurrentUser(user);
    showNotification("Xush kelibsiz! Tizimga muvaffaqiyatli kirdingiz.");
    navigate("#/dashboard");
  };

  return (
    <div className="container" style={{ maxWidth: 450, marginTop: "4rem" }}>
      <div className="glass-panel" style={{ padding: "2.5rem" }}>
        <h2 style={{ textAlign: "center", marginBottom: 8 }}>Tizimga Kirish</h2>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label className="form-label">Email Manzil</label>
            <input type="email" className="form-input" placeholder="admin@maktab.uz" required value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Parol</label>
            <input type="password" className="form-input" placeholder="••••••••" required value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: "100%", justifyContent: "center", marginTop: 12 }}>Kirish (JWT Auth)</button>
        </form>
      </div>
    </div>
  );
}

function CoursesPage({ navigate, setActiveCourseId }) {
  return (
    <div className="container">
      <h2>Barcha Kurslar Katalogi</h2>
      <div className="grid-2" style={{ marginTop: 20 }}>
        {INITIAL_COURSES.map(course => (
          <div key={course.id} className="glass-panel" style={{ padding: "1.5rem" }}>
            <h3>{course.title}</h3>
            <p style={{ color: "var(--text-muted)", margin: "10px 0" }}>{course.description}</p>
            <button className="btn btn-primary" onClick={() => { setActiveCourseId(course.id); navigate(`#/courses/${course.id}`); }}>Darslarni Ko'rish</button>
          </div>
        ))}
      </div>
    </div>
  );
}

function CourseDetailPage({ courseId, activeLesson, setActiveLesson, showNotification }) {
  const course = INITIAL_COURSES.find(c => c.id === courseId) || INITIAL_COURSES[0];
  return (
    <div className="container">
      <h2>{course.title} — {activeLesson.title}</h2>
      <div className="glass-panel" style={{ padding: "2rem", marginTop: 20 }}>
        <p style={{ color: "var(--text-muted)" }}>Kinescope Stream ID: {activeLesson.video_id}</p>
      </div>
    </div>
  );
}

function PricingPage({ navigate, showNotification }) {
  return (
    <div className="container">
      <h2>Maktablar uchun Tarif Rejalari</h2>
    </div>
  );
}

function DashboardPage({ navigate, currentUser, showNotification }) {
  return (
    <div className="container">
      <h2>Maktab Boshqaruv Paneli (Dashboard)</h2>
      <p style={{ color: "var(--text-muted)" }}>Rol: {currentUser?.role || "school_owner"}</p>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
