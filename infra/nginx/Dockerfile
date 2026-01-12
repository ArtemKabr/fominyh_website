# infra/nginx/Dockerfile — nginx reverse proxy

FROM nginx:1.25-alpine

# УДАЛЯЕМ дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf

# КОПИРУЕМ наш основной конфиг
COPY infra/nginx/nginx.conf /etc/nginx/nginx.conf
