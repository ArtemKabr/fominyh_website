// frontend/src/components/layout/Header/Header.tsx — шапка
import {NavLink} from "react-router-dom"; //
import "./header.css"; // 

export function Header() {
    return (
        <header className="header">
            <div className="header__inner header__inner--center"> {/* я добавил */}
                <img
                    className="header__logo"
                    src="/images/Логотип ЕФ1133.png"
                    alt="Logo"
                />

                <nav className="header__nav header__nav--center"> {/* я добавил */}
                    <NavLink className="header__link" to="/">
                        Главная
                    </NavLink>
                    <NavLink className="header__link" to="/services">
                        Услуги
                    </NavLink>
                    <NavLink className="header__link" to="/services">
                        Запись
                    </NavLink>


                </nav>
            </div>
        </header>
    );
}
