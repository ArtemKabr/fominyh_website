// frontend/src/pages/Admin/UsersPage.tsx — клиенты
// Назначение: список пользователей (карты)

import { useEffect, useState } from "react";
import "./admin.css";

type User = { id: number; name: string; phone: string; email: string; is_admin: boolean };

export function UsersPage() {
  const userId = localStorage.getItem("user_id") || "";
  const [items, setItems] = useState<User[]>([]);

  useEffect(() => {
    fetch("/api/admin/users", { headers: { "X-User-Id": userId } })
      .then((r) => r.json())
      .then(setItems);
  }, []);

  return (
    <div className="admin">
      <h1 className="admin__h1">Клиенты</h1>

      <div className="users-grid">
        {items.map((u) => (
          <div key={u.id} className="admin-card">
            <div className="admin-card__head">
              <div className="admin-card__title">{u.name}</div>
              {u.is_admin && <div className="badge badge--ok">admin</div>}
            </div>
            <div className="admin-card__row">{u.phone}</div>
            <div className="admin-card__row">{u.email}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
