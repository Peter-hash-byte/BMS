import os
import sys

# Set up paths
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'HotelManagementSystem.settings'

# Import the WSGI application
from HotelManagementSystem.wsgi import application as application
