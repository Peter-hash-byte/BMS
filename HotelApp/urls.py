from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="Home"),
    path('all/', views.all_include, name="all_include"),
    path('OnlineBooking/', views.OnlineBooking, name='OnlineBooking'),
    
    # Auth
    path('login/', views.Author_login, name='Author_login'),
    path('logout/', views.auth_logout, name='auth_logout'),
    path('register/', views.Author_Reg, name='Author_Reg'),
    path('forgot-password/', views.Author_ForgotPass, name='Author_ForgotPass'),
    
    # Admin Dashboard
    path('admin-page/', views.Admin, name='Adminpage'),
    path('admin/all-include/', views.all_admin, name='all_admin'),
    
    # Employees
    path('employees/add/', views.Addemployee, name='Addemployee'),
    path('employees/edit/<str:id>/', views.Editemployee, name='Editemployee'),
    path('employees/all/', views.Allemployee, name='Allemployee'),
    path('employees/delete/<str:id>/', views.AllEmployee_Delete, name='AllEmployee_Delete'),
    path('employees/search/', views.Add_Employee_Search, name='Add_Employee_Search'),
    path('employees/salary/add/', views.AddEmployeeSalary, name='AddEmployeeSalary'),
    path('employees/show/', views.EmployeeShow, name='EmployeeShow'),
    path('employees/page-delete/<str:id>/', views.AddEmplopage_Delete, name='AddEmplopage_Delete'),
    
    # Bookings
    path('bookings/online/', views.online_Booking_info, name='online_Booking_info'),
    path('bookings/online/edit/<int:id>/', views.Edit_online_Booking, name='Edit_online_Booking'),
    path('bookings/online/delete/<int:id>/', views.Delete, name='delete'),
    
    path('bookings/offline/add/', views.AddCustomer, name='AddCustomer'),
    path('bookings/offline/all/', views.AllCustomer, name='AllCustomer'),
    path('bookings/offline/edit/<int:id>/', views.EditCustomer, name='EditCustomer'),
    path('bookings/offline/delete/<int:id>/', views.AllCustpage_Delete, name='AllCustpage_Delete'),
    path('bookings/offline/page-delete/<int:id>/', views.AddCustpage_Delete, name='AddCustpage_Delete'),
    path('bookings/search/', views.Search, name='Search'),
    
    # Rooms
    path('rooms/add/', views.Add_room, name='Add_room'),
    path('rooms/all/', views.All_Room, name='All_Room'),
    path('rooms/edit/<int:id>/', views.EditRooms, name='EditRooms'),
    path('rooms/delete/<int:id>/', views.AllRooms_Delete, name='AllRooms_Delete'),
    path('rooms/add-delete/<int:id>/', views.AddRooms_Delete, name='AddRooms_Delete'),
    path('rooms/search/', views.Add_Room_Search, name='Add_Room_Search'),
    
    # Operations
    path('housekeeping/', views.Housekeeping, name='Housekeeping'),
    path('check-in/<str:type>/<int:id>/', views.CheckIn, name='CheckIn'),
    path('check-out/<str:type>/<int:id>/', views.CheckOut, name='CheckOut'),
    path('maintenance/', views.Maintenance, name='Maintenance'),
    path('billing/<str:type>/<int:id>/', views.Billing, name='Billing'),
    path('reports/', views.Reports, name='Reports'),
    
    # User Profile
    path('profile/', views.UserProfile, name='UserProfile'),
    path('settings/', views.UserSettings, name='UserSettings'),
]
