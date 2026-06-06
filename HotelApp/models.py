from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Receptionist', 'Receptionist'),
        ('Housekeeper', 'Housekeeper'),
        ('Manager', 'Manager'),
        ('Administrator', 'Administrator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Receptionist')
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Room(models.Model):
    ROOM_STATUS = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
        ('Dirty', 'Dirty'),
        ('Cleaning', 'Cleaning'),
        ('Maintenance', 'Maintenance'),
        ('Out of Service', 'Out of Service'),
    ]
    room_number = models.CharField(max_length=255, unique=True)
    room_type = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)
    facility = models.CharField(max_length=500)
    price = models.IntegerField()
    image = models.ImageField(upload_to='rooms/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=ROOM_STATUS, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.status})"

class OnlineBooking(models.Model):
    STATUS_CHOICES = [
        ('Inquiry', 'Inquiry'),
        ('Reserved', 'Reserved'),
        ('Confirmed', 'Confirmed'),
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
    ]
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    id_number = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='online_bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Reserved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Room {self.room}"

class OfflineBooking(models.Model):
    STATUS_CHOICES = [
        ('Reserved', 'Reserved'),
        ('Confirmed', 'Confirmed'),
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
    ]
    check_in = models.DateField()
    check_out = models.DateField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, related_name='offline_bookings')
    gender = models.CharField(max_length=20)
    id_number = models.CharField(max_length=50)
    country = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Reserved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - Room {self.room}"

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    joining_date = models.DateField()
    date_of_birth = models.DateField()
    department = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    blood_group = models.CharField(max_length=10)
    education = models.CharField(max_length=255)
    id_number = models.CharField(max_length=50, unique=True)
    guardian_name = models.CharField(max_length=255)
    guardian_phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='employees/', null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"

class GuestCharge(models.Model):
    CHARGE_TYPES = [
        ('Room', 'Room'),
        ('Restaurant', 'Restaurant'),
        ('Laundry', 'Laundry'),
        ('Conference', 'Conference'),
        ('Other', 'Other'),
    ]
    online_booking = models.ForeignKey(OnlineBooking, on_delete=models.CASCADE, null=True, blank=True)
    offline_booking = models.ForeignKey(OfflineBooking, on_delete=models.CASCADE, null=True, blank=True)
    charge_type = models.CharField(max_length=50, choices=CHARGE_TYPES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class GuestPayment(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('M-Pesa', 'M-Pesa'),
        ('Card', 'Card'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    online_booking = models.ForeignKey(OnlineBooking, on_delete=models.CASCADE, null=True, blank=True)
    offline_booking = models.ForeignKey(OfflineBooking, on_delete=models.CASCADE, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    receipt_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class MaintenanceTicket(models.Model):
    PRIORITY_LEVELS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Emergency', 'Emergency'),
    ]
    TICKET_STATUS = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue = models.CharField(max_length=255)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='Medium')
    status = models.CharField(max_length=20, choices=TICKET_STATUS, default='Open')
    assigned_to = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

class EmployeeSalary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    salary_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.salary_amount}"
