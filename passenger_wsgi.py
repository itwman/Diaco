"""
Diaco MES — Passenger WSGI Entry Point
=======================================
چابکان از Phusion Passenger استفاده می‌کند.
این فایل باید در ریشه پروژه باشد.
"""
import os
import sys

# مسیر پروژه را به Python path اضافه کن
project_path = os.path.dirname(os.path.abspath(__file__))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# مسیر venv را اضافه کن
venv_path = os.path.join(project_path, 'venv', 'lib', 'python3.11', 'site-packages')
if os.path.exists(venv_path) and venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# settings را روی production بگذار
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# فایل .env را بارگذاری کن
from dotenv import load_dotenv
env_path = os.path.join(project_path, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

# WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
