"""
Diaco MES — Passenger WSGI (cPanel/Shared Hosting)
"""
import os
import sys

project_path = '/home1/chelleh1/diaco'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# venv site-packages
venv_path = '/home1/chelleh1/virtualenv/diaco/3.10/lib/python3.10/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

# load .env
env_file = os.path.join(project_path, '.env')
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip())

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
