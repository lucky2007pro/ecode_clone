const { useState, useEffect } = React;

// --- MOCK & REAL DATA ---
const TELEGRAM_ADMIN_HANDLE = "exode_biz_support"; // Admin Telegram username
const TELEGRAM_ADMIN_URL = `https://t.me/${TELEGRAM_ADMIN_HANDLE}`;

const ONBOARDING_ROLES = [
  { id: "school_owner", title: "Onlayn maktab egasiman", icon: "🏫" },
  { id: "expert_teacher", title: "Individual ekspert/o'qituvchiman", icon: "👨‍🏫" },
  { id: "producer", title: "Prodyuserman", icon: "🎬" },
  { id: "corporate_hr", title: "Korporativ o'qitish", icon: "🏢" },
  { id: "other", title: "Boshqa", icon: "⚡" }
];

const FEATURES_LIST = [
  { id: "all", hash: "#/features", title: "Barcha imkoniyatlar", desc: "Bitta platformada 11 ta vosita", icon: "📑" },
  { id: "course-builder", hash: "#/features/course-builder", title: "Kurs konstruktori", desc: "Video, matn, testlar — vizual muharrir", icon: "🎛️" },
  { id: "homework", hash: "#/features/homework", title: "Uy vazifalari", desc: "Testlar, topshiriqlar va avto-tekshirish", icon: "📝" },
  { id: "payments", hash: "#/features/payments", title: "Telegram orqali to'lov", desc: "Admin bilan Telegramda bog'lanish", icon: "💬" },
  { id: "installments", hash: "#/features/installments", title: "Bo'lib-bo'lib to'lash", desc: "Bosqichma-bosqich ruxsat berish", icon: "🔄" },
  { id: "customization", hash: "#/features/customization", title: "Maktab kastomizatsiyasi", desc: "O'z brendingiz va domen", icon: "🎨" },
  { id: "analytics", hash: "#/features/analytics", title: "Analitika", desc: "Daromad va faollik statistikasi", icon: "📈" },
  { id: "messenger", hash: "#/features/messenger", title: "Messendjer", desc: "Platforma ichida suhbat", icon: "💬" },
  { id: "marketing", hash: "#/features/marketing", title: "Marketing va sotuv", desc: "Piksellar va UTM tracker", icon: "📢" },
  { id: "docs", hash: "#/docs", title: "API hujjatlar", desc: "Hujjatlar va integratsiyalar", icon: "💻" }
];

