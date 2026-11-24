import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# Импортируем main из твоего файла bot.py
from bot import main as start_bot

# --- Простой веб-сервер для health check ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Этот сервер будет отвечать "OK" на GET-запросы
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b"OK")

    def do_HEAD(self):
        # Добавили этот метод, чтобы UptimeRobot получал ответ 200 OK
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()


def run_health_server():
    # Render сам сообщает, на каком порту нужно слушать
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    print(f"Health check server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    # Запускаем веб-сервер в отдельном потоке
    health_thread = threading.Thread(target=run_health_server)
    health_thread.daemon = True
    health_thread.start()

    # Запускаем основного бота
    print("Starting bot...")
    asyncio.run(start_bot())
