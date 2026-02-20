"""
Diaco MES - Production Settings
================================
تنظیمات محیط تولید. امنیت بالا.
"""
from .base import *

# =============================================================================
# SECURITY
# =============================================================================
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# =============================================================================
# CORS - فقط دامنه‌های مجاز
# =============================================================================
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://iranianc.com',
    cast=Csv()
)
