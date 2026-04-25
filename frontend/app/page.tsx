"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-indigo-600 to-purple-600 text-white">
      <h1 className="text-5xl font-bold mb-4">🏋️ Pilates Studio</h1>

      <p className="text-lg opacity-80 mb-8">
        Book your classes, manage your schedule
      </p>

      <div className="flex gap-4">
        <Link href="/classes">
          <button className="px-6 py-3 bg-white text-black rounded-xl font-medium hover:scale-105 transition">
            View Classes
          </button>
        </Link>

        <Link href="/login">
          <button className="px-6 py-3 border border-white rounded-xl hover:bg-white hover:text-black transition">
            Login
          </button>
        </Link>
      </div>
    </div>
  );
}