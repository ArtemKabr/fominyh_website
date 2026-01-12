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

export function Booking() {
  const { serviceId } = useParams<{ serviceId: string }>();

  const [service, setService] = useState<Service | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [date, setDate] = useState("");
  const [slots, setSlots] = useState<string[]>([]);
  const [selectedSlot, setSelectedSlot] = useState("");

  const [name, setName] = useState(""); // (я добавил)
  const [phone, setPhone] = useState(""); // (я добавил)
  const [submitting, setSubmitting] = useState(false); // (я добавил)
  const [success, setSuccess] = useState(false); // (я добавил)

  /* ============================================================
     Загрузка услуги
     ============================================================ */
  useEffect(() => {
    if (!serviceId) return;

    fetch(`/api/services/${serviceId}`)
      .then((r) => {
        if (!r.ok) throw new Error();
        return r.json();
      })
      .then(setService)
      .catch(() => setError("Услуга не найдена"))
      .finally(() => setLoading(false));
  }, [serviceId]);

  /* ============================================================
     Загрузка слотов
     ============================================================ */
  useEffect(() => {
    if (!date || !serviceId) return;

    fetch(`/api/booking/free?day=${date}&service_id=${serviceId}`)
      .then((r) => r.json())
      .then((data) => {
        setSlots(data.slots ?? []);
        setSelectedSlot("");
      });
  }, [date, serviceId]);

  /* ============================================================
     Отправка записи
     ============================================================ */
  const submitBooking = async () => {
    if (!selectedSlot || !name || !phone) return;

    setSubmitting(true);

    await fetch("/api/booking", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        service_id: Number(serviceId),
        start_at: selectedSlot,
        client_name: name,
        client_phone: phone,
      }),
    });

    setSubmitting(false);
    setSuccess(true);
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
        <p>
          {service.duration_minutes} мин · {service.price} ₽
        </p>
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
                key={slot}
                className={
                  slot === selectedSlot
                    ? "booking__slot booking__slot--active"
                    : "booking__slot"
                }
                onClick={() => setSelectedSlot(slot)}
              >
                {new Date(slot).toLocaleTimeString("ru-RU", {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </button>
            ))}
          </div>
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
    </div>
  );
}
