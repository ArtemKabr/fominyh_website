// frontend/src/pages/Admin/SlotsPage.tsx — слоты
// Назначение: календарь занятости по дням + интервалы + бронирование

import {useEffect, useMemo, useState} from "react";
import "./admin.css";

type CalendarDay = { date: string; count: number };

type Booking = {
    id: number;
    start_time: string;
    status: string;
    service: { id: number; name: string; price: number };
    user: {
        id: number | null;
        name: string;
        phone: string;
        email: string | null;
    };
};

type DaySlot = {
    time: string;
    status: "free" | "booked";
};

function toYmd(d: Date) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${dd}`;
}

export function SlotsPage() {
    const userId = localStorage.getItem("user_id") || "";
    const serviceId = 1; // фикс, как было

    const [month, setMonth] = useState(() => {
        const d = new Date();
        return new Date(d.getFullYear(), d.getMonth(), 1);
    });

    // модалка переноса (я добавил)
    const [rescheduleId, setRescheduleId] = useState<number | null>(null); // (я добавил)
    const [rescheduleDay, setRescheduleDay] = useState<string>(""); // (я добавил)
    const [rescheduleTime, setRescheduleTime] = useState<string>(""); // (я добавил)

    const [busy, setBusy] = useState<Record<string, number>>({});
    const [selectedDay, setSelectedDay] = useState<string>("");

    const [dayBookings, setDayBookings] = useState<Booking[]>([]);
    const [daySlots, setDaySlots] = useState<DaySlot[]>([]);

    const [mode, setMode] = useState<"admin" | "client" | null>(null); // (я добавил)
    const [selectedSlots, setSelectedSlots] = useState<string[]>([]); // (я добавил)

    // ---- форма для клиента (я добавил) ----
    const [guestName, setGuestName] = useState<string>(""); // (я добавил)
    const [guestPhone, setGuestPhone] = useState<string>(""); // (я добавил)
    const [guestEmail, setGuestEmail] = useState<string>(""); // (я добавил)
    const [comment, setComment] = useState<string>(""); // (я добавил)

    const monthDays = useMemo(() => {
        const y = month.getFullYear();
        const m = month.getMonth();
        const last = new Date(y, m + 1, 0).getDate();
        return Array.from({length: last}, (_, i) => new Date(y, m, i + 1));
    }, [month]);

    const loadCalendar = async () => {
        const from = toYmd(new Date(month.getFullYear(), month.getMonth(), 1));
        const to = toYmd(new Date(month.getFullYear(), month.getMonth() + 1, 0));

        const res = await fetch(
            `/api/admin/bookings/calendar?date_from=${from}&date_to=${to}`,
            {headers: {"X-User-Id": userId}}
        );

        const data: CalendarDay[] = await res.json();
        const map: Record<string, number> = {};
        data.forEach((x) => (map[x.date] = x.count));
        setBusy(map);
    };

    const loadDay = async (day: string) => {
        setSelectedDay(day);
        setSelectedSlots([]); // (я добавил)
        setMode(null); // (я добавил)

        setGuestName(""); // (я добавил)
        setGuestPhone(""); // (я добавил)
        setGuestEmail(""); // (я добавил)
        setComment(""); // (я добавил)

        const resBookings = await fetch(`/api/admin/bookings/by-day?day=${day}`, {
            headers: {"X-User-Id": userId},
        });
        const bookings: Booking[] = await resBookings.json();
        setDayBookings(bookings.filter((x) => x.status !== "canceled"));

        const resSlots = await fetch(
            `/api/admin/slots?day=${day}&service_id=${serviceId}`,
            {headers: {"X-User-Id": userId}}
        );
        setDaySlots(await resSlots.json());
    };

    const toggleSlot = (time: string) => {
        if (!mode) return;

        if (mode === "client") {
            setSelectedSlots([time]);
            return;
        }

        setSelectedSlots((prev) =>
            prev.includes(time) ? prev.filter((t) => t !== time) : [...prev, time]
        );
    };

    const cancelBooking = async (id: number) => {
        await fetch(`/api/admin/bookings/${id}/cancel`, {
            method: "POST",
            headers: {"X-User-Id": userId},
        });

        await loadDay(selectedDay); // (я добавил)
        await loadCalendar(); // (я добавил)
    };

    const rescheduleBooking = (id: number) => {
        setRescheduleId(id); // (я добавил)
        setRescheduleDay(selectedDay); // (я добавил)
        setRescheduleTime(""); // (я добавил)
    };

    // ---- подтвердить перенос (исправлено) ----
    const submitReschedule = async () => {
        if (!rescheduleId || !rescheduleDay || !rescheduleTime) return;

        const qs = new URLSearchParams({
            new_day: rescheduleDay,
            new_time: rescheduleTime,
        }).toString(); // (я добавил)

        const res = await fetch(
            `/api/admin/bookings/${rescheduleId}/reschedule?${qs}`,
            {
                method: "POST",
                headers: {"X-User-Id": userId},
            }
        );

        if (!res.ok) {
            const data = await res.json().catch(() => ({})); // (я добавил)
            alert((data as any)?.detail || "Ошибка переноса записи"); // (я добавил)
            return;
        }

        setRescheduleId(null); // (я добавил)
        setRescheduleTime(""); // (я добавил)

        await loadDay(rescheduleDay); // (я добавил)
        await loadCalendar(); // (я добавил)
    };

    const bookSelected = async () => {
        if (mode === "client") {
            if (!guestName.trim() || !guestPhone.trim()) return;
        }

        for (const time of selectedSlots) {
            const res = await fetch("/api/admin/slots/book", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-User-Id": userId,
                },
                body: JSON.stringify({
                    service_id: serviceId,
                    day: selectedDay,
                    time,
                    mode,
                    guest_name: mode === "client" ? guestName.trim() : null, // (я добавил)
                    guest_phone: mode === "client" ? guestPhone.trim() : null, // (я добавил)
                    guest_email:
                        mode === "client" ? guestEmail.trim() || null : null, // (я добавил)
                    comment: comment.trim() || null, // (я добавил)
                }),
            });

            if (!res.ok) return;
        }

        setSelectedSlots([]);
        setMode(null);
        setGuestName("");
        setGuestPhone("");
        setGuestEmail("");
        setComment("");

        await loadDay(selectedDay);
        await loadCalendar();
    };

    useEffect(() => {
        loadCalendar();
        setSelectedDay("");
        setDayBookings([]);
        setDaySlots([]);
        setSelectedSlots([]);
        setMode(null);
    }, [month]);

    return (
        <div className="admin">
            <h1 className="admin__h1">Слоты</h1>

            <div className="slots__toolbar">
                <button
                    className="btn btn--ghost"
                    onClick={() =>
                        setMonth(new Date(month.getFullYear(), month.getMonth() - 1, 1))
                    }
                >
                    ←
                </button>

                <div className="slots__month">
                    {month.toLocaleString("ru-RU", {
                        month: "long",
                        year: "numeric",
                    })}
                </div>

                <button
                    className="btn btn--ghost"
                    onClick={() =>
                        setMonth(new Date(month.getFullYear(), month.getMonth() + 1, 1))
                    }
                >
                    →
                </button>
            </div>

            <div className="slots__grid">
                {monthDays.map((d) => {
                    const day = toYmd(d);
                    const count = busy[day] || 0;

                    const cls =
                        "slot-day " +
                        (count > 0 ? "slot-day--busy " : "slot-day--free ") +
                        (selectedDay === day ? "slot-day--active" : "");

                    return (
                        <button
                            key={day}
                            className={cls}
                            onClick={() => loadDay(day)}
                        >
                            <div className="slot-day__num">{d.getDate()}</div>
                            {count > 0 && (
                                <div className="slot-day__count">{count}</div>
                            )}
                        </button>
                    );
                })}
            </div>

            {selectedDay ? (
                <div className="slots__details">
                    <div className="slots__details-title">
                        Интервалы: {selectedDay}
                    </div>

                    <div className="slots__times">
                        {daySlots.map((s) => (
                            <button
                                key={s.time}
                                disabled={s.status !== "free"}
                                className={
                                    "btn slot-time " +
                                    (selectedSlots.includes(s.time)
                                        ? mode === "admin"
                                            ? "slot-time--admin"
                                            : "slot-time--client"
                                        : "")
                                }
                                onClick={() => toggleSlot(s.time)}
                            >
                                {s.time}
                            </button>
                        ))}
                    </div>

                    <div className="slot-actions">
                        <div className="slot-actions__modes">
                            <button
                                className={`btn ${
                                    mode === "admin" ? "btn--active" : ""
                                }`}
                                onClick={() => {
                                    setMode("admin");
                                    setSelectedSlots([]);
                                }}
                            >
                                Режим админа
                            </button>

                            <button
                                className={`btn ${
                                    mode === "client" ? "btn--active" : ""
                                }`}
                                onClick={() => {
                                    setMode("client");
                                    setSelectedSlots([]);
                                }}
                            >
                                Режим клиента
                            </button>
                        </div>

                        {mode === "client" && selectedSlots.length > 0 && (
                            <div className="client-form">
                                <input
                                    className="client-form__input"
                                    value={guestName}
                                    onChange={(e) => setGuestName(e.target.value)}
                                    placeholder="ФИО"
                                />
                                <input
                                    className="client-form__input"
                                    value={guestPhone}
                                    onChange={(e) => setGuestPhone(e.target.value)}
                                    placeholder="Телефон"
                                />
                                <input
                                    className="client-form__input"
                                    value={guestEmail}
                                    onChange={(e) => setGuestEmail(e.target.value)}
                                    placeholder="Email (необязательно)"
                                />
                                <input
                                    className="client-form__input"
                                    value={comment}
                                    onChange={(e) => setComment(e.target.value)}
                                    placeholder="Комментарий / откуда заказ"
                                />
                            </div>
                        )}

                        {selectedSlots.length > 0 && (
                            <div className="slot-actions__confirm">
                                <div>Время: {selectedSlots.join(", ")}</div>

                                <button
                                    className="btn btn--primary"
                                    onClick={bookSelected}
                                    disabled={
                                        mode === "client" &&
                                        (!guestName.trim() ||
                                            !guestPhone.trim())
                                    }
                                >
                                    Забронировать
                                </button>

                                <button
                                    className="btn btn--ghost"
                                    onClick={() => {
                                        setSelectedSlots([]);
                                        setMode(null);
                                        setGuestName("");
                                        setGuestPhone("");
                                        setGuestEmail("");
                                        setComment("");
                                    }}
                                >
                                    Отменить
                                </button>
                            </div>
                        )}
                    </div>

                    {dayBookings.map((b) => (
                        <div key={b.id} className="admin-card">
                            <div className="admin-card__head">
                                <div className="admin-card__title">
                                    {b.service.name}
                                </div>
                                <div className="badge badge--ok">
                                    {b.status}
                                </div>
                            </div>

                            <div className="admin-card__row">
                                {new Date(b.start_time).toLocaleTimeString(
                                    "ru-RU",
                                    {
                                        hour: "2-digit",
                                        minute: "2-digit",
                                    }
                                )}
                            </div>

                            <div className="admin-card__row">
                                {b.user?.name || "Админ"} •{" "}
                                {b.user?.phone || "—"} •{" "}
                                {b.user?.email || "—"}
                            </div>

                            {b.status === "active" && (
                                <div className="admin-card__actions">
                                    <button
                                        className="btn btn--danger"
                                        onClick={() => cancelBooking(b.id)}
                                    >
                                        Удалить
                                    </button>

                                    <button
                                        className="btn btn--ghost"
                                        onClick={() =>
                                            rescheduleBooking(b.id)
                                        }
                                    >
                                        Перенести
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            ) : null}

            {rescheduleId ? (
                <div className="modal-backdrop">
                    <div className="modal">
                        <h3>Перенос записи</h3>

                        <label>Дата</label>
                        <input
                            type="date"
                            value={rescheduleDay}
                            onChange={(e) =>
                                setRescheduleDay(e.target.value)
                            }
                        />

                        <label>Время</label>
                        <input
                            type="time"
                            value={rescheduleTime}
                            onChange={(e) =>
                                setRescheduleTime(e.target.value)
                            }
                        />

                        <div className="modal__actions">
                            <button
                                className="btn btn--primary"
                                onClick={submitReschedule}
                            >
                                Сохранить
                            </button>

                            <button
                                className="btn btn--ghost"
                                onClick={() => {
                                    setRescheduleId(null);
                                    setRescheduleTime("");
                                }}
                            >
                                Отмена
                            </button>
                        </div>
                    </div>
                </div>
            ) : null}
        </div>
    );
}