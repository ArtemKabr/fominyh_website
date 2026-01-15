// frontend/src/pages/ServiceDetail/ServiceDetail.tsx
// Назначение: детальная страница услуги + переход к записи

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import "./service-detail.css";

type Service = {
    id: number;
    name: string;
    slug: string;
    category: string;
    price: number;
    duration_minutes: number;
    image: string;
    description: string;
    benefits?: string[]; // (я исправил)
};

export function ServiceDetail() {
    const { slug } = useParams<{ slug: string }>();
    const navigate = useNavigate();

    const [service, setService] = useState<Service | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!slug) return;

        fetch(`/api/services/slug/${slug}`)
            .then((r) => {
                if (!r.ok) throw new Error("not found");
                return r.json();
            })
            .then(setService)
            .catch(() => setService(null))
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

                {Array.isArray(service.benefits) && service.benefits.length > 0 && (
                    <ul className="service-detail__benefits">
                        {service.benefits.map((b) => (
                            <li key={b}>{b}</li>
                        ))}
                    </ul>
                )}

                <div className="service-detail__meta">
                    <strong>{service.duration_minutes} мин</strong>
                    <strong>{service.price} ₽</strong>
                </div>

                <button
                    className="service-detail__btn"
                    onClick={() => navigate(`/booking/${service.slug}`)}
                >
                    Записаться
                </button>
            </div>
        </section>
    );
}
