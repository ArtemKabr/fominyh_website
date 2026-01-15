// frontend/src/pages/Register/RegisterPage.tsx — страница регистрации
// Назначение: регистрация пользователя (без JWT)

import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import "./register.css";

export function RegisterPage() {
    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(""); // (я добавил)

    const submit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");

        const res = await fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name,
                phone,
                email,
                password,
            }),
        });

        if (!res.ok) {
            setError("Ошибка регистрации");
            return;
        }

        const data: { user_id: number } = await res.json();

        localStorage.setItem("user_id", String(data.user_id)); // (я добавил)
        navigate("/account"); // (я добавил)
    };

    return (
        <div className="register">
            <div className="register__card">
                <h1 className="register__title">Регистрация</h1>

                {error && <div className="register__error">{error}</div>} {/* я добавил */}

                <form className="register__form" onSubmit={submit}>
                    <input
                        type="text"
                        placeholder="Имя"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                    />

                    <input
                        type="tel"
                        placeholder="Телефон"
                        value={phone}
                        onChange={(e) => setPhone(e.target.value)}
                        required
                    />

                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />

                    <input
                        type="password"
                        placeholder="Пароль"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />

                    <button type="submit">
                        Зарегистрироваться
                    </button>
                </form>

                <div className="register__hint">
                    Уже есть аккаунт?{" "}
                    <NavLink to="/login">Войти</NavLink>
                </div>
            </div>
        </div>
    );
}
