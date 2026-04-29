"use client";

import { useEffect, useState } from "react";
import { getAdminClasses } from "@/lib/api";

export default function AdminPage() {
  const [classes, setClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);
        setError("");

        const data = await getAdminClasses();

        setClasses(data);
      } catch (err: any) {
        console.error(err);
        setError(err.message || "Failed loading admin data");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  if (loading) {
    return (
      <div className="p-6 text-white">
        Admin Dashboard Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 text-red-400">
        {error}
      </div>
    );
  }

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold mb-4">
        Admin Dashboard
      </h1>

      {classes.length === 0 ? (
        <p>No classes found</p>
      ) : (
        <div className="space-y-2">
          {classes.map((c) => (
            <div
              key={c.id}
              className="bg-gray-900 p-3 rounded"
            >
              Class #{c.id}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}