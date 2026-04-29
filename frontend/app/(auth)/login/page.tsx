"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    console.log("CLICKED");
    console.log("EMAIL:", email);
    console.log("PASSWORD:", password);

    try {
      await login(email, password);
      router.push("/classes");
    } catch (err: any) {
      console.error("LOGIN ERROR:", err.message);
      alert(err.message);
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-black text-white">
      <div className="p-6 bg-gray-900 rounded w-80 space-y-3">

        <input
          placeholder="Email"
          className="w-full p-2 bg-gray-800"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 bg-gray-800"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleLogin}
          className="w-full bg-purple-600 p-2"
        >
          Login
        </button>

      </div>
    </div>
  );
}