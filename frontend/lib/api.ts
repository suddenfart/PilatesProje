const API_URL = "http://127.0.0.1:8000";

/* =========================
   🔐 LOGIN
========================= */
export async function login(email: string, password: string) {
  const formData = new URLSearchParams();

  formData.append("username", email);
  formData.append("password", password);

  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data;
}

/* =========================
   📅 CLASSES
========================= */
export async function getClasses() {
  const userStr = localStorage.getItem("user");

  const token = userStr
    ? JSON.parse(userStr).access_token || JSON.parse(userStr).token
    : null;

  const res = await fetch(`${API_URL}/classes`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Failed to fetch classes");
  }

  return data;
}

/* =========================
   📌 BOOKING
========================= */
export async function createBooking(classId: number) {
  const userStr = localStorage.getItem("user");

  const token = userStr
    ? JSON.parse(userStr).access_token || JSON.parse(userStr).token
    : null;

  const res = await fetch(`${API_URL}/bookings`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      class_id: classId,
    }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Booking failed");
  }

  return data;
}