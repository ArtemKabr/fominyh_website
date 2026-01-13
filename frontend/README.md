# Frontend — FOMINYH WEBSITE

Frontend часть сайта салона массажа **FOMINYH WEBSITE**.  
Реализован на **React + TypeScript + Vite**.  
Работает с backend через REST API (FastAPI).

---

## 📦 Стек

- React
- TypeScript
- Vite
- React Router
- Fetch API
- CSS (без UI-фреймворков)
- Nginx (prod)

---

## 📁 Структура

```text
frontend/
├── public/
│   └── images/                # изображения (категории, услуги, баннеры)
├── src/
│   ├── api/                   # API-клиенты (services, booking, auth)
│   ├── components/            # переиспользуемые компоненты
│   ├── pages/                 # страницы (Home, Services, Booking и т.д.)
│   ├── layouts/               # layout (Header / Footer)
│   ├── router/                # роутинг
│   ├── styles/                # общие стили
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── vite.config.ts
├── package.json
└── tsconfig.json
⚙️ Установка и запуск (dev)
1. Установить зависимости
bash
Копировать код
npm install
или

bash
Копировать код
npm ci
2. Запуск в режиме разработки
bash
Копировать код
npm run dev
По умолчанию:

arduino
Копировать код
http://localhost:5173
🔌 Подключение к backend
API URL задаётся через переменную окружения.

.env
env
Копировать код
VITE_API_URL=http://localhost/api
Использование в коде:

ts
Копировать код
const API_URL = import.meta.env.VITE_API_URL;
Backend должен быть доступен, например:

arduino
Копировать код
http://localhost/api/services
🧱 Сборка production
bash
Копировать код
npm run build
Результат:

Копировать код
dist/
🚀 Деплой (Nginx)
1. Скопировать dist на сервер
bash
Копировать код
scp -r dist/* user@server:/var/www/frontend/
2. Пример nginx.conf
nginx
Копировать код
server {
    listen 80;
    server_name example.com;

    root /var/www/frontend;
    index index.html;

    location / {
        try_files $uri /index.html;
    }

    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
🔄 Обновление фронта на сервере
bash
Копировать код
npm run build
scp -r dist/* user@server:/var/www/frontend/
Перезапуск nginx (если нужно):

bash
Копировать код
sudo systemctl reload nginx
🧪 Тестирование
Unit-тесты не используются (по требованиям проекта).
Проверка — через:

ручное тестирование UI

интеграция с backend API

проверка сценариев записи

❗ Частые проблемы
1. Белый экран после деплоя
Причина: нет try_files /index.html.

2. API не работает
Проверь:

VITE_API_URL

backend запущен

nginx проксирует /api

3. Изменил код — но ничего не меняется
Нужно пересобрать:

bash
Копировать код
npm run build
🧠 Принципы
frontend не содержит бизнес-логики

вся логика — в backend

frontend = UI + запросы

📌 Связанные README
Backend: backend/README.md

Корень проекта: README.md