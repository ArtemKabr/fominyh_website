// frontend/src/components/services/ServiceCard.tsx — карточка услуги
// Назначение: отображение услуги в списке

import { useNavigate } from "react-router-dom";
import "./service-card.css";

type Props = {
  id: number;
  category: string;
  slug: string;
  name: string;
  shortDescription: string;
  duration_minutes: number | null; // (я добавил)
  price: number;
  image?: string;
};

export function ServiceCard({
  category,
  slug,
  name,
  shortDescription,
  duration_minutes,
  price,
  image,
}: Props) {
  const navigate = useNavigate();

  const goToDetail = () => {
    navigate(`/services/${category}/${slug}`);
  };

  return (
    <div
      className="service-card"
      onClick={goToDetail}
      style={{
        backgroundImage: image ? `url(${image})` : undefined,
      }}
    >
      <div className="service-card__overlay">
        <h3 className="service-card__title">{name}</h3>

        {shortDescription && (
          <p className="service-card__desc">{shortDescription}</p>
        )}

        <div className="service-card__meta">
          <span>
            {duration_minutes !== null
              ? `${duration_minutes} мин`
              : "—"}
          </span>
          <span>{price} ₽</span>
        </div>

        <button
          className="service-card__btn"
          onClick={(e) => {
            e.stopPropagation();
            goToDetail();
          }}
        >
          Подробнее
        </button>
      </div>
    </div>
  );
}
