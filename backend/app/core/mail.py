# backend/app/core/mail.py — отправка писем
# Назначение: регистрация и сброс пароля (SMTP)

import smtplib
import ssl
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.settings import settings

logger = logging.getLogger(__name__)


async def send_email(
    to_email: str,
    subject: str,
    body: str,
) -> None:
    """Отправка email через SMTP. Ошибки не валят API."""

    # Проверяем, настроен ли SMTP
    if not all(
        [
            settings.smtp_host,
            settings.smtp_port,
            settings.smtp_user,
            settings.smtp_password,
            settings.smtp_from,
        ]
    ):
        logger.warning("SMTP отключён или не настроен.")
        return

    logger.info("SMTP send_email вызван для %s", to_email)

    # Формируем письмо
    msg = MIMEMultipart()
    msg["From"] = settings.smtp_from
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        # создаём контекст SSL
        context = ssl.create_default_context()

        # выбираем класс в зависимости от порта
        if settings.smtp_port == 465:
            # порт 465 — SSL-соединение, starttls() не вызываем
            with smtplib.SMTP_SSL(
                settings.smtp_host, settings.smtp_port, timeout=10
            ) as server:
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)
        else:
            # обычно порт 587 — StartTLS
            with smtplib.SMTP(
                settings.smtp_host, settings.smtp_port, timeout=10
            ) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(settings.smtp_user, settings.smtp_password)
                server.send_message(msg)

        logger.info("SMTP письмо успешно отправлено на %s", to_email)

    except Exception as exc:
        # Логируем ошибку, но не пробрасываем, чтобы API не падал
        logger.exception("SMTP ошибка при отправке письма: %s", exc)
        return
