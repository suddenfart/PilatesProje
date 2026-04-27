"use client";

import { createBooking } from "@/lib/api";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  classItem: any;
};

export default function BookingModal({ isOpen, onClose, classItem }: Props) {
  if (!isOpen || !classItem) return null;

  const handleConfirm = async () => {
    try {
      await createBooking(classItem.id);
      alert("Booking successful ✅");
      onClose();
    } catch (err: any) {
      alert(err.message || "Booking failed ❌");
    }
  };

  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center">
      
      <div className="bg-gray-900 p-6 rounded-xl w-96 border border-gray-700">

        <h2 className="text-xl font-bold mb-3">
          📅 Pilates Class #{classItem.id}
        </h2>

        <div className="space-y-2 text-sm text-gray-300">
          <p>🕒 Start: {new Date(classItem.start_time).toLocaleString()}</p>
          <p>🕒 End: {new Date(classItem.end_time).toLocaleString()}</p>
          <p>👥 Capacity: {classItem.capacity}</p>
        </div>

        {/* ACTIONS */}
        <div className="flex gap-2 mt-5">

          <button
            onClick={onClose}
            className="flex-1 bg-gray-700 py-2 rounded"
          >
            Cancel
          </button>

          <button
            onClick={handleConfirm}
            className="flex-1 bg-purple-600 py-2 rounded"
          >
            Confirm
          </button>

        </div>

      </div>
    </div>
  );
}