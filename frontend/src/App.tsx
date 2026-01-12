// frontend/src/App.tsx — роутинг приложения
// Назначение: маршруты сайта (корректная навигация без редиректов на главную)

import { Routes, Route, Navigate } from "react-router-dom"; //
import { MainLayout } from "./components/layout/MainLayout/MainLayout"; //

import { Home } from "./pages/Home/Home"; //
import { Services } from "./pages/Services/Services"; //
import { ServicesCategory } from "./pages/ServicesCategory/ServicesCategory"; //
import { ServiceDetail } from "./pages/ServiceDetail/ServiceDetail"; //
import { Booking } from "./pages/Booking/Booking"; //

export default function App() {
  return (
    <Routes>
      {/* layout всегда общий */}
      <Route element={<MainLayout />}>
        {/* главная */}
        <Route path="/" element={<Home />} />

        {/* услуги */}
        <Route path="/services" element={<Services />} />
        <Route path="/services/:category" element={<ServicesCategory />} />
        <Route path="/services/:category/:slug" element={<ServiceDetail />} />

        {/* запись — ТОЛЬКО с serviceId */}
        <Route path="/booking/:serviceId" element={<Booking />} /> {/* (я добавил) */}

        {/* защита от несуществующих роутов */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
