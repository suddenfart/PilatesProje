"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getClasses, createBooking } from "@/lib/api";

export default function ClassesPage() {
  const router = useRouter();

  const [classes, setClasses] = useState<any[]>([]);
  const [selected, setSelected] = useState<any>(null);

  const [loading, setLoading] = useState(true);

  // 💎 PRO LEVEL: booked state (şimdilik fake, sonra backend’den gelecek)
  const [bookedMap, setBookedMap] = useState<Record<number, boolean>>({});

  useEffect(() => {
    const run = async () => {
      const user = localStorage.getItem("user");

      if (!user) {
        router.replace("/login");
        return;
      }

      const data = await getClasses();
      setClasses(data);

      setLoading(false);
    };

    run();
  }, [router]);

  // 🚀 HIZLI FIX VERSION
  const book = async (classId: number) => {
    try {
      await createBooking(classId);

      alert("Booked successfully 🎉");

      // 💎 UI update (optimistic)
      setBookedMap((prev) => ({
        ...prev,
        [classId]: true,
      }));
    } catch (err: any) {
      alert(err.message); // 👈 Already booked artık görünür
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
        Loading...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex gap-6 p-6">

      {/* LEFT - LIST */}
      <div className="flex-1 grid md:grid-cols-2 gap-4">

        {classes.map((c) => (
          <div
            key={c.id}
            onClick={() => setSelected(c)}
            className="cursor-pointer bg-gray-900 border border-gray-800 p-4 rounded-xl hover:border-purple-500 transition"
          >
            <h2 className="font-bold text-lg">
              Pilates Class #{c.id}
            </h2>

            <p className="text-sm text-gray-400">
              🕒 {new Date(c.start_time).toLocaleString()}
            </p>

            <p className="text-sm text-gray-400">
              👥 Capacity: {c.capacity}
            </p>
          </div>
        ))}

      </div>

      {/* RIGHT - DETAIL PANEL */}
      <div className="w-96 bg-gray-900 border border-gray-800 rounded-xl p-4">

        {selected ? (
          <>
            <h2 className="text-xl font-bold mb-4">
              📅 Class #{selected.id}
            </h2>

            <div className="space-y-2 text-sm text-gray-300">
              <p>🕒 Start: {new Date(selected.start_time).toLocaleString()}</p>
              <p>🕒 End: {new Date(selected.end_time).toLocaleString()}</p>
              <p>👥 Capacity: {selected.capacity}</p>
            </div>

            {/* 💎 PRO LEVEL BUTTON */}
            <button
              onClick={() => book(selected.id)}
              disabled={bookedMap[selected.id]}
              className="mt-6 w-full bg-purple-600 disabled:bg-gray-700 py-2 rounded-lg"
            >
              {bookedMap[selected.id]
                ? "Already Booked"
                : "Book This Class"}
            </button>

          </>
        ) : (
          <p className="text-gray-500">
            Select a class to see details
          </p>
        )}

      </div>

    </div>
  );
}