// frontend/src/pages/Admin/AdminLayout.tsx — layout админ-панели
// Назначение: меню разделов админки и контейнер

import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import "./admin.css";

export function AdminLayout() {
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id");

  useEffect(() => {
    if (!userId) navigate("/login");
  }, [userId, navigate]);

  return (
    <div className="admin-layout">
      <aside className="admin-layout__menu">
        <div className="admin-layout__title">Админ</div>

        <NavLink to="/admin/bookings" className="admin-layout__link">
          Записи (новые)
        </NavLink>

        <NavLink to="/admin/history" className="admin-layout__link">
          История
        </NavLink>

        <NavLink to="/admin/slots" className="admin-layout__link">
          Слоты
        </NavLink>

        <NavLink to="/admin/reserve" className="admin-layout__link">
          Резерв
        </NavLink>

        <NavLink to="/admin/services" className="admin-layout__link">
          Услуги
        </NavLink>

        <NavLink to="/admin/users" className="admin-layout__link">
          Клиенты
        </NavLink>

        <NavLink to="/admin/stats" className="admin-layout__link">
          Статистика
        </NavLink>
      </aside>

      <main className="admin-layout__content">
        <Outlet />
      </main>
    </div>
  );
}
