// frontend/src/components/layout/Header/Header.tsx — шапка
// Назначение: навигация + авторизация

import { NavLink, useNavigate } from "react-router-dom"; // (я добавил)
import "./header.css";

export function Header() {
    const navigate = useNavigate(); // (я добавил)
    const token = localStorage.getItem("token");

    const logout = () => {
        localStorage.removeItem("token"); // (я добавил)
        navigate("/"); // (я добавил)
    };

    return (
        <header className="header">
            <div className="header__inner header__inner--center">
                <img
                    className="header__logo"
                    src="/images/Логотип ЕФ1133.png"
                    alt="Logo"
                />

                <nav className="header__nav header__nav--center">
                    <NavLink className="header__link" to="/">
                        Главная
                    </NavLink>

                    <NavLink className="header__link" to="/services">
                        Услуги
                    </NavLink>

                    <NavLink className="header__link" to="/services">
                        Запись
                    </NavLink>

                    {token ? (
                        <>
                            <NavLink
                                className="header__link header__link--account"
                                to="/account"
                            >
                                Личный кабинет
                            </NavLink>

                            <button
                                className="header__link header__logout"
                                onClick={logout}
                            >
                                Выйти
                            </button>
                        </>
                    ) : (
                        <NavLink
                            className="header__link header__link--account"
                            to="/login"
                        >
                            Войти
                        </NavLink>
                    )}
                </nav>
            </div>
        </header>
    );
}
