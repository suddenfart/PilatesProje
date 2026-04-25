"use client";

import { useEffect, useState } from "react";

type ClassItem = {
  id: number;
  start_time: string;
  end_time: string;
  capacity: number;
};

export default function Page() {
  const [classes, setClasses] = useState<ClassItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log("🔥 EFFECT STARTED");

    const load = async () => {
      try {
        console.log("🚀 FETCH START");

        const res = await fetch("http://127.0.0.1:8000/classes/");

        console.log("📥 STATUS:", res.status);

        const data = await res.json();

        console.log("📦 DATA:", data);

        if (Array.isArray(data)) {
          setClasses([...data]);
        } else {
          console.warn("⚠️ DATA NOT ARRAY:", data);
          setClasses([]);
        }
      } catch (err) {
        console.error("❌ FETCH ERROR:", err);
      } finally {
        console.log("🏁 LOADING FALSE");
        setLoading(false);
      }
    };

    load();
  }, []);

  console.log("🔁 RENDER STATE:", classes);

  if (loading) return <p>Loading classes...</p>;

  return (
    <div style={{ padding: 20 }}>
      <h1>Classes</h1>

      {classes.length === 0 ? (
        <p>No classes</p>
      ) : (
        classes.map((c) => (
          <div key={c.id}>
            <p>ID: {c.id}</p>
            <p>{c.start_time}</p>
            <p>{c.end_time}</p>
            <p>{c.capacity}</p>
          </div>
        ))
      )}
    </div>
  );
}