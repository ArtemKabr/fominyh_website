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
    comment: string | null;
};

type DaySlot = {
    time: string;
    status: "free" | "booked";
};

type Service = {
    id: number;
    name: string;
    duration_minutes: number;
};

function toYmd(d: Date) {
    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const dd = String(d.getDate()).padStart(2, "0");
    return `${y}-${m}-${dd}`;
}

const todayYmd = toYmd(new Date()); // (я добавил)


export function SlotsPage() {
    const userId = localStorage.getItem("user_id") || "";

    const [services, setServices] = useState<Service[]>([]);
    const [serviceId, setServiceId] = useState<number | null>(null);

    const [month, setMonth] = useState(() => {
        const d = new Date();
        return new Date(d.getFullYear(), d.getMonth(), 1);
    });

    const [busy, setBusy] = useState<Record<string, number>>({});
    const [selectedDay, setSelectedDay] = useState<string>("");

    const [dayBookings, setDayBookings] = useState<Booking[]>([]);
    const [daySlots, setDaySlots] = useState<DaySlot[]>([]);

    const [mode, setMode] = useState<"admin" | "client" | null>(null);
    const [selectedSlots, setSelectedSlots] = useState<string[]>([]);

    const [guestName, setGuestName] = useState("");
    const [guestPhone, setGuestPhone] = useState("");
    const [guestEmail, setGuestEmail] = useState("");
    const [comment, setComment] = useState("");

    // --- ДОБАВЛЕНО: перенос ---
    const [rescheduleId, setRescheduleId] = useState<number | null>(null); // (я добавил)
    const [rescheduleTime, setRescheduleTime] = useState<string>(""); // (я добавил)

    const monthDays = useMemo(() => {
        const y = month.getFullYear();
        const m = month.getMonth();
        const last = new Date(y, m + 1, 0).getDate();
        return Array.from({length: last}, (_, i) => new Date(y, m, i + 1));
    }, [month]);

    // -----------------------
    // ЗАГРУЗКА ДАННЫХ
    // -----------------------

    const loadServices = async () => {
        const res = await fetch("/api/services");
        if (!res.ok) return;

        const data = await res.json();
        const list = Array.isArray(data) ? data : [];
        setServices(list);

        if (list.length > 0 && serviceId === null) {
            setServiceId(list[0].id); // (я добавил)
        }
    };


    const cancelBooking = async (id: number) => {
        const res = await fetch(`/api/admin/bookings/${id}/cancel`, {
            method: "POST",
            headers: {"X-User-Id": userId},
        });

        if (!res.ok) {
            const data = await res.json().catch(() => ({}));
            alert((data as any)?.detail || "Ошибка удаления"); // (я добавил)
            return; // (я добавил)
        }

        if (selectedDay) {
            await loadDay(selectedDay);
        }
        await loadCalendar();
    };


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
        setSelectedDay(day); // (я добавил)
        setSelectedSlots([]); // (я добавил)
        setMode(null); // (я добавил)

        setGuestName("");
        setGuestPhone("");
        setGuestEmail("");
        setComment("");

        const resBookings = await fetch(
            `/api/admin/bookings/by-day?day=${day}`,
            {headers: {"X-User-Id": userId}}
        );

        const rawBookings = await resBookings.json();
        setDayBookings(
            rawBookings.filter((b: Booking) => b.status !== "canceled")
        );

        const effectiveServiceId = serviceId ?? services[0]?.id ?? null; // (я добавил)
        if (!effectiveServiceId) {
            setDaySlots([]); // (я добавил)
            return; // (я добавил)
        }

        const resSlots = await fetch(
            `/api/admin/slots?day=${day}&service_id=${effectiveServiceId}`,
            {headers: {"X-User-Id": userId}}
        );

        const slots = await resSlots.json();
        setDaySlots(Array.isArray(slots) ? slots : []);
    };


    // -----------------------
    // ДЕЙСТВИЯ
    // -----------------------

    const toggleSlot = (time: string) => {
        // режим переноса (я добавил)
        if (rescheduleId) {
            setRescheduleTime(time); // (я добавил)
            return;
        }

        if (!mode) return;

        if (mode === "client") {
            setSelectedSlots([time]);
            return;
        }

        setSelectedSlots((prev) =>
            prev.includes(time)
                ? prev.filter((t) => t !== time)
                : [...prev, time]
        );
    };

    const bookSelected = async () => {
        if (!serviceId || !selectedDay) return;

        if (mode === "client" && (!guestName.trim() || !guestPhone.trim())) {
            return;
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
                    guest_name: mode === "client" ? guestName.trim() : null,
                    guest_phone: mode === "client" ? guestPhone.trim() : null,
                    guest_email:
                        mode === "client" ? guestEmail.trim() || null : null,
                    comment: comment.trim() || null,
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

    // --- ДОБАВЛЕНО: перенос ---
    const rescheduleBooking = (id: number) => { // (я добавил)
        setRescheduleId(id);
        setRescheduleTime("");
        setMode("admin");
        setSelectedSlots([]);
    };

    const submitReschedule = async () => { // (я добавил)
        if (!rescheduleId || !rescheduleTime || !selectedDay) return;

        const qs = new URLSearchParams({
            new_day: selectedDay,
            new_time: rescheduleTime,
        }).toString();

        const res = await fetch(
            `/api/admin/bookings/${rescheduleId}/reschedule?${qs}`,
            {
                method: "POST",
                headers: {"X-User-Id": userId},
            }
        );

        if (!res.ok) {
            alert("Ошибка переноса записи");
            return;
        }

        setRescheduleId(null);
        setRescheduleTime("");

        await loadDay(selectedDay);
        await loadCalendar();
    };

    // -----------------------
    // EFFECTS
    // -----------------------

    useEffect(() => {
        loadServices();
    }, []);

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
                            disabled={day < todayYmd} // (я добавил)
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

            {selectedDay && (
                <div className="slots__details">
                    <div className="slots__details-title">
                        Интервалы: {selectedDay}
                    </div>

                    <div className="slots__times">
                        {daySlots.map((s) => (
                            <button
                                key={s.time}
                                disabled={
                                    s.status !== "free" ||
                                    (mode === "client" && !serviceId)
                                }
                                className={
                                    "btn slot-time " +
                                    (s.status === "booked" ? "slot-time--booked " : "") +
                                    (selectedSlots.includes(s.time)
                                        ? mode === "admin"
                                            ? "slot-time--admin"
                                            : "slot-time--client"
                                        : "") +
                                    (rescheduleTime === s.time
                                        ? " slot-time--admin"
                                        : "")
                                }
                                onClick={() => toggleSlot(s.time)}
                            >
                                {s.time}
                            </button>
                        ))}
                    </div>

                    {/* подтверждение переноса */}
                    {rescheduleId && rescheduleTime && (
                        <div className="slot-actions__confirm">
                            <div>Новое время: {rescheduleTime}</div>

                            <button
                                className="btn btn--primary"
                                onClick={submitReschedule}
                            >
                                Подтвердить перенос
                            </button>

                            <button
                                className="btn btn--ghost"
                                onClick={() => {
                                    setRescheduleId(null);
                                    setRescheduleTime("");
                                }}
                            >
                                Отменить
                            </button>
                        </div>
                    )}

                    <div className="slot-actions">
                        <div className="slot-actions__modes">
                            <button
                                className={`btn ${mode === "admin" ? "btn--active" : ""}`}
                                onClick={() => {
                                    setMode("admin");
                                    setSelectedSlots([]);
                                }}
                            >
                                Режим админа
                            </button>

                            <button
                                className={`btn ${mode === "client" ? "btn--active" : ""}`}
                                onClick={() => {
                                    setMode("client");
                                    setSelectedSlots([]);
                                }}
                            >
                                Режим клиента
                            </button>

                            {mode === "client" && (
                                <div className="slots__service-select">
                                    <label>Услуга</label>
                                    <select
                                        value={serviceId ?? ""}
                                        onChange={async (e) => {
                                            const id = Number(e.target.value);
                                            setServiceId(id);
                                            setSelectedSlots([]);
                                            if (selectedDay) {
                                                await loadDay(selectedDay);
                                            }
                                        }}
                                    >
                                        <option value="" disabled>
                                            Выберите услугу
                                        </option>
                                        {services.map((s) => (
                                            <option key={s.id} value={s.id}>
                                                {s.name} ({s.duration_minutes} мин)
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            )}
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

                        {selectedSlots.length > 0 && !rescheduleId && (
                            <div className="slot-actions__confirm">
                                <div>Время: {selectedSlots.join(", ")}</div>

                                <button
                                    className="btn btn--primary"
                                    onClick={bookSelected}
                                    disabled={
                                        mode === "client" &&
                                        (!serviceId ||
                                            !guestName.trim() ||
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
                                {new Date(b.start_time).toLocaleTimeString("ru-RU", {
                                    hour: "2-digit",
                                    minute: "2-digit",
                                })}
                            </div>

                            <div className="admin-card__row">
                                {b.user?.name || "Админ"} •{" "}
                                {b.user?.phone || "—"} •{" "}
                                {b.user?.email || "—"}
                            </div>

                            {b.comment && (
                                <div className="admin-card__row admin-card__comment">
                                    Комментарий: {b.comment}
                                </div>
                            )}

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
                                        onClick={() => rescheduleBooking(b.id)}
                                    >
                                        Перенести
                                    </button>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}