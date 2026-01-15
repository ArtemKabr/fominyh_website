// frontend/src/pages/Admin/AdminPage.tsx — админ-панель салона
// Назначение: управление записями

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./admin.css";

type Booking = {
  id: number;
  start_time: string;
  status: string;
  service: {
    name: string;
    price: number;
  };
  user: {
    name: string;
    phone: string;
    email: string;
  };
};

export function AdminPage() {
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  const [bookings, setBookings] = useState<Booking[]>([]);

  const loadBookings = async () => {
    const res = await fetch("/api/admin/bookings", {
      headers: { "X-User-Id": userId! },
    });

    if (res.status === 403) {
      navigate("/account");
      return;
    }

    setBookings(await res.json());
  };

  useEffect(() => {
    if (!userId) {
      navigate("/login");
      return;
    }

    loadBookings();
  }, [userId]);

  const confirmBooking = async (id: number) => {
    await fetch(`/api/admin/bookings/${id}/confirm`, {
      method: "POST",
      headers: { "X-User-Id": userId! },
    });

    await loadBookings(); // ✅ ОБНОВЛЕНИЕ
  };

  const cancelBooking = async (id: number) => {
    await fetch(`/api/admin/bookings/${id}/cancel`, {
      method: "POST",
      headers: { "X-User-Id": userId! },
    });

    await loadBookings(); // ✅ ОБНОВЛЕНИЕ
  };

  return (
    <div className="admin">
      <h1>Админ-панель</h1>

      {bookings.map((b) => (
        <div key={b.id} className="admin__card">
          <strong>{b.service.name}</strong>
          <div>{new Date(b.start_time).toLocaleString()}</div>
          <div>
            {b.user.name} • {b.user.phone}
          </div>
          <div>Статус: {b.status}</div>

          <div className="admin__actions">
            <button
              disabled={b.status !== "active"}
              onClick={() => confirmBooking(b.id)}
            >
              Подтвердить
            </button>

            <button
              disabled={b.status === "canceled"}
              onClick={() => cancelBooking(b.id)}
            >
              Отменить
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
