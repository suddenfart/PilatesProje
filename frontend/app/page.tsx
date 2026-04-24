"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import Link from "next/link";

export default function HomePage() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setUser(token ? "logged-in" : null);
  }, []);

  return (
    <div style={{ padding: 30 }}>
      <h1>🏋️ Pilates App</h1>

      <p>Welcome to your booking system</p>

      <div style={{ marginTop: 20, display: "flex", gap: 10 }}>
        <Link href="/classes">
          <button>View Classes</button>
        </Link>

        {!user && (
          <Link href="/login">
            <button>Login</button>
          </Link>
        )}
      </div>

      {user && (
        <div style={{ marginTop: 20 }}>
          <p>✅ Logged in</p>
        </div>
      )}
    </div>
  );
}