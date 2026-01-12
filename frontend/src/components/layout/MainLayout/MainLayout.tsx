// frontend/src/components/layout/MainLayout/MainLayout.tsx — основной layout
import { Outlet } from "react-router-dom"; // 
import { Header } from "../Header/Header"; // 
import { Footer } from "../Footer/Footer"; // 
import "./main-layout.css"; // 

export function MainLayout() {
  return (
    <div className="layout">
      <section className="hero"> {/* я добавил */}
        <div className="hero__overlay" /> {/* я добавил */}

        <div className="hero__content"> {/* я добавил */}
          <Header /> {/* ← header теперь ВНУТРИ баннера */}
        </div>
      </section>

      <main className="layout__content">
        <Outlet />
      </main>

      <Footer />
    </div>
  );
}
