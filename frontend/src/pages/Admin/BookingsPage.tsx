// frontend/src/pages/Admin/BookingsPage.tsx — новые записи
// Назначение: подтверждение/отмена pending-записей + просмотр комментария клиента

import { useEffect, useState } from "react";
import "./admin.css";

type Booking = {
    id: number;
    start_time: string;
    status: string;
    service: {
        id: number;
        name: string;
        price: number;
    };
    user: {
        id: number | null;
        name: string;
        phone: string;
        email: string | null;
    };
    comment: string | null; // (я добавил)
};

export function BookingsPage() {
    const userId = localStorage.getItem("user_id") || "";
    const [items, setItems] = useState<Booking[]>([]);

    const load = async () => {
        const res = await fetch("/api/admin/bookings", {
            headers: { "X-User-Id": userId },
        });

        if (!res.ok) return;

        const data: Booking[] = await res.json();
        setItems(data.filter((x) => x.status === "pending"));
    };

    const confirm = async (id: number) => {
        await fetch(`/api/admin/bookings/${id}/confirm`, {
            method: "POST",
            headers: { "X-User-Id": userId },
        });
        await load();
    };

    const cancel = async (id: number) => {
        await fetch(`/api/admin/bookings/${id}/cancel`, {
            method: "POST",
            headers: { "X-User-Id": userId },
        });
        await load();
    };

    useEffect(() => {
        load();
    }, []);

    return (
        <div className="admin">
            <h1 className="admin__h1">Новые записи</h1>

            {items.length === 0 && (
                <div className="admin__muted">
                    Новых записей нет
                </div>
            )}

            {items.map((b) => (
                <div
                    key={b.id}
                    className="admin-card admin-card--pending"
                >
                    <div className="admin-card__head">
                        <div className="admin-card__title">
                            {b.service.name}
                        </div>
                        <div className="badge badge--pending">
                            ожидает
                        </div>
                    </div>

                    <div className="admin-card__row">
                        {new Date(b.start_time).toLocaleString("ru-RU")}
                    </div>

                    <div className="admin-card__row">
                        {b.user?.name || "Гость"} •{" "}
                        {b.user?.phone || "—"} •{" "}
                        {b.user?.email || "—"}
                    </div>

                    {b.comment && (
                        <div className="admin-card__row admin-card__comment">
                            Комментарий клиента: {b.comment}
                        </div>
                    )} {/* (я добавил) */}

                    <div className="admin-card__actions">
                        <button
                            className="btn btn--primary"
                            onClick={() => confirm(b.id)}
                        >
                            Подтвердить
                        </button>

                        <button
                            className="btn btn--danger"
                            onClick={() => cancel(b.id)}
                        >
                            Отменить
                        </button>
                    </div>
                </div>
            ))}
        </div>
    );
}
