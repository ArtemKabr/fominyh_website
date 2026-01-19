// frontend/src/pages/Home/Home.tsx — главная страница (премиум, информативная)
// Назначение: главная страница + премиум-слайдер отзывов (2 карточки, плавно)

import {useState, useEffect} from "react";
import {useNavigate} from "react-router-dom";
import {ServicesText} from "./ServicesText";
import "./home.css";

export function Home() {
    const navigate = useNavigate();

    /* ============================================================
       СЕРТИФИКАТЫ — модальное окно
       ============================================================ */
    const [activeCert, setActiveCert] = useState<string | null>(null);

    useEffect(() => {
        if (!activeCert) return;

        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === "Escape") {
                setActiveCert(null);
            }
        };

        window.addEventListener("keydown", handleKeyDown);
        return () => window.removeEventListener("keydown", handleKeyDown);
    }, [activeCert]);

    /* ============================================================
       ОТЗЫВЫ — данные и логика слайдера
       ============================================================ */
    const reviews = [
        {
            name: "Анна К.",
            service: "Биоэнергетический массаж",
            text: "Глубокое расслабление, ушло напряжение в спине уже после первого сеанса.",
        },
        {
            name: "Марина Л.",
            service: "Скульптурирующий массаж лица",
            text: "Лицо стало более подтянутым, очень мягкая и аккуратная работа.",
        },
        {
            name: "Ольга S.",
            service: "Массаж Гуаша",
            text: "Приятная процедура, уменьшились отёки, кожа заметно посвежела.",
        },
        {
            name: "Екатерина М.",
            service: "Лимфодренажный массаж",
            text: "Появилось ощущение лёгкости в теле, очень комфортный сеанс.",
        },
        {
            name: "Наталья D.",
            service: "Ультразвуковая чистка",
            text: "Кожа стала гладкой и чистой, без раздражения.",
        },
        {
            name: "Ирина В.",
            service: "Биоэнергетический массаж",
            text: "Спокойная атмосфера, чувствуется профессиональный подход.",
        },
        {
            name: "Юлия Р.",
            service: "Скульптинг лица",
            text: "Эффект лифтинга заметен сразу, результат очень понравился.",
        },
        {
            name: "Татьяна Н.",
            service: "Массаж тела",
            text: "Сняло зажимы в шее и плечах, чувствую себя отдохнувшей.",
        },
        {
            name: "Алина G.",
            service: "Гуаша + лимфодренаж",
            text: "Лицо стало более свежим, ушла утренняя отёчность.",
        },
        {
            name: "Виктория П.",
            service: "Биоэнергетический массаж",
            text: "Очень бережная и глубокая работа, ощущение баланса.",
        },
        {
            name: "Светлана К.",
            service: "Скульптурирующий массаж",
            text: "Понравилось, что всё подбирается индивидуально.",
        },
        {
            name: "Елена Z.",
            service: "Массаж лица",
            text: "Кожа стала более упругой, приятное ощущение после процедуры.",
        },
        {
            name: "Дарья О.",
            service: "УЗ чистка + уход",
            text: "Чисто, аккуратно, без покраснений.",
        },
        {
            name: "Полина Т.",
            service: "Лимфодренаж",
            text: "Очень комфортно, исчезло чувство тяжести.",
        },
        {
            name: "Мария S.",
            service: "Массаж тела",
            text: "Процедура прошла спокойно, тело полностью расслабилось.",
        },
        {
            name: "Анастасия К.",
            service: "Скульптинг лица",
            text: "Чётче стал овал лица, результат заметен.",
        },
        {
            name: "Ксения Л.",
            service: "Гуаша",
            text: "Очень приятная техника, кожа стала сияющей.",
        },
        {
            name: "Валерия М.",
            service: "Биоэнергетический массаж",
            text: "После сеанса появилось ощущение лёгкости.",
        },
        {
            name: "Инна Р.",
            service: "Массаж лица и тела",
            text: "Комплексный подход, всё продумано.",
        },
        {
            name: "Юлия Н.",
            service: "Уход за кожей лица",
            text: "Кожа напитанная, ухоженная, эффект сохраняется.",
        },
    ];

    const REVIEWS_PER_PAGE = 2; // 

    const [reviewIndex, setReviewIndex] = useState(0);
    const [direction, setDirection] = useState<"next" | "prev">("next"); // 

    const visibleReviews = reviews.slice(
        reviewIndex,
        reviewIndex + REVIEWS_PER_PAGE
    );

    const nextReviews = () => {
        if (reviewIndex + REVIEWS_PER_PAGE < reviews.length) {
            setDirection("next"); // 
            setReviewIndex(reviewIndex + 1);
        }
    };

    const prevReviews = () => {
        if (reviewIndex > 0) {
            setDirection("prev"); // 
            setReviewIndex(reviewIndex - 1);
        }
    };

    /* ============================================================
       RENDER
       ============================================================ */
    return (
        <div className="home">
            {/* HERO */}
            <section className="home__hero">
                <div className="home__content">
                    <h1 className="home__title">Эстетический массаж и уход за телом</h1>

                    <p className="home__lead">
                        Пространство заботы, восстановления и глубокого расслабления,
                        где внимание к телу становится искусством.
                    </p>

                    <p className="home__text">
                        В салоне эстетики Екатерины Фоминых мы создаём атмосферу,
                        в которой красота, здоровье и внутреннее равновесие
                        соединяются в одном ощущении.
                    </p>

                    <p className="home__text">
                        Мы работаем с телом мягко и осознанно, помогая снять
                        накопленное напряжение и восстановить энергию.
                    </p>

                    <button className="home__cta" onClick={() => navigate("/services")}>
                        Ознакомиться с услугами
                    </button>
                </div>
            </section>

            {/* ВИДЕО */}
            <section className="home__video-section">
                <div className="home__video">
                    <video src="/video/ek.MP4" autoPlay muted loop playsInline/>
                </div>
            </section>

            {/* ТЕКСТ УСЛУГ */}
            <ServicesText/> {/* (я добавил) */}

            {/* ОТЗЫВЫ */}
            <section className="home__section">
                <div className="home__content">
                    <h2 className="home__subtitle">Отзывы клиентов</h2>

                    <div className="home__reviews-wrapper">
                        <button
                            className="home__reviews-arrow"
                            onClick={prevReviews}
                            disabled={reviewIndex === 0}
                        >
                            ‹
                        </button>

                        <div className="home__reviews" data-direction={direction}>
                            {visibleReviews.map((r, i) => (
                                <div key={i} className="home__review">
                                    <p className="home__review-text">“{r.text}”</p>
                                    <div className="home__review-meta">
                                        <span className="home__review-name">{r.name}</span>
                                        <span className="home__review-service">{r.service}</span>
                                    </div>
                                </div>
                            ))}
                        </div>

                        <button
                            className="home__reviews-arrow"
                            onClick={nextReviews}
                            disabled={reviewIndex + REVIEWS_PER_PAGE >= reviews.length}
                        >
                            ›
                        </button>
                    </div>
                </div>
            </section>

            {/* СЕРТИФИКАТЫ */}
            <section className="home__section">
                <div className="home__content">
                    <h2 className="home__subtitle">Наши дипломы и сертификаты</h2>

                    <div className="home__certificates">
                        {[
                            "/images/certificates/cert-1.jpg",
                            "/images/certificates/cert-2.jpg",
                            "/images/certificates/cert-3.jpg",
                        ].map((src) => (
                            <img
                                key={src}
                                src={src}
                                alt="Сертификат"
                                onClick={() => setActiveCert(src)}
                            />
                        ))}
                    </div>
                </div>
            </section>

            {/* МОДАЛКА СЕРТИФИКАТА */}
            {activeCert && (
                <div className="home__cert-modal" onClick={() => setActiveCert(null)}>
                    <img src={activeCert} alt="Сертификат увеличенный"/>
                </div>
            )}

            {/* КОНТАКТЫ */}
            <section className="home__section">
                <div className="home__content">
                    <h2 className="home__subtitle">Контакты</h2>

                    <div className="home__contacts">
                        {/* КАРТА */}
                        <div className="home__map">
                            <iframe
                                src="https://yandex.ru/map-widget/v1/?ll=49.671430%2C58.603437&z=16&l=map&pt=49.671430%2C58.603437%2Cpm2rdm"
                                loading="lazy"
                                referrerPolicy="no-referrer-when-downgrade"
                                title="Салон эстетики Екатерины Фоминых"
                            />
                        </div>

                        <p>г. Киров, ул. Конева, д. 7/7</p>
                        <p>
                            Телефон: <a href="tel:+79128287561">+7&nbsp;912&nbsp;828-75-61</a>
                        </p>
                        <p>
                            Email:{" "}
                            <a href="mailto:Fominykh-1970@inbox.ru">
                                Fominykh-1970@inbox.ru
                            </a>
                        </p>
                    </div>
                </div>
            </section>

            {/* ЗАПИСЬ */}
            <section className="home__section home__section--cta">
                <div className="home__content">
                    <h2 className="home__subtitle">Запись на сеанс</h2>

                    <p className="home__text">
                        Вы можете записаться на удобное время онлайн или связаться
                        с нами для консультации и подбора процедуры.
                    </p>

                    <p className="home__text home__telegram-info">
                        После записи вы можете получать уведомления в Telegram.<br/>
                        <span className="home__telegram-link">
                <img
                    src="/icons/telegram.svg"
                    alt="Telegram"
                    className="home__telegram-icon"
                />
                <a
                    href="https://t.me/EF_Beauty_bot"
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}  // (я добавил)
                >
    @EF_Beauty_bot
</a>

            </span>
                    </p>  {/* (я добавил) */}

                    <button
                        className="home__cta home__cta--big"
                        onClick={() => navigate("/services")}
                    >
                        Записаться
                    </button>
                </div>
            </section>

        </div>
    );
}
