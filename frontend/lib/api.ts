const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

// =====================
// TOKEN
// =====================
export function getToken() {
  if (typeof window === "undefined") return null;

  const user = localStorage.getItem("user");
  if (!user) return null;

  try {
    return JSON.parse(user).access_token;
  } catch {
    return null;
  }
}

// =====================
// SAFE FETCH
// =====================
async function safeFetch(url: string, options: any = {}) {
  const token = getToken();

  const res = await fetch(`${API_URL}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  const data = await res.json().catch(() => ({}));

  // 🔥 TOKEN EXPIRE HANDLING
  if (res.status === 401) {
    localStorage.removeItem("user");
    window.location.href = "/auth/login";
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    throw new Error(data.detail || "API error");
  }

  return data;
}

// =====================
// CLASSES
// =====================
export function getClasses() {
  return safeFetch("/classes");
}

// =====================
// BOOKINGS
// =====================
export function createBooking(class_id: number) {
  return safeFetch(`/bookings?class_id=${class_id}`, {
    method: "POST",
  });
}