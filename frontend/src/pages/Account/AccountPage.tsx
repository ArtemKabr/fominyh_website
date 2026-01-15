// frontend/src/pages/Account/AccountPage.tsx — личный кабинет пользователя
// Назначение: ЛК v2 (аватар + редактирование профиля, без JWT)

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./account.css";

type Profile = {
    name: string;
    phone: string;
    email: string;
    avatar_url?: string;
};

type Dashboard = {
    profile: Profile;
    stats: {
        total: number;
        active: number;
        canceled: number;
    };
    card: {
        number: string;
        discount_percent: number;
        bonus_balance: number;
    };
};

type Booking = {
    id: number;
    service_name: string;
    price: number;
    duration_minutes: number;
    start_at: string;
    status: string;
};

export function AccountPage() {
    const navigate = useNavigate();
    const userId = localStorage.getItem("user_id");

    const [dashboard, setDashboard] = useState<Dashboard | null>(null);
    const [bookings, setBookings] = useState<Booking[]>([]);
    const [edit, setEdit] = useState(false);
    const [form, setForm] = useState<Profile | null>(null);

    useEffect(() => {
        if (!userId) {
            navigate("/login");
            return;
        }

        fetch("/api/user/dashboard", {
            headers: { "X-User-Id": userId },
        })
            .then((r) => r.json())
            .then((data) => {
                setDashboard(data);
                setForm(data.profile);
            })
            .catch(() => {
                localStorage.removeItem("user_id");
                navigate("/login");
            });

        fetch("/api/user/bookings", {
            headers: { "X-User-Id": userId },
        })
            .then((r) => r.json())
            .then(setBookings);
    }, [userId, navigate]);

    const logout = () => {
        localStorage.removeItem("user_id");
        navigate("/");
    };

    if (!dashboard || !form) {
        return <div className="account">Загрузка...</div>;
    }

    return (
        <div className="account">
            <div className="account__header">
                <h1>Личный кабинет</h1>
                <button onClick={logout}>Выйти</button>
            </div>

            {/* ПРОФИЛЬ */}
            <section className="account__card">
                <div className="account__card-header">
                    <h2>Профиль</h2>

                    {!edit ? (
                        <button onClick={() => setEdit(true)}>
                            Редактировать
                        </button>
                    ) : (
                        <div className="account__actions">
                            <button
                                onClick={async () => {
                                    await fetch("/api/user/profile", {
                                        method: "PUT",
                                        headers: {
                                            "Content-Type": "application/json",
                                            "X-User-Id": userId!,
                                        },
                                        body: JSON.stringify(form),
                                    });

                                    setDashboard({
                                        ...dashboard,
                                        profile: form,
                                    });
                                    setEdit(false);
                                }}
                            >
                                Сохранить
                            </button>
                            <button onClick={() => setEdit(false)}>
                                Отмена
                            </button>
                        </div>
                    )}
                </div>

                <div className="account__profile">
                    <label className="account__avatar">
                        <img
                            src={form.avatar_url || "/avatar-placeholder.png"}
                            alt="Аватар"
                        />
                        <input
                            type="file"
                            accept="image/*"
                            hidden
                            onChange={async (e) => {
                                if (!e.target.files?.[0]) return;

                                const fd = new FormData();
                                fd.append("file", e.target.files[0]);

                                const res = await fetch("/api/user/avatar", {
                                    method: "POST",
                                    headers: { "X-User-Id": userId! },
                                    body: fd,
                                });

                                const data = await res.json();
                                setForm({ ...form, avatar_url: data.avatar_url });
                                setDashboard({
                                    ...dashboard,
                                    profile: {
                                        ...dashboard.profile,
                                        avatar_url: data.avatar_url,
                                    },
                                });
                            }}
                        />
                        <span>Изменить</span>
                    </label>

                    <div className="account__fields">
                        {edit ? (
                            <>
                                <input
                                    value={form.name}
                                    onChange={(e) =>
                                        setForm({
                                            ...form,
                                            name: e.target.value,
                                        })
                                    }
                                />
                                <input
                                    value={form.phone}
                                    onChange={(e) =>
                                        setForm({
                                            ...form,
                                            phone: e.target.value,
                                        })
                                    }
                                />
                                <input
                                    value={form.email}
                                    onChange={(e) =>
                                        setForm({
                                            ...form,
                                            email: e.target.value,
                                        })
                                    }
                                />
                            </>
                        ) : (
                            <>
                                <p><strong>{dashboard.profile.name}</strong></p>
                                <p>{dashboard.profile.phone}</p>
                                <p>{dashboard.profile.email}</p>
                            </>
                        )}
                    </div>
                </div>
            </section>

            {/* КАРТА */}
            <section className="account__card">
                <h2>Карта клиента</h2>
                <p>Номер: {dashboard.card.number}</p>
                <p>Скидка: {dashboard.card.discount_percent}%</p>
                <p>Бонусы: {dashboard.card.bonus_balance}</p>
            </section>

            {/* СТАТИСТИКА */}
            <section className="account__card">
                <h2>Статистика</h2>
                <p>Всего записей: {dashboard.stats.total}</p>
                <p>Активные: {dashboard.stats.active}</p>
                <p>Отменённые: {dashboard.stats.canceled}</p>
            </section>

            {/* ЗАПИСИ */}
            <section className="account__card">
                <h2>Мои записи</h2>

                {bookings.length === 0 && <p>Записей нет</p>}

                {bookings.map((b) => (
                    <div key={b.id} className="account__booking">
                        <strong>{b.service_name}</strong>
                        <div>
                            {new Date(b.start_at).toLocaleString()} • {b.price} ₽
                        </div>
                        <div>Статус: {b.status}</div>
                    </div>
                ))}
            </section>
        </div>
    );
}
