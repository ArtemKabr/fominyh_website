// frontend/src/pages/ServiceDetail/ServiceDetail.tsx
// Назначение: детальная страница услуги + переход к записи

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getServices, Service } from "../../api/services.api";
import "./service-detail.css";

export function ServiceDetail() {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();

  const [service, setService] = useState<Service | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!slug) return;

    getServices()
      .then((services) => {
        const found = services.find((s) => s.slug === slug);
        setService(found ?? null);
      })
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return <div className="service-detail">Загрузка…</div>;
  }

  if (!service) {
    return <div className="service-detail">Услуга не найдена</div>;
  }

  return (
    <section
      className="service-detail"
      style={{ backgroundImage: `url(${service.image})` }}
    >
      <div className="service-detail__overlay">
        <h1 className="service-detail__title">{service.name}</h1>

        <p className="service-detail__description">
          {service.description}
        </p>

        <ul className="service-detail__benefits">
          {service.benefits.map((b) => (
            <li key={b}>{b}</li>
          ))}
        </ul>

        <div className="service-detail__meta">
          <strong>{service.duration} мин</strong>
          <strong>{service.price} ₽</strong>
        </div>

        <button
          className="service-detail__btn"
          onClick={() => navigate(`/booking/${service.id}`)} // 
        >
          Записаться
        </button>
      </div>
    </section>
  );
}
