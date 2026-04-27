"use client";

import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-gray-950 text-white flex">

      {/* SIDEBAR */}
      <aside className="w-64 bg-gray-900 border-r border-gray-800 p-4">

        <h1 className="text-xl font-bold mb-6">
          🧘 Pilates Studio
        </h1>

        <nav className="space-y-3">

          <Link href="/classes" className="block hover:text-purple-400">
            📅 Classes
          </Link>

          <Link href="/bookings" className="block hover:text-purple-400">
            📌 My Bookings
          </Link>

        </nav>

      </aside>

      {/* CONTENT */}
      <main className="flex-1 p-6">
        {children}
      </main>

    </div>
  );
}