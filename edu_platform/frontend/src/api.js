
if (!import.meta.env.VITE_API_URL && import.meta.env.PROD) {
  throw new Error('VITE_API_URL env o\'zgaruvchisi production build uchun majburiy');
}

export const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8001/api/v1';
export const API_ORIGIN = API_URL.replace(/\/api\/v1\/?$/, '');
export const WS_URL = API_URL.replace(/^http/, 'ws');

export async function api(path, { method = 'GET', body, auth = true } = {}) {
  const headers = {};

  if (auth) {
    const token = localStorage.getItem('token');
    if (token) headers['Authorization'] = `Bearer ${token}`;
  }

  let requestBody = body;
  if (
    body &&
    typeof body === 'object' &&
    !(body instanceof URLSearchParams) &&
    !(body instanceof FormData) &&
    !(body instanceof Blob)
  ) {
    headers['Content-Type'] = 'application/json';
    requestBody = JSON.stringify(body);
  }

  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers,
    body: requestBody,
  });

  if (response.status === 401) {
    localStorage.removeItem('token');
    if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
      window.location.href = '/login';
    }
    throw new Error('Avtorizatsiya xatoligi (401). Qaytadan tizimga kiring.');
  }

  if (!response.ok) {
    let message = `So'rovda xatolik (status: ${response.status})`;
    try {
      const data = await response.json();
      if (data?.detail) {
        message = Array.isArray(data.detail)
          ? data.detail.map((d) => d.msg || d.type || String(d)).join(', ')
          : typeof data.detail === 'object'
            ? JSON.stringify(data.detail)
            : String(data.detail);
      }
    } catch {

    }
    throw new Error(message);
  }

  if (response.status === 204) return null;
  return response.json();
}
