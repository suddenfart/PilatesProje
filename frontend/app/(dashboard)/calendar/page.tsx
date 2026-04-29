"use client";

import { useEffect, useState } from "react";
import { getClasses, updateClassTime } from "@/lib/api";
import { DndContext, useDraggable, useDroppable } from "@dnd-kit/core";

const hours = Array.from({ length: 12 }, (_, i) => i + 8);
const days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export default function CalendarPage() {
  const [classes, setClasses] = useState<any[]>([]);

  useEffect(() => {
    getClasses().then(setClasses);
  }, []);

  const handleDragEnd = async (event: any) => {
    const { active, over } = event;
    if (!over) return;

    const classId = Number(active.id);
    const [dayIndex, hour] = over.id.split("-");

    const start = new Date();
    start.setHours(Number(hour));

    const end = new Date(start);
    end.setHours(start.getHours() + 1);

    await updateClassTime(
      classId,
      start.toISOString(),
      end.toISOString()
    );

    const updated = await getClasses();
    setClasses(updated);
  };

  return (
    <div className="p-6 bg-gray-950 text-white min-h-screen">
      <h1 className="text-2xl font-bold mb-6">📅 Calendar</h1>

      <DndContext onDragEnd={handleDragEnd}>
        <div className="grid grid-cols-8 gap-2">
          <div></div>

          {days.map((d) => (
            <div key={d} className="text-center font-bold">
              {d}
            </div>
          ))}

          {hours.map((hour) => (
            <div key={hour} className="contents">
              <div className="text-gray-400 text-sm">
                {hour}:00
              </div>

              {days.map((_, dayIndex) => {
                const id = `${dayIndex}-${hour}`;

                const match = classes.find((c) => c.hour === hour);

                return (
                  <DroppableCell key={id} id={id}>
                    {match && (
                      <DraggableClass c={match} />
                    )}
                  </DroppableCell>
                );
              })}
            </div>
          ))}
        </div>
      </DndContext>
    </div>
  );
}

// ======================
// DRAGGABLE
// ======================
function DraggableClass({ c }: any) {
  const { attributes, listeners, setNodeRef, transform } =
    useDraggable({
      id: c.id,
    });

  return (
    <div
      ref={setNodeRef}
      {...listeners}
      {...attributes}
      style={{
        transform: transform
          ? `translate(${transform.x}px, ${transform.y}px)`
          : undefined,
      }}
      className="bg-purple-600 text-xs p-1 rounded cursor-grab"
    >
      🧘 Class
    </div>
  );
}

// ======================
// DROPPABLE
// ======================
function DroppableCell({ id, children }: any) {
  const { setNodeRef, isOver } = useDroppable({ id });

  return (
    <div
      ref={setNodeRef}
      className={`h-20 border ${
        isOver ? "bg-green-700" : "border-gray-800"
      }`}
    >
      {children}
    </div>
  );
}