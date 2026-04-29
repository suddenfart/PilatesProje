"use client";

import { useEffect, useState } from "react";

type AdminStats = {
  total_bookings: number;
  total_classes: number;
  occupancy_rate: number;
};

export default function AdminPage() {
  const [data, setData] = useState<AdminStats | null>(null);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/admin");

    ws.onopen = () => {
      console.log("WS connected");
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data);
        console.log("WS DATA:", msg);

        // 💎 REAL BACKEND DATA
        if (msg.total_bookings !== undefined) {
          setData({
            total_bookings: msg.total_bookings,
            total_classes: msg.total_classes,
            occupancy_rate: msg.occupancy_rate,
          });
          return;
        }

        // 🧪 TEST MODE SUPPORT
        if (msg.type === "test") {
          setData({
            total_bookings: 5,
            total_classes: 3,
            occupancy_rate: 66,
          });
        }
      } catch (err) {
        console.error("WS parse error:", err);
      }
    };

    ws.onerror = () => {
      console.warn("WS connection issue (ignore if reconnects)");
    };

    ws.onclose = () => {
      console.warn("WS closed");
    };

    return () => ws.close();
  }, []);

  return (
    <div className="p-6 text-white">
      <h1 className="text-2xl font-bold mb-6">
        Admin Dashboard
      </h1>

      {!data ? (
        <p className="text-gray-400">
          Waiting for data...
        </p>
      ) : (
        <div className="space-y-2">
          <p>Bookings: {data.total_bookings}</p>
          <p>Classes: {data.total_classes}</p>
          <p>Occupancy: {data.occupancy_rate}%</p>
        </div>
      )}
    </div>
  );
}