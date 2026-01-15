// frontend/src/pages/Login/LoginPage.tsx — страница входа
// Назначение: вход пользователя или администратора (разные кабинеты)

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "./login.css";

export function LoginPage() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const login = async (asAdmin: boolean) => {
        setError("");

        const loginRes = await fetch("/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (!loginRes.ok) {
            setError("Неверный email или пароль");
            return;
        }

        const loginData: { user_id: number } = await loginRes.json();
        const userId = loginData.user_id;

        if (!userId) {
            setError("Не удалось получить пользователя");
            return;
        }

        localStorage.setItem("user_id", String(userId));

        const meRes = await fetch("/api/auth/me", {
            method: "GET",
            headers: {
                "X-User-Id": String(userId),
            },
        });

        if (!meRes.ok) {
            localStorage.removeItem("user_id");
            setError("Ошибка авторизации");
            return;
        }

        const user: { is_admin: boolean } = await meRes.json();

        if (user.is_admin && !asAdmin) {
            localStorage.removeItem("user_id");
            setError(
                "Администратору нужно войти через кнопку «Войти как администратор салона»"
            );
            return;
        }

        if (!user.is_admin && asAdmin) {
            localStorage.removeItem("user_id");
            setError("У вас нет прав администратора");
            return;
        }

        if (user.is_admin && asAdmin) {
            navigate("/admin");
            return;
        }

        navigate("/account");
    };

    return (
        <div className="login">
            <div className="login__card">
                <h1 className="login__title">Вход</h1>

                {error && <div className="login__error">{error}</div>}

                <form
                    className="login__form"
                    onSubmit={(e) => {
                        e.preventDefault();
                        login(false);
                    }}
                >
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

                    <button type="submit" className="login__submit">
                        Войти
                    </button>
                </form>

                <button
                    type="button"
                    className="login__admin-btn"
                    onClick={() => login(true)}
                >
                    Войти как администратор салона
                </button>

                <div className="login__footer">
                    Нет аккаунта?{" "}
                    <Link to="/register">Регистрация</Link>
                </div>
            </div>
        </div>
    );
}
