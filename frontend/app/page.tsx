"use client";

import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">

      {/* HERO SECTION */}
      <div className="flex flex-col items-center justify-center text-center px-6 py-24">
        <h1 className="text-5xl font-bold mb-4">
          Pilates Studio Management 🧘‍♀️
        </h1>

        <p className="text-gray-400 max-w-xl mb-8">
          Classes, bookings and instructors all in one modern platform.
          Manage your studio efficiently and effortlessly.
        </p>

        <div className="flex gap-4">
          <Link
            href="/login"
            className="px-6 py-3 bg-purple-600 hover:bg-purple-500 rounded-lg font-medium"
          >
            Get Started
          </Link>

          <Link
            href="/classes"
            className="px-6 py-3 bg-gray-800 hover:bg-gray-700 rounded-lg font-medium"
          >
            View Classes
          </Link>
        </div>
      </div>

      {/* FEATURES */}
      <div className="grid md:grid-cols-3 gap-6 px-10 pb-20">

        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h3 className="text-xl font-semibold mb-2">📅 Class Management</h3>
          <p className="text-gray-400 text-sm">
            Easily create, edit and manage all your pilates sessions.
          </p>
        </div>

        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h3 className="text-xl font-semibold mb-2">👥 Booking System</h3>
          <p className="text-gray-400 text-sm">
            Students can book classes instantly with real-time capacity tracking.
          </p>
        </div>

        <div className="bg-gray-900 p-6 rounded-xl border border-gray-800">
          <h3 className="text-xl font-semibold mb-2">📊 Analytics</h3>
          <p className="text-gray-400 text-sm">
            Track attendance, performance and studio growth.
          </p>
        </div>

      </div>

      {/* FOOTER */}
      <div className="text-center text-gray-600 text-sm pb-10">
        © {new Date().getFullYear()} Pilates App. All rights reserved.
      </div>

    </div>
  );
}