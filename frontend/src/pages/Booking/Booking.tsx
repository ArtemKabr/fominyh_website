// frontend/src/pages/Booking/Booking.tsx
// Назначение: запись на услугу (дата → время → данные → отправка)

import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./booking.css";

type Service = {
    id: number;
    name: string;
    price: number;
    duration_minutes: number;
};

type Slot = {
    iso: string;
    time: string;
};

function extractTime(raw: string): string {
    if (raw.includes("T")) return raw.split("T")[1]?.slice(0, 5) ?? "";
    if (raw.includes(" ")) return raw.split(" ")[1]?.slice(0, 5) ?? "";
    return raw.slice(0, 5);
}

export function Booking() {
    const { slug } = useParams<{ slug: string }>();

    const [service, setService] = useState<Service | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [date, setDate] = useState("");
    const [slots, setSlots] = useState<Slot[]>([]);
    const [selectedSlot, setSelectedSlot] = useState("");

    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");

    // ---- резерв (я добавил)
    const [reserveEmail, setReserveEmail] = useState(""); // (я добавил)
    const [reserveComment, setReserveComment] = useState(""); // (я добавил)
    const [reserveSent, setReserveSent] = useState(false); // (я добавил)

    const [submitting, setSubmitting] = useState(false);
    const [success, setSuccess] = useState(false);

    /* ===== загрузка услуги ===== */
    useEffect(() => {
        if (!slug) return;

        fetch(`/api/services/slug/${slug}`)
            .then((r) => {
                if (!r.ok) throw new Error();
                return r.json();
            })
            .then(setService)
            .catch(() => setError("Услуга не найдена"))
            .finally(() => setLoading(false));
    }, [slug]);

    /* ===== загрузка слотов ===== */
    useEffect(() => {
        if (!date || !service) return;

        fetch(`/api/booking/free?day=${date}&service_id=${service.id}`)
            .then((r) => r.json())
            .then((data) => {
                const normalized: Slot[] = (data.slots ?? []).map((raw: string) => ({
                    iso: raw,
                    time: extractTime(raw),
                }));
                setSlots(normalized);
                setSelectedSlot("");
                setReserveSent(false); // (я добавил)
            })
            .catch(() => setSlots([]));
    }, [date, service]);

    /* ===== обычная запись ===== */
    const submitBooking = async () => {
        if (!selectedSlot || !name || !phone || !service || !date) return;

        setSubmitting(true);
        try {
            await fetch("/api/booking", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    service_id: service.id,
                    day: date,
                    time: selectedSlot,
                    user_name: name,
                    phone,
                    email: null,
                }),
            });
            setSuccess(true);
        } finally {
            setSubmitting(false);
        }
    };

    /* ===== резерв ===== */
    const submitReserve = async () => {
        if (!name || !phone || !service || !date) return;

        await fetch("/api/booking/reserve", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                service_id: service.id,
                day: date,
                name,
                phone,
                email: reserveEmail || null,
                comment: reserveComment || null,
            }),
        });

        setReserveSent(true);
    };

    if (loading) return <div className="booking">Загрузка…</div>;
    if (error || !service) return <div className="booking">{error}</div>;

    if (success) {
        return (
            <div className="booking">
                <h2>Запись успешно создана</h2>
                <p>Мы свяжемся с вами для подтверждения.</p>
            </div>
        );
    }

    return (
        <div className="booking">
            <h1 className="booking__title">Запись на услугу</h1>

            <div className="booking__service">
                <h2>{service.name}</h2>
                <p>{service.duration_minutes} мин · {service.price} ₽</p>
            </div>

            <div className="booking__block">
                <label>Дата</label>
                <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            </div>

            {slots.length > 0 && (
                <div className="booking__block">
                    <label>Время</label>
                    <div className="booking__slots">
                        {slots.map((slot) => (
                            <button
                                key={slot.iso}
                                className={
                                    slot.time === selectedSlot
                                        ? "booking__slot booking__slot--active"
                                        : "booking__slot"
                                }
                                onClick={() => setSelectedSlot(slot.time)}
                            >
                                {slot.time}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {slots.length === 0 && date && !reserveSent && (
                <div className="booking__block">
                    <p>
                        Все временные интервалы на этот день заняты.
                        Вы можете записаться в резерв или выбрать другую дату.
                    </p>

                    <label>ФИО</label>
                    <input value={name} onChange={(e) => setName(e.target.value)} />

                    <label>Телефон</label>
                    <input value={phone} onChange={(e) => setPhone(e.target.value)} />

                    <label>Почта</label>
                    <input value={reserveEmail} onChange={(e) => setReserveEmail(e.target.value)} />

                    <label>Комментарий</label>
                    <input
                        value={reserveComment}
                        onChange={(e) => setReserveComment(e.target.value)}
                    />

                    <button className="booking__submit" onClick={submitReserve}>
                        Записаться в резерв
                    </button>
                </div>
            )}

            {selectedSlot && (
                <div className="booking__block">
                    <label>Ваше имя</label>
                    <input value={name} onChange={(e) => setName(e.target.value)} />

                    <label>Телефон</label>
                    <input value={phone} onChange={(e) => setPhone(e.target.value)} />

                    <button
                        className="booking__submit"
                        disabled={submitting}
                        onClick={submitBooking}
                    >
                        {submitting ? "Отправка..." : "Записаться"}
                    </button>
                </div>
            )}

            {reserveSent && (
                <p>Вы добавлены в резерв. Мы свяжемся с вами.</p>
            )}
        </div>
    );
}
