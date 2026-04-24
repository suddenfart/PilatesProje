import { getToken } from "./auth";

const API_URL = "http://127.0.0.1:8000";

// 🔥 GENERIC FETCH WITH AUTH
export async function apiFetch(url: string, options: RequestInit = {}) {
  const token = getToken();

  return fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
}