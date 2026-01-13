// frontend/src/api/booking.api.ts — API онлайн-записи
// Назначение: работа с бронированием через backend

import { api } from "./client";

export type FreeSlotsResponse = {
  day: string;
  service_id: number;
  slots: string[];
};

export type CreateBookingPayload = {
  service_id: number;
  start_time: string;
  user_name: string;
  phone: string;
  email?: string;
};

export async function getFreeSlots(
  day: string,
  serviceId: number
): Promise<FreeSlotsResponse> {
  const res = await api.get<FreeSlotsResponse>("/booking/free", {
    params: {
      day,
      service_id: serviceId,
    },
  });
  return res.data;
}

export async function createBooking(payload: CreateBookingPayload) {
  const res = await api.post("/booking", payload);
  return res.data;
}

export async function cancelBooking(bookingId: number) {
  const res = await api.post(`/booking/${bookingId}/cancel`);
  return res.data;
}
