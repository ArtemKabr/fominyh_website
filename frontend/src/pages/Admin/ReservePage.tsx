// frontend/src/pages/Admin/ReservePage.tsx — резерв
// Назначение: список заявок в резерв (админ)

import { useEffect, useState } from "react";
import "./admin.css";

type Reserve = {
  id: number;
  service_id: number;
  day: string;
  name: string;
  phone: string;
  email: string | null;
  comment: string | null;
  created_at: string;
};

export function ReservePage() {
  const userId = localStorage.getItem("user_id") || "";
  const [items, setItems] = useState<Reserve[]>([]);

  const load = async () => {
    const res = await fetch("/api/admin/reserve", {
      headers: { "X-User-Id": userId },
    });
    setItems(await res.json());
  };

  const remove = async (id: number) => {
    if (!confirm("Удалить резерв?")) return;

    await fetch(`/api/admin/reserve/${id}`, {
      method: "DELETE",
      headers: { "X-User-Id": userId },
    });

    load();
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="admin">
      <h1 className="admin__h1">Резерв</h1>

      {items.map((r) => (
        <div key={r.id} className="admin-card">
          <div className="admin-card__head">
            <div className="admin-card__title">{r.name}</div>
          </div>

          <div className="admin-card__row">
            {r.day} • {r.phone}
          </div>

          {r.email && (
            <div className="admin-card__row">{r.email}</div>
          )}

          {r.comment && (
            <div className="admin-card__row">{r.comment}</div>
          )}

          <button
            className="btn btn--danger"
            onClick={() => remove(r.id)}
          >
            Удалить
          </button>
        </div>
      ))}
    </div>
  );
}
