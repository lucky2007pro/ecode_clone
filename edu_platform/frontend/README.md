# Edu Platform — Frontend

Ta'lim platformasi (ERP/LMS) uchun frontend qismi. React + Vite asosida yozilgan bo'lib, kurslar, darslar, testlar, uy vazifalari, talabalar va analitika bo'limlarini o'z ichiga oladi. Backend sifatida FastAPI serveri ishlatiladi.

## Ishga tushirish

```bash
npm ci
cp .env.example .env   # kerak bo'lsa, VITE_API_URL ni o'zgartiring
npm run dev
```

Backend standart ravishda `http://localhost:8000` da ishlashi kerak. Boshqa manzil ishlatmoqchi bo'lsangiz, `.env` faylida `VITE_API_URL` ni belgilang.

## Buyruqlar

- `npm run dev` — lokal development server
- `npm run build` — production build
- `npm run preview` — build natijasini ko'rish
- `npm run lint` — kod tekshiruvi