const INITIAL_COURSES = [
  {
    id: "c1",
    title: "Python & FastAPI Microservices Masterclass",
    slug: "fastapi-microservices",
    description: "Multi-tenant backend arxitekturasi, RabbitMQ Event-Driven, Kinescope va Kommo CRM integratsiyasi.",
    price: 1200000,
    cover: "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=600&q=80",
    modules_count: 5,
    lessons_count: 32,
    students: 142,
    telegram_invite_link: `https://t.me/${TELEGRAM_ADMIN_HANDLE}?text=Assalomu%20alaykum!%20Python%20FastAPI%20kursini%20xarid%20qilmoqchiman.`,
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
            is_free: true
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

      {toast && (
        <div style={{ position: "fixed", bottom: 25, right: 25, zIndex: 9999, background: "rgba(16, 185, 129, 0.95)", color: "white", padding: "14px 28px", borderRadius: 14, boxShadow: "0 10px 40px rgba(0,0,0,0.6)", fontWeight: 600 }}>
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
            <span className="nav-link" onClick={() => setIsDropdownOpen(!isDropdownOpen)} style={{ cursor: "pointer" }}>
              Imkoniyatlar {isDropdownOpen ? "▲" : "▼"}
            </span>

            {isDropdownOpen && (
              <div className="glass-panel" style={{ position: "absolute", top: "120%", left: "-100px", width: "680px", padding: "1.5rem", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", zIndex: 1000, background: "#0c1322" }}>
                {FEATURES_LIST.map((item) => (
                  <div key={item.id} onClick={() => navigate(item.hash)} style={{ display: "flex", gap: 12, padding: 12, borderRadius: 12, cursor: "pointer" }}>
                    <div style={{ width: 42, height: 42, borderRadius: 10, background: "rgba(99, 102, 241, 0.15)", display: "flex", alignItems: "center", justifyContent: "center" }}>{item.icon}</div>
                    <div>
                      <div style={{ fontWeight: 700, color: "#fff" }}>{item.title}</div>
                      <div style={{ fontSize: "0.8rem", color: "#94a3b8" }}>{item.desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </li>

          <li><span className={`nav-link ${route === "#/courses" ? "active" : ""}`} onClick={() => navigate("#/courses")}>Kurslar Catalog</span></li>
          <li><span className={`nav-link ${route === "#/pricing" ? "active" : ""}`} onClick={() => navigate("#/pricing")}>Tariflar</span></li>
          <li><span className={`nav-link ${route === "#/dashboard" ? "active" : ""}`} onClick={() => navigate("#/dashboard")}>Dashboard</span></li>
        </ul>

        <div style={{ display: "flex", gap: 10 }}>
          <a href={TELEGRAM_ADMIN_URL} target="_blank" className="btn btn-secondary btn-sm">💬 Telegram Admin</a>
          <button className="btn btn-primary btn-sm" onClick={() => navigate("#/register")}>Maktab ochish</button>
        </div>
      </nav>

      {/* ROUTING */}
      {route === "#/" && <HomePage navigate={navigate} />}
      {route === "#/courses" && <CoursesPage navigate={navigate} />}
      {route === "#/pricing" && <PricingPage navigate={navigate} />}
      {route === "#/dashboard" && <DashboardPage navigate={navigate} currentUser={currentUser} showNotification={showNotification} />}
      {route === "#/register" && <RegisterPage navigate={navigate} setCurrentUser={setCurrentUser} showNotification={showNotification} />}

      <footer style={{ borderTop: "1px solid var(--border-glass)", padding: "3rem 0", marginTop: "5rem", textAlign: "center", color: "var(--text-dim)" }}>
        <div className="container">
          <p>© 2026 Exode.biz — Onlayn Maktab va Kurslar Platformasi. Telegram Admin Checkout: @{TELEGRAM_ADMIN_HANDLE}</p>
        </div>
      </footer>
    </div>
  );
}

function HomePage({ navigate }) {
  return (
    <div className="container" style={{ textAlign: "center", padding: "4rem 0" }}>
      <h1 className="hero-title">O'z Onlayn Maktabingizni <br /><span className="text-gradient">Exode.biz bilan Barpo Eting</span></h1>
      <p className="hero-desc">Kinescope video xavfsizligi, Kommo CRM avto-lidi, Telegram Admin orqali to'lov hamda Gmail bepul OTP tasdiqlash.</p>
      <div style={{ display: "flex", gap: 16, justifyContent: "center", marginTop: 24 }}>
        <button className="btn btn-primary" onClick={() => navigate("#/register")}>Maktab Ochish (14 kun bepul)</button>
        <a href={TELEGRAM_ADMIN_URL} target="_blank" className="btn btn-secondary">💬 Telegram Admin bilan Bog'lanish</a>
      </div>
    </div>
  );
}

function CoursesPage({ navigate }) {
  return (
    <div className="container">
      <h2>Barcha Kurslar Katalogi</h2>
      <div className="grid-2" style={{ marginTop: 20 }}>
        {INITIAL_COURSES.map(c => (
          <div key={c.id} className="glass-panel" style={{ padding: "2rem" }}>
            <h3>{c.title}</h3>
            <p style={{ color: "var(--text-muted)", margin: "10px 0" }}>{c.description}</p>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 20 }}>
              <span style={{ fontSize: "1.2rem", fontWeight: 700, color: "var(--accent)" }}>{c.price.toLocaleString()} UZS</span>
              <a href={`https://t.me/${TELEGRAM_ADMIN_HANDLE}?text=Assalomu%20alaykum!%20${encodeURIComponent(c.title)}%20kursini%20xarid%20qilmoqchiman.`} target="_blank" className="btn btn-primary">
                💬 Telegramda Xarid Qilish
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PricingPage({ navigate }) {
  return (
    <div className="container">
      <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
        <h2>Maktablar uchun Tarif Rejalari</h2>
        <p style={{ color: "var(--text-muted)" }}>Admin bilan Telegram orqali bog'lanib tarifni faollashtiring</p>
      </div>

      <div className="grid-3">
        <div className="glass-panel" style={{ padding: "2.5rem", textAlign: "center" }}>
          <h3>Boshlang'ich (Start)</h3>
          <div style={{ margin: "20px 0", fontSize: "2rem", fontWeight: 800 }}>490,000 UZS / oy</div>
          <a href={`https://t.me/${TELEGRAM_ADMIN_HANDLE}?text=Assalomu%20alaykum!%20Start%20tarifini%20faollashtirmoqchiman.`} target="_blank" className="btn btn-primary" style={{ width: "100%", justifyContent: "center" }}>
            💬 Admin bilan Bog'lanish
          </a>
        </div>
        <div className="glass-panel pulse-card" style={{ padding: "2.5rem", textAlign: "center", border: "1px solid var(--primary)" }}>
          <h3>Professional (Pro)</h3>
          <div style={{ margin: "20px 0", fontSize: "2rem", fontWeight: 800 }}>990,000 UZS / oy</div>
          <a href={`https://t.me/${TELEGRAM_ADMIN_HANDLE}?text=Assalomu%20alaykum!%20Pro%20tarifini%20faollashtirmoqchiman.`} target="_blank" className="btn btn-primary" style={{ width: "100%", justifyContent: "center" }}>
            💬 Admin bilan Bog'lanish
          </a>
        </div>
        <div className="glass-panel" style={{ padding: "2.5rem", textAlign: "center" }}>
          <h3>Korporativ (Enterprise)</h3>
          <div style={{ margin: "20px 0", fontSize: "2rem", fontWeight: 800 }}>2,400,000 UZS / oy</div>
          <a href={`https://t.me/${TELEGRAM_ADMIN_HANDLE}?text=Assalomu%20alaykum!%20Enterprise%20tarifini%20faollashtirmoqchiman.`} target="_blank" className="btn btn-primary" style={{ width: "100%", justifyContent: "center" }}>
            💬 Admin bilan Bog'lanish
          </a>
        </div>
      </div>
    </div>
  );
}

function RegisterPage({ navigate, setCurrentUser, showNotification }) {
  const [selectedRole, setSelectedRole] = useState("school_owner");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();
    setCurrentUser({ name, email, role: selectedRole });
    showNotification("Maktabingiz yaratildi! Gmail pochtangizga tasdiqlash kodi yuborildi.");
    navigate("#/dashboard");
  };

  return (
    <div className="container" style={{ maxWidth: 550, marginTop: "2rem" }}>
      <div className="glass-panel" style={{ padding: "2.5rem" }}>
        <h2 style={{ textAlign: "center", marginBottom: 20 }}>Sizga to'g'ri keladigan variantni tanlang</h2>
        <div style={{ display: "flex", flexDirection: "column", gap: 10, marginBottom: 20 }}>
          {ONBOARDING_ROLES.map(role => (
            <div key={role.id} onClick={() => setSelectedRole(role.id)} style={{ padding: "12px 16px", borderRadius: 12, background: selectedRole === role.id ? "rgba(99, 102, 241, 0.15)" : "rgba(255,255,255,0.03)", border: selectedRole === role.id ? "2px solid var(--primary)" : "1px solid var(--border-glass)", cursor: "pointer", display: "flex", alignItems: "center", gap: 12, fontWeight: 600 }}>
              <span>{role.icon}</span>
              <span>{role.title}</span>
            </div>
          ))}
        </div>
        <form onSubmit={handleRegister}>
          <div className="form-group">
            <label className="form-label">To'liq Ismingiz</label>
            <input type="text" className="form-input" required value={name} onChange={e => setName(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">Gmail Emailingiz (OTP Tasdiqlash)</label>
            <input type="email" className="form-input" required value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: "100%", justifyContent: "center", marginTop: 12 }}>Davom Etish</button>
        </form>
      </div>
    </div>
  );
}

function DashboardPage({ currentUser, showNotification }) {
  return (
    <div className="container">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <h2>Maktab Boshqaruv Paneli (Admin)</h2>
        <button className="btn btn-primary" onClick={() => showNotification("O'quvchiga kursga kirish huquqi berildi!")}>
          + O'quvchiga Kirish Huquqini Berish
        </button>
      </div>
      <div className="glass-panel" style={{ padding: "2rem" }}>
        <h3>Murojaatlar va Kommo CRM Loglari</h3>
        <p style={{ color: "var(--text-muted)", marginTop: 8 }}>Telegram orqali kelgan to'lov murojaatlari va CRM lidi</p>
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
