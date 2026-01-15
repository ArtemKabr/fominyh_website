// frontend/src/App.tsx — роутинг приложения
// Назначение: маршруты сайта (корректная навигация без редиректов на главную)

import { Routes, Route, Navigate } from "react-router-dom"; //
import { MainLayout } from "./components/layout/MainLayout/MainLayout"; //

import { Home } from "./pages/Home/Home"; //
import { Services } from "./pages/Services/Services"; //
import { ServicesCategory } from "./pages/ServicesCategory/ServicesCategory"; //
import { ServiceDetail } from "./pages/ServiceDetail/ServiceDetail"; //
import { Booking } from "./pages/Booking/Booking"; //
import { AccountPage } from "./pages/Account/AccountPage";
import { LoginPage } from "./pages/Login/LoginPage";
import { RegisterPage } from "./pages/Register/RegisterPage";
import { AccountPage } from "./pages/Account/AccountPage";
import { AdminPage } from "./pages/Admin/AdminPage";
import { AdminLayout } from "./pages/Admin/AdminLayout"; // (я добавил)
import { BookingsPage } from "./pages/Admin/BookingsPage"; // (я добавил)
import { HistoryPage } from "./pages/Admin/HistoryPage"; // (я добавил)
import { SlotsPage } from "./pages/Admin/SlotsPage"; // (я добавил)
import { ServicesPage } from "./pages/Admin/ServicesPage"; // (я добавил)
import { UsersPage } from "./pages/Admin/UsersPage"; // (я добавил)
import { StatsPage } from "./pages/Admin/StatsPage"; // (я добавил)
import { ReservePage } from "./pages/Admin/ReservePage";


export default function App() {
  return (
    <Routes>
      {/* layout всегда общий */}
      <Route element={<MainLayout />}>
        {/* главная */}
        <Route path="/" element={<Home />} />

        {/* ЛК пользователя */}
        <Route path="/account" element={<AccountPage />} />


        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<BookingsPage />} />
          <Route path="bookings" element={<BookingsPage />} />
          <Route path="history" element={<HistoryPage />} />
          <Route path="slots" element={<SlotsPage />} />
          <Route path="services" element={<ServicesPage />} />
          <Route path="users" element={<UsersPage />} />
          <Route path="stats" element={<StatsPage />} />
          <Route path="reserve" element={<ReservePage />} />
      </Route>


        {/* услуги */}
        <Route path="/services" element={<Services />} />
        <Route path="/services/:category" element={<ServicesCategory />} />
        <Route path="/services/:category/:slug" element={<ServiceDetail />} />


        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/account" element={<AccountPage />} />


        <Route path="/admin" element={<AdminPage />} />



        {/* запись — ПО SLUG */}
        <Route path="/booking/:slug" element={<Booking />} /> {/* (я исправил) */}

        {/* защита от несуществующих роутов */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
