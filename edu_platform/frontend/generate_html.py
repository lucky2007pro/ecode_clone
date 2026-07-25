import os

base = r"d:\python najot ta'liim\fastapi\erp_platform\edu_platform\frontend"

def get_layout(title, content):
    return f"""<!DOCTYPE html>
<html lang="uz">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Exode.biz</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="./src/index.css">
  <style>
    .dropdown-container {{ position: relative; display: inline-block; }}
    .dropdown-menu {{ display: none; position: absolute; top: 100%; left: -100px; width: 680px; padding: 1.5rem; background: #0c1322; border: 1px solid rgba(255,255,255,0.15); border-radius: 20px; grid-template-columns: 1fr 1fr; gap: 1rem; z-index: 1000; box-shadow: 0 25px 60px rgba(0,0,0,0.8); }}
    .dropdown-container:hover .dropdown-menu {{ display: grid; }}
    .dropdown-item {{ display: flex; align-items: flex-start; gap: 12px; padding: 12px; border-radius: 12px; text-decoration: none; color: inherit; transition: background 0.2s; }}
    .dropdown-item:hover {{ background: rgba(255,255,255,0.06); }}
    .dropdown-icon {{ width: 42px; height: 42px; border-radius: 10px; background: rgba(99,102,241,0.15); border: 1px solid rgba(99,102,241,0.3); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; flex-shrink: 0; }}
  </style>
</head>
<body>
  <div class="bg-glow"></div>
  <nav class="navbar">
    <a href="index.html" class="nav-brand">
      <div class="brand-icon">⚡</div>
      <span>exode<span class="text-gradient">.biz</span></span>
    </a>
    <ul class="nav-links">
      <li class="dropdown-container">
        <span class="nav-link" style="cursor:pointer">Imkoniyatlar ▼</span>
        <div class="dropdown-menu">
          <a href="features.html" class="dropdown-item"><div class="dropdown-icon">📑</div><div><div style="font-weight:700;color:#fff">Barcha imkoniyatlar</div><div style="font-size:0.8rem;color:#94a3b8">Bitta platformada 11 ta vosita</div></div></a>
          <a href="course-builder.html" class="dropdown-item"><div class="dropdown-icon">🎛️</div><div><div style="font-weight:700;color:#fff">Kurs konstruktori</div><div style="font-size:0.8rem;color:#94a3b8">Video, matn, testlar — vizual muharrir</div></div></a>
          <a href="homework.html" class="dropdown-item"><div class="dropdown-icon">📝</div><div><div style="font-weight:700;color:#fff">Uy vazifalari</div><div style="font-size:0.8rem;color:#94a3b8">Testlar, topshiriqlar va avto-tekshirish</div></div></a>
          <a href="payments.html" class="dropdown-item"><div class="dropdown-icon">💳</div><div><div style="font-weight:700;color:#fff">To'lovlarni qabul qilish</div><div style="font-size:0.8rem;color:#94a3b8">Payme, Click, Uzum va rossiya kartalari</div></div></a>
          <a href="installments.html" class="dropdown-item"><div class="dropdown-icon">🔄</div><div><div style="font-weight:700;color:#fff">Bo'lib-bo'lib to'lash</div><div style="font-size:0.8rem;color:#94a3b8">Avto-yechib olish va bosqichma-bosqich...</div></div></a>
          <a href="customization.html" class="dropdown-item"><div class="dropdown-icon">🎨</div><div><div style="font-weight:700;color:#fff">Maktab kastomizatsiyasi</div><div style="font-size:0.8rem;color:#94a3b8">O'z brendingiz, ranglar va domen</div></div></a>
          <a href="analytics.html" class="dropdown-item"><div class="dropdown-icon">📈</div><div><div style="font-weight:700;color:#fff">Analitika</div><div style="font-size:0.8rem;color:#94a3b8">Daromad, faollik va o'quvchi xulqi</div></div></a>
          <a href="messenger.html" class="dropdown-item"><div class="dropdown-icon">💬</div><div><div style="font-weight:700;color:#fff">Messendjer</div><div style="font-size:0.8rem;color:#94a3b8">Platforma ichida o'quvchilar bilan suhbat</div></div></a>
          <a href="marketing.html" class="dropdown-item"><div class="dropdown-icon">📢</div><div><div style="font-weight:700;color:#fff">Marketing va sotuv</div><div style="font-size:0.8rem;color:#94a3b8">Piksellar, UTM, jo'natmalar va tripvayrlar</div></div></a>
          <a href="docs.html" class="dropdown-item"><div class="dropdown-icon">💻</div><div><div style="font-weight:700;color:#fff">API hujjatlar</div><div style="font-size:0.8rem;color:#94a3b8">Hujjatlar va integratsiyalar</div></div></a>
        </div>
      </li>
      <li><a href="courses.html" class="nav-link">Kurslar Catalog</a></li>
      <li><a href="pricing.html" class="nav-link">Tariflar & Bo'lib to'lash</a></li>
      <li><a href="dashboard.html" class="nav-link">Dashboard</a></li>
    </ul>
    <div style="display:flex;gap:10px">
      <a href="login.html" class="btn btn-secondary btn-sm">Kirish</a>
      <a href="register.html" class="btn btn-primary btn-sm">Maktab ochish</a>
    </div>
  </nav>

  {content}

  <footer style="border-top:1px solid var(--border-glass);padding:3rem 0;margin-top:5rem;text-align:center;color:var(--text-dim)">
    <div class="container">
      <p>© 2026 Exode.biz — Onlayn Maktab va Kurslar Platformasi. Barcha huquqlar himoyalangan.</p>
    </div>
  </footer>
</body>
</html>"""

