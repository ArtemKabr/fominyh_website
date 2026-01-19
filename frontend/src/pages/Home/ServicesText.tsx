// frontend/src/pages/Home/ServicesText.tsx — текстовые описания услуг
// Назначение: вывод маркетинговых описаний услуг на главной

import { useEffect, useState } from "react";

type MarketingService = {
    slug: string;
    full_description: string;
};

export function ServicesText() {
    const [services, setServices] = useState<MarketingService[]>([]);

    useEffect(() => {
        fetch("/api/services/marketing")
            .then(res => res.json())
            .then(setServices);
    }, []);

    return (
        <section className="home__section">
            <div className="home__content">
                <h2 className="home__subtitle">Наши услуги</h2>

                {services.map(service => (
                    <p key={service.slug} className="home__text">
                        {service.full_description}
                    </p>
                ))}
            </div>
        </section>
    );
}
