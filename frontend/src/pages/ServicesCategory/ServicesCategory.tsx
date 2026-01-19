// frontend/src/pages/ServicesCategory/ServicesCategory.tsx — услуги по категории
import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { ServiceCard } from "../../components/services/ServiceCard";
import "./services-category.css";

type Service = {
  id: number;
  category: "face" | "body" | "complex";
  slug: string;
  name: string;
  shortDescription: string;
  duration: number;
  price: number;
  image?: string;
};

const CATEGORY_TITLES: Record<Service["category"], string> = {
  face: "Массаж лица",
  body: "Массаж тела",
  complex: "Комплексный массаж",
};

const VALID_CATEGORIES: Service["category"][] = [
  "face",
  "body",
  "complex",
];

export function ServicesCategory() {
  const { category } = useParams();

  if (!category || !VALID_CATEGORIES.includes(category as Service["category"])) {
    return (
      <section className="services-category">
        <h1 className="services-category__title">Услуги</h1>
        <div>Категория не найдена</div>
      </section>
    );
  }

  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch("/api/services")
      .then((r) => r.json())
      .then((data) => setServices(data))
      .finally(() => setLoading(false));
  }, []);

  const normalizedCategory = category as Service["category"];

  const filtered = useMemo(() => {
    return services.filter((s) => s.category === normalizedCategory);
  }, [services, normalizedCategory]);

  const title = CATEGORY_TITLES[normalizedCategory];

  return (
    <section className="services-category">
      <h1 className="services-category__title">{title}</h1>

      {loading && <div>Загрузка…</div>}

      {!loading && filtered.length === 0 && (
        <div>Услуги пока не добавлены</div>
      )}

      <div className="services-category__grid">
        {filtered.map((s) => (
          <ServiceCard
            key={s.id}
            id={s.id}
            category={s.category}
            slug={s.slug}
            name={s.name}
            shortDescription={s.shortDescription}
            duration_minutes={s.duration_minutes}
            price={s.price}
            image={s.image}
          />
        ))}
      </div>
    </section>
  );
}
