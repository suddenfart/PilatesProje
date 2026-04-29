"use client";

import { useEffect, useState } from "react";
import { getMyBookings } from "@/lib/api";

export default function BookingsPage() {
  const [bookings, setBookings] = useState<any[]>([]);

  useEffect(() => {
    getMyBookings().then(setBookings);
  }, []);

  if (!bookings.length) {
    return (
      <div className="p-6 text-gray-400">
        No bookings yet
      </div>
    );
  }

  return (
    <div className="p-6 space-y-3">

      {bookings.map((b) => (
        <div
          key={b.id}
          className="bg-gray-900 p-4 rounded-xl border border-gray-800"
        >

          <p className="font-bold">
            🧘 Pilates Session
          </p>

          <p className="text-sm text-gray-400">
            🕒 {new Date(b.start_time).toLocaleString()}
          </p>

          <p className="text-sm text-gray-400">
            ➝ {new Date(b.end_time).toLocaleString()}
          </p>

        </div>
      ))}

    </div>
  );
}