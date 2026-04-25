const API_URL = "http://127.0.0.1:8000";

export async function apiFetch(url: string, options: RequestInit = {}) {
  console.log("📡 API CALL:", API_URL + url);

  return fetch(API_URL + url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
}