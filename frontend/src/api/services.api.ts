// frontend/src/api/services.api.ts — API услуг
// Назначение: загрузка услуг из backend

import { api } from "./client";

export type Service = {
  id: number;
  name: string;
  price: number;
  duration_minutes: number;
};

export async function getServices(): Promise<Service[]> {
  const res = await api.get<Service[]>("/services");
  return res.data;
}
