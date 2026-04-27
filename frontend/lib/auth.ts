import { api } from "./api";

export async function login(email: string, password: string) {
  const form = new URLSearchParams();
  form.append("username", email);
  form.append("password", password);

  const res = await fetch("http://127.0.0.1:8000/auth/login", {
    method: "POST",
    body: form,
  });

  if (!res.ok) throw new Error("Login failed");

  const data = await res.json();

  localStorage.setItem("token", data.access_token);
  localStorage.setItem("user_id", data.user_id);

  return data;
}

export async function register(email: string, password: string) {
  return api("/auth/register", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}