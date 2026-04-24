"use client";

import { useEffect, useState } from "react";

export default function AdminPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws/admin");

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === "analytics_update") {
        setData(msg.data);
      }
    };

    return () => ws.close();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Admin Dashboard</h1>

      {!data ? (
        <p>Waiting for data...</p>
      ) : (
        <>
          <p>Bookings: {data.total_bookings}</p>
          <p>Classes: {data.total_classes}</p>
          <p>Occupancy: {data.occupancy_rate}%</p>
        </>
      )}
    </div>
  );
}