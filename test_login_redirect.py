import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HotelManagementSystem.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from HotelApp.models import CustomUser

def test_login():
    client = Client()
    # Ensure user exists
    user, created = CustomUser.objects.get_or_create(
        username='testuser',
        email='test@example.com',
        defaults={'first_name': 'Test', 'role': 'Manager'}
    )
    user.set_password('password123')
    user.save()
    
    print(f"Testing login for {user.email}...")
    
    login_url = reverse('Author_login')
    response = client.post(login_url, {'Email': 'test@example.com', 'Password': 'password123'}, follow=True)
    
    print(f"Final URL: {response.request['PATH_INFO']}")
    print(f"Status Code: {response.status_code}")
    
    if response.request['PATH_INFO'] == reverse('Adminpage'):
        print("SUCCESS: Redirected to Adminpage")
    elif response.request['PATH_INFO'] == reverse('Home'):
        print("FAILURE: Redirected to Home")
    else:
        print(f"UNKNOWN: Redirected to {response.request['PATH_INFO']}")

if __name__ == "__main__":
    test_login()
