"use client";

import { useEffect, useState } from "react";
import { getClasses, createBooking } from "@/lib/api";

export default function ClassesPage() {
  const [classes, setClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [bookingId, setBookingId] = useState<number | null>(null);

  const fetchClasses = async () => {
    try {
      const data = await getClasses();
      setClasses(data);
    } catch (err: any) {
      console.error(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClasses();
  }, []);

  const handleBook = async (id: number) => {
    try {
      setBookingId(id);

      await createBooking(id);

      alert("Booked successfully!");

      // 🔥 listeyi yenile (çok önemli)
      await fetchClasses();

    } catch (err: any) {
      alert(err.message);
    } finally {
      setBookingId(null);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white p-10">
      <h1 className="text-2xl mb-6">Classes</h1>

      <div className="grid gap-4">
        {classes.map((c) => (
          <div key={c.id} className="bg-gray-800 p-4 rounded space-y-2">

            <p><b>Title:</b> {c.title}</p>
            <p><b>Start:</b> {c.start_time}</p>
            <p><b>End:</b> {c.end_time}</p>

            {/* Eğer backend capacity veriyorsa */}
            {c.capacity && (
              <p>
                Capacity: {c.capacity}
              </p>
            )}

            <button
              onClick={() => handleBook(c.id)}
              disabled={bookingId === c.id}
              className="mt-3 px-4 py-1 bg-green-600 rounded hover:bg-green-500 disabled:opacity-50"
            >
              {bookingId === c.id ? "Booking..." : "Book"}
            </button>

          </div>
        ))}
      </div>
    </div>
  );
}