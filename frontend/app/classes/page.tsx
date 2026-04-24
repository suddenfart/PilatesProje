"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type ClassItem = {
  id: number;
  start_time: string;
  end_time: string;
  capacity: number;
};

export default function ClassesPage() {
  const [classes, setClasses] = useState<ClassItem[]>([]);
  const [loading, setLoading] = useState(true);

  // 📦 CLASSES GET
  const fetchClasses = async () => {
    try {
      const res = await apiFetch("/classes/");
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail);

      setClasses(data);
    } catch (err) {
      console.error(err);
      alert("Classes load failed");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClasses();
  }, []);

  // 📌 BOOK CLASS
  const bookClass = async (class_id: number) => {
    try {
      const res = await apiFetch("/bookings/", {
        method: "POST",
        body: JSON.stringify({ class_id }),
      });

      const data = await res.json();

      if (!res.ok) {
        alert(data.detail || "Booking failed");
        return;
      }

      alert("Booked successfully 🚀");
    } catch (err) {
      console.error(err);
      alert("Error booking class");
    }
  };

  if (loading) return <p>Loading classes...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>Classes</h1>

      {classes.length === 0 && <p>No classes found</p>}

      <div style={{ display: "grid", gap: 10 }}>
        {classes.map((c) => (
          <div
            key={c.id}
            style={{
              border: "1px solid #ddd",
              padding: 10,
              borderRadius: 8,
            }}
          >
            <p>
              <b>ID:</b> {c.id}
            </p>

            <p>
              <b>Start:</b> {new Date(c.start_time).toLocaleString()}
            </p>

            <p>
              <b>End:</b> {new Date(c.end_time).toLocaleString()}
            </p>

            <p>
              <b>Capacity:</b> {c.capacity}
            </p>

            <button onClick={() => bookClass(c.id)}>Book</button>
          </div>
        ))}
      </div>
    </div>
  );
}