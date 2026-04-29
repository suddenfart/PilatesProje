export async function login(email: string, password: string) {
  console.log("LOGIN REQUEST:", email, password);

  const res = await fetch(
    `http://127.0.0.1:8000/auth/login?email=${encodeURIComponent(
      email
    )}&password=${encodeURIComponent(password)}`,
    {
      method: "POST",
    }
  );

  const data = await res.json().catch(() => ({}));

  console.log("LOGIN RESPONSE:", data);

  if (!res.ok) {
    let message = "Giriş başarısız";

    if (typeof data.detail === "string") {
      message = data.detail;
    } else if (Array.isArray(data.detail)) {
      message = data.detail.map((d: any) => d.msg).join(", ");
    }

    throw new Error(message);
  }

  localStorage.setItem("user", JSON.stringify(data));

  return data;
}