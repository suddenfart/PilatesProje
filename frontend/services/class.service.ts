import { api } from "@/lib/api";

export type ClassType = {
  id: number;
  start_time: string;
  end_time: string;
  capacity: number;
};

export async function getClasses(): Promise<ClassType[]> {
  return api<ClassType[]>("/classes/");
}

export async function createClass(data: {
  start_time: string;
  end_time: string;
  capacity: number;
}) {
  return api("/classes/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}