# frontend/Dockerfile — продакшн фронта (без node)
FROM nginx:stable-alpine

COPY infra/nginx/nginx.conf /etc/nginx/nginx.conf
COPY dist /usr/share/nginx/html