# Pages map with full rich contents
pages = {
    "course-builder.html": ("Kurs Konstruktori", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-primary">Vizual Muharrir</span>
    <h1 style="font-size:2.8rem;margin:12px 0">Kurs Konstruktori</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">Video, matn, testlar va fayllardan iborat kurslarni bir necha daqiqada vizual konstruktor orqali noldan yarating.</p>
    <div style="margin-top:24px;display:flex;gap:12px">
      <a href="courses.html" class="btn btn-primary">Demo Kurslarni Ko'rish</a>
      <a href="register.html" class="btn btn-secondary">Sinab ko'rish</a>
    </div>
  </div>

  <div class="grid-2">
    <div class="glass-panel" style="padding:2rem">
      <h3>📹 Kinescope Video Integratsiyasi</h3>
      <p style="color:var(--text-muted);margin-top:10px">Videolaringiz serverga tushmaydi. Kinescope API orqali to'g'ridan-to'g'ri bulutga yuklanadi, 4K transkodlanadi va DRM bilan himoyalanadi.</p>
    </div>
    <div class="glass-panel" style="padding:2rem">
      <h3>📚 Modullar va Darslar Tartibi</h3>
      <p style="color:var(--text-muted);margin-top:10px">Darslarni modullarga ajrating, darslar ketma-ketligini o'rnating hamda bepul sinov (Free Preview) darslarini belgilang.</p>
    </div>
  </div>
</div>
"""),

    "homework.html": ("Uy Vazifalari va Testlar", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-success">7 xil vazifa turi</span>
    <h1 style="font-size:2.8rem;margin:12px 0">Uy Vazifalari va Testlar</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">Testlar, moslashtirish, mantiqiy tanlov, matnli topshiriqlar va fayl yuklash — avto-tekshirish hamda kurator baholash imkoniyati bilan.</p>
  </div>
  <div class="grid-3">
    <div class="glass-panel" style="padding:1.5rem">
      <h4>⚡ Avto-Tekshirish</h4>
      <p style="color:var(--text-muted);font-size:0.9rem;margin-top:8px">Test va moslashtirish vazifalarida to'g'ri javoblar kaliti bo'yicha bal darhol avtomatik hisoblanadi.</p>
    </div>
    <div class="glass-panel" style="padding:1.5rem">
      <h4>👨‍🏫 Kurator Baholashi</h4>
      <p style="color:var(--text-muted);font-size:0.9rem;margin-top:8px">Matnli va faylli vazifalarni kuratorlar tekshirib, izoh hamda bal qo'yadi.</p>
    </div>
    <div class="glass-panel" style="padding:1.5rem">
      <h4>📜 Avto-Sertifikat</h4>
      <p style="color:var(--text-muted);font-size:0.9rem;margin-top:8px">Barcha vazifa va darslarni yakunlagan o'quvchiga avtomatik PDF sertifikat beriladi.</p>
    </div>
  </div>
</div>
"""),

    "payments.html": ("To'lovlarni Qabul Qilish", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-warning">Payme & Click & Uzum</span>
    <h1 style="font-size:2.8rem;margin:12px 0">To'lovlarni Qabul Qilish</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">O'quvchilar Payme, Click, Uzum Bank yoki Visa/Mastercard orqali bir zumda to'laydi. To'lov o'tgach kurs avtomatik ochiladi.</p>
  </div>
  <div class="grid-3">
    <div class="glass-panel" style="padding:2rem;text-align:center">
      <h2 style="color:#38bdf8">Payme Merchant</h2>
      <p style="color:var(--text-muted);margin-top:8px">JSON-RPC 2.0 Instant Check & Perform transaction</p>
    </div>
    <div class="glass-panel" style="padding:2rem;text-align:center">
      <h2 style="color:#34d399">Click Merchant</h2>
      <p style="color:var(--text-muted);margin-top:8px">Prepare & Complete checkout protocol</p>
    </div>
    <div class="glass-panel" style="padding:2rem;text-align:center">
      <h2 style="color:#c084fc">Uzum Bank</h2>
      <p style="color:var(--text-muted);margin-top:8px">Quick checkout and installment integration</p>
    </div>
  </div>
</div>
"""),

    "installments.html": ("Bo'lib-bo'lib To'lash", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-primary">Auto-debit Subscription</span>
    <h1 style="font-size:2.8rem;margin:12px 0">Bo'lib-bo'lib To'lash (Installments)</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">O'quvchilar kartani 1 marta bog'laydi — har oy to'lov kartadan avtomatik yechib olinadi va kurs modullari bosqichma-bosqich ochiladi.</p>
  </div>
</div>
"""),

    "customization.html": ("Maktab Kastomizatsiyasi", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-success">White-Label & Custom Domain</span>
    <h1 style="font-size:2.8rem;margin:12px 0">Maktab Kastomizatsiyasi</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">O'z brendingiz, shaxsiy domeningiz (maktabim.uz), logoniz va brend ranglaringiz bilan to'liq shaxsiy platformaga ega bo'ling.</p>
  </div>
</div>
"""),

    "analytics.html": ("Analitika va Sotuv Voronkasi", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-warning">Real-time Dashbord</span>
    <h1 style="font-size:2.8rem;margin:12px 0">Ta'lim va Sotuv Analitikasi</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">O'quvchilar faolligi, daromad statistikasi, yetib borish foizi, NPS ko'rsatkichi hamda sotuv voronkasi — barcha ma'lumotlar bitta joyda.</p>
  </div>
</div>
"""),

    "messenger.html": ("Messendjer Live Chat", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-primary">WebSocket Live Chat</span>
    <h1 style="font-size:2.8rem;margin:12px 0">Platforma Ichidagi Messendjer</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">O'quvchi va kuratorlar o'rtasida real-time muloqot, fayl ulashish va savol-javoblar tizimi.</p>
  </div>
</div>
"""),

    "marketing.html": ("Marketing va Sotuv", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-success">FB Pixel & GA4 & UTM</span>
    <h1 style="font-size:2.8rem;margin:12px 0">Marketing va Sotuv Vositalari</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">Facebook Pixel, Google Analytics 4, UTM metkalar kuzatuvi hamda Telegram yopiq kanallariga avtomatik taklif nomalari.</p>
  </div>
</div>
"""),

    "docs.html": ("API Hujjatlar va Integratsiyalar", """
<div class="container">
  <div class="glass-panel" style="padding:3rem;margin-bottom:3rem">
    <span class="badge badge-primary">FastAPI Swagger / OpenAPI 3.0</span>
    <h1 style="font-size:2.8rem;margin:12px 0">API Hujjatlar va Integratsiyalar</h1>
    <p style="font-size:1.2rem;color:var(--text-muted);max-width:800px">Exode REST API hujjatlari. Dasturchilar va uchinchi tomon tizimlar uchun ochiq API endpointlar.</p>
  </div>
  <div class="glass-panel" style="padding:2rem">
    <h3>API Endpoint Misoli (Curl)</h3>
    <pre style="background:#050811;padding:1.25rem;border-radius:12px;margin-top:12px;color:#818cf8;font-size:0.9rem">curl -X POST https://api.exode.biz/api/v1/auth/register \\
  -H "Content-Type: application/json" \\
  -d '{{
    "email": "student@exode.biz",
    "password": "secretpassword",
    "full_name": "Jasur Alimov",
    "school_id": "8f3d1b2c-..."
  }}'</pre>
  </div>
</div>
"""),

    "features.html": ("Barcha Imkoniyatlar", """
<div class="container">
  <div style="text-align:center;margin-bottom:3rem">
    <span class="badge badge-primary" style="margin-bottom:12px">Bitta platformada 11 ta vosita</span>
    <h2>Exode.biz Barcha Imkoniyatlari</h2>
  </div>
  <div class="grid-3">
    <a href="course-builder.html" style="text-decoration:none;color:inherit"><div class="glass-panel glass-panel-interactive" style="padding:2rem"><h3>🎛️ Kurs konstruktori</h3><p style="color:var(--text-muted);margin-top:8px">Video, matn, testlar — vizual muharrir</p></div></a>
    <a href="homework.html" style="text-decoration:none;color:inherit"><div class="glass-panel glass-panel-interactive" style="padding:2rem"><h3>📝 Uy vazifalari</h3><p style="color:var(--text-muted);margin-top:8px">Testlar, topshiriqlar va avto-tekshirish</p></div></a>
    <a href="payments.html" style="text-decoration:none;color:inherit"><div class="glass-panel glass-panel-interactive" style="padding:2rem"><h3>💳 To'lovlarni qabul qilish</h3><p style="color:var(--text-muted);margin-top:8px">Payme, Click, Uzum va rossiya kartalari</p></div></a>
    <a href="installments.html" style="text-decoration:none;color:inherit"><div class="glass-panel glass-panel-interactive" style="padding:2rem"><h3>🔄 Bo'lib-bo'lib to'lash</h3><p style="color:var(--text-muted);margin-top:8px">Avto-yechib olish va bosqichma-bosqich...</p></div></a>
    <a href="customization.html" style="text-decoration:none;color:inherit"><div class="glass-panel glass-panel-interactive" style="padding:2rem"><h3>🎨 Maktab kastomizatsiyasi</h3><p style="color:var(--text-muted);margin-top:8px">O'z brendingiz, ranglar va domen</p></div></a>
    <a href="analytics.html" style="text-decoration:none;color:inherit"><div class="glass-panel glass-panel-interactive" style="padding:2rem"><h3>📈 Analitika</h3><p style="color:var(--text-muted);margin-top:8px">Daromad, faollik va o'quvchi xulqi</p></div></a>
  </div>
</div>
"""),

    "pricing.html": ("Tariflar & Bo'lib to'lash", """
<div class="container">
  <div style="text-align:center;margin-bottom:2.5rem">
    <h2>Maktablar uchun Tarif Rejalari</h2>
    <p style="color:var(--text-muted)">O'zingizga mos tarif rejasi bilan maktabingizni kengaytiring</p>
  </div>
  <div class="grid-3">
    <div class="glass-panel" style="padding:2.5rem">
      <h3>Boshlang'ich (Start)</h3>
      <div style="margin:20px 0"><span style="font-size:2.5rem;font-weight:800">490,000</span> UZS / oy</div>
      <a href="register.html" class="btn btn-primary" style="width:100%;justify-content:center">Tarifni Tanlash</a>
    </div>
    <div class="glass-panel pulse-card" style="padding:2.5rem;border:1px solid var(--primary)">
      <h3>Professional (Pro)</h3>
      <div style="margin:20px 0"><span style="font-size:2.5rem;font-weight:800">990,000</span> UZS / oy</div>
      <a href="register.html" class="btn btn-primary" style="width:100%;justify-content:center">Tarifni Tanlash</a>
    </div>
    <div class="glass-panel" style="padding:2.5rem">
      <h3>Korporativ (Enterprise)</h3>
      <div style="margin:20px 0"><span style="font-size:2.5rem;font-weight:800">2,400,000</span> UZS / oy</div>
      <a href="register.html" class="btn btn-primary" style="width:100%;justify-content:center">Tarifni Tanlash</a>
    </div>
  </div>
</div>
"""),

    "dashboard.html": ("Boshqaruv Paneli", """
<div class="container">
  <h2>Maktab Boshqaruv Paneli (Dashboard)</h2>
  <p style="color:var(--text-muted);margin-bottom:20px">Kommo CRM va Kinescope integratsiya statistikasi</p>
  <div class="grid-4">
    <div class="glass-panel" style="padding:1.5rem"><p style="color:var(--text-dim);font-size:0.85rem">Jami O'quvchilar</p><h3 style="font-size:2rem;color:var(--accent)">240 ta</h3></div>
    <div class="glass-panel" style="padding:1.5rem"><p style="color:var(--text-dim);font-size:0.85rem">Jami Daromad</p><h3 style="font-size:2rem;color:var(--success)">18.4M UZS</h3></div>
    <div class="glass-panel" style="padding:1.5rem"><p style="color:var(--text-dim);font-size:0.85rem">Kommo CRM Sync</p><h3 style="font-size:2rem;color:var(--primary)">5 req/s</h3></div>
    <div class="glass-panel" style="padding:1.5rem"><p style="color:var(--text-dim);font-size:0.85rem">Kinescope Storage</p><h3 style="font-size:2rem;color:var(--secondary)">14.2 GB</h3></div>
  </div>
</div>
""")
}

for fname, (title, content) in pages.items():
    filePath = os.path.join(base, fname)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(get_layout(title, content))

print("All 17 HTML files written with full content!")