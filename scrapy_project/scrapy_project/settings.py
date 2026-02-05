# Scrapy settings for scrapy_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "scrapy_project"

SPIDER_MODULES = ["scrapy_project.spiders"]
NEWSPIDER_MODULE = "scrapy_project.spiders"

ADDONS = {}


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# Obey robots.txt rules (Lo dejamos en False como tenías para evitar bloqueos innecesarios en este sitio)
ROBOTSTXT_OBEY = False

# Configuración de cortesía para no saturar el servidor
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 1  # Un segundo de base entre peticiones

# AutoThrottle: Se ajusta solo según la velocidad del servidor
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Cookies desactivadas para evitar rastreo de sesión de bot
COOKIES_ENABLED = False

# Formato de salida
FEED_EXPORT_ENCODING = "utf-8"
FEED_EXPORT_INDENT = 2

# Opcional: Si quieres ver los errores más claros en consola
LOG_LEVEL = 'INFO'