import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./services.css";

type ServiceCategory = {
  slug: string;
  title: string;
  description: string;
  image: string;
};

export function Services() {
  const navigate = useNavigate();
  const [categories, setCategories] = useState<ServiceCategory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/data/service_categories.json")
      .then((res) => res.json())
      .then((data: ServiceCategory[]) => setCategories(data))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="services">Загрузка…</div>;
  }

  return (
    <section className="services">
      <h1 className="services__title">Выберите направление</h1>

      <div className="services__grid">
        {categories.map((c) => (
          <div
            key={c.slug}
            className="services__card"
            style={{ backgroundImage: `url(${c.image})` }} // 
            onClick={() => navigate(`/services/${c.slug}`)}
          >
            <div className="services__card-content"> {/* я добавил */}
              <h3 className="services__card-title">{c.title}</h3>

              <p className="services__card-desc">{c.description}</p>

              <button
                className="services__card-btn"
                onClick={(e) => {
                  e.stopPropagation(); // 
                  navigate(`/services/${c.slug}`);
                }}
              >
                Подробнее
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
