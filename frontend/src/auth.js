const AUTH_STORAGE_KEY = 'quiz-authenticated';

export function isAuthenticated() {
  return localStorage.getItem(AUTH_STORAGE_KEY) === '1';
}

export function login() {
  localStorage.setItem(AUTH_STORAGE_KEY, '1');
  window.dispatchEvent(new Event('auth-changed'));
}

export function logout() {
  localStorage.removeItem(AUTH_STORAGE_KEY);
  window.dispatchEvent(new Event('auth-changed'));
}
