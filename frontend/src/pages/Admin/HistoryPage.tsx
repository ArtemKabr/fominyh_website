// frontend/src/pages/Admin/HistoryPage.tsx — история записей
// Назначение: просмотр обработанных записей без действий

import {useEffect, useState} from "react";
import "./admin.css";

type Booking = {
    id: number;
    start_time: string;
    status: string;
    service: { id: number; name: string; price: number };
    user: { id: number; name: string; phone: string; email: string };
};

export function HistoryPage() {
    const userId = localStorage.getItem("user_id") || "";
    const [items, setItems] = useState<Booking[]>([]);

    const load = async () => {
        const res = await fetch("/api/admin/bookings", {
            headers: {"X-User-Id": userId},
        });
        const data: Booking[] = await res.json();
        setItems(data.filter((x) => x.status !== "pending"));
    };

    const badgeClass = (s: string) => {
        if (s === "active") return "badge--ok";
        if (s === "canceled") return "badge--bad";
        if (s === "completed") return "badge--done";
        return "badge--pending";
    };

    const badgeText = (s: string) => {
        if (s === "active") return "подтверждено";
        if (s === "canceled") return "отменено";
        if (s === "completed") return "завершено";
        return s;
    };

    const clearHistory = async () => {
        if (!confirm("Очистить всю историю записей?")) return; // (я добавил)

        const res = await fetch("/api/admin/bookings/history/clear", {
            method: "POST",
            headers: {
                "X-User-Id": userId,
            },
        }); // (я добавил)

        if (!res.ok) {
            alert("Ошибка очистки истории"); // (я добавил)
            return;
        }

        load(); // (я исправил)
    };


    useEffect(() => {
        load();
    }, []);

    return (
        <div className="admin">
            <h1 className="admin__h1">История</h1>
            <button
                className="btn btn--danger"
                onClick={clearHistory}
            >
                Очистить историю
            </button>

            {items.map((b) => (
                <div key={b.id} className="admin-card">
                    <div className="admin-card__head">
                        <div className="admin-card__title">{b.service.name}</div>
                        <div className={`badge ${badgeClass(b.status)}`}>{badgeText(b.status)}</div>
                    </div>

                    <div className="admin-card__row">{new Date(b.start_time).toLocaleString()}</div>
                    <div className="admin-card__row">
                        {b.user.name} • {b.user.phone} • {b.user.email}
                    </div>
                </div>
            ))}
        </div>
    );
}
