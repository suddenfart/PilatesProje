"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  const navItem = (href: string, label: string) => {
    const active = pathname === href;

    return (
      <Link
        href={href}
        className={`block px-3 py-2 rounded-lg transition ${
          active
            ? "bg-purple-600 text-white"
            : "text-gray-400 hover:text-white hover:bg-gray-800"
        }`}
      >
        {label}
      </Link>
    );
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white flex">

      {/* SIDEBAR */}
      <aside className="w-64 bg-gray-900 border-r border-gray-800 p-5">

        <h1 className="text-xl font-bold mb-6">
          🧘 Pilates Studio
        </h1>

        <nav className="space-y-2">
          {navItem("/classes", "📅 Classes")}
          {navItem("/bookings", "📌 My Bookings")}
          {navItem("/calendar", "🗓 Calendar")}
          {navItem("/admin", "⚙️ Admin")}
        </nav>

      </aside>

      {/* CONTENT */}
      <main className="flex-1 p-6">
        {children}
      </main>

    </div>
  );
}