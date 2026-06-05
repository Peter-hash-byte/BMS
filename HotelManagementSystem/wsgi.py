"""
WSGI config for Kivulini Hotel PMS.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HotelManagementSystem.settings')

application = get_wsgi_application()
