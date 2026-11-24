import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- Импортируем и запускаем твоего бота ---
# Мы предполагаем, что основной код бота находится в файле bot.py
# и запускается через функцию main(), как у нас и было.
from bot import main as start_bot

# --- Простой веб-сервер для "здоровья" ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Этот сервер будет отвечать "OK" на любой запрос,
        # показывая хостингу, что бот жив.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Health check server running on port {port}")
    server.serve_forever()

# --- Запускаем всё вместе ---
if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True # Поток завершится вместе с основной программой
    health_thread.start()

    # Запускаем бота в основном потоке
    print("Starting bot...")
    asyncio.run(start_bot())
