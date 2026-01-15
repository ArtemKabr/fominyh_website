// frontend/src/pages/Admin/StatsPage.tsx — статистика
// Назначение: базовая статистика салона

import { useEffect, useState } from "react";
import "./admin.css";

type Stats = { total: number; active: number; canceled: number };

export function StatsPage() {
  const userId = localStorage.getItem("user_id") || "";
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    fetch("/api/admin/stats", { headers: { "X-User-Id": userId } })
      .then((r) => r.json())
      .then(setStats);
  }, []);

  if (!stats) return <div className="admin">Загрузка...</div>;

  return (
    <div className="admin">
      <h1 className="admin__h1">Статистика</h1>

      <div className="stats">
        <div className="stat">
          <div className="stat__label">Всего записей</div>
          <div className="stat__value">{stats.total}</div>
        </div>
        <div className="stat">
          <div className="stat__label">Активных</div>
          <div className="stat__value">{stats.active}</div>
        </div>
        <div className="stat">
          <div className="stat__label">Отменено</div>
          <div className="stat__value">{stats.canceled}</div>
        </div>
      </div>
    </div>
  );
}
