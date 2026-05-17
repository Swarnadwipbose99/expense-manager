// main.js – shared helpers for Expense Manager

/**
 * apiFetch – wraps fetch with JWT injection.
 * Returns the raw Response so callers can check res.ok and call res.json() or res.blob().
 */
async function apiFetch(url, options = {}) {
  const token = localStorage.getItem('jwt');
  const headers = Object.assign({ 'Content-Type': 'application/json' }, options.headers || {});
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(url, Object.assign({}, options, { headers }));

  // Auto-redirect on 401
  if (res.status === 401) {
    localStorage.removeItem('jwt');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login';
  }
  return res;
}

// ── Theme toggle ─────────────────────────────────────────────────────────────
function initTheme() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-bs-theme', saved);
  const btn = document.getElementById('themeToggle');
  if (btn) {
    btn.textContent = saved === 'dark' ? '☀️ Light' : '🌙 Dark';
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-bs-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-bs-theme', next);
      localStorage.setItem('theme', next);
      btn.textContent = next === 'dark' ? '☀️ Light' : '🌙 Dark';
    });
  }
}

// ── Navbar auth state ─────────────────────────────────────────────────────────
function initNavbar() {
  const token = localStorage.getItem('jwt');
  const logoutBtn = document.getElementById('logoutBtn');
  if (logoutBtn) {
    if (token) {
      logoutBtn.classList.remove('d-none');
      logoutBtn.addEventListener('click', async () => {
        await apiFetch('/api/v1/auth/logout', { method: 'POST' });
        localStorage.removeItem('jwt');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
      });
    }
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavbar();
});
