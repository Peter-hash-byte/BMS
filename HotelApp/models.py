from django.db import models

# Create your models here.
class AuthorRegistration(models.Model):
    ROLE_CHOICES = [
        ('Receptionist', 'Receptionist'),
        ('Housekeeper', 'Housekeeper'),
        ('Manager', 'Manager'),
        ('Administrator', 'Administrator'),
    ]
    Id = models.AutoField(primary_key=True)
    Fname = models.CharField(max_length=255)
    Lname = models.CharField(max_length=255)
    Email = models.CharField(max_length=255,unique=True)
    Phone_Number = models.BigIntegerField()
    Password = models.CharField(max_length=255)
    Role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Receptionist')
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.Fname
    class Meta:
        db_table = 'Authority_reg'

class Online_Booking(models.Model):
    STATUS_CHOICES = [
        ('Inquiry', 'Inquiry'),
        ('Reserved', 'Reserved'),
        ('Confirmed', 'Confirmed'),
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
    ]
    Id = models.AutoField(primary_key=True)
    Check_in = models.DateField()
    Check_out = models.DateField()
    ADULT = models.CharField(max_length=255)
    CHILDREN = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Phone_Number = models.BigIntegerField()
    City = models.CharField(max_length=255)
    Country = models.CharField(max_length=255)
    Nid_No = models.BigIntegerField() # Numeric only
    Address = models.TextField(blank=True, null=True)
    Room_No = models.CharField(max_length=255, null=True)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Reserved')
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.Name} {self.Surname} - Room {self.Room_No} ({self.Status})"
    class Meta:
        db_table = 'Online_Booking_table'

class Offline_Booking(models.Model):
    STATUS_CHOICES = [
        ('Reserved', 'Reserved'),
        ('Confirmed', 'Confirmed'),
        ('Checked In', 'Checked In'),
        ('Checked Out', 'Checked Out'),
        ('Cancelled', 'Cancelled'),
        ('No Show', 'No Show'),
    ]
    Customer_Id = models.AutoField(primary_key=True)
    Check_in = models.DateField()
    Check_out = models.DateField()
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255)
    Mobile_Number = models.BigIntegerField()
    ADULT = models.CharField(max_length=255)
    CHILDREN = models.CharField(max_length=255)
    Total_Person = models.IntegerField()
    Select_Room = models.CharField(max_length=255)
    Room_Number = models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Personal_Identity = models.BigIntegerField() 
    Country = models.CharField(max_length=255)
    Address = models.TextField(blank=True, null=True)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Reserved')
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.First_Name} - Room {self.Room_Number}"
    class Meta:
        db_table = 'Offline_Booking_Customer'


class Add_Employee(models.Model):
    Employee_Id = models.CharField(max_length=255,primary_key=True)
    First_Name = models.CharField(max_length=255)
    Last_Name = models.CharField(max_length=255)
    Email = models.EmailField(max_length=255,unique=True)
    Mobile_Number = models.BigIntegerField(unique=True)
    Joining_Date = models.DateField()
    Dateof_Birth = models.DateField()
    Departments = models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Blood_Group = models.CharField(max_length=255)
    Education = models.CharField(max_length=255)
    Personal_Identity = models.BigIntegerField(unique=True)
    Guardian = models.CharField(max_length=255)
    Guardian_Number = models.BigIntegerField()
    Upload_Image = models.ImageField(upload_to='employees/')
    Address = models.TextField(blank=True, null=True)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.First_Name} {self.Last_Name} ({self.Employee_Id})"
    class Meta:
        db_table = 'Add_Employees'

class Add_Room(models.Model):
    ROOM_STATUS = [
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Occupied', 'Occupied'),
        ('Dirty', 'Dirty'),
        ('Cleaning', 'Cleaning'),
        ('Maintenance', 'Maintenance'),
        ('Out of Service', 'Out of Service'),
    ]
    Id = models.AutoField(primary_key=True)
    Room_Number = models.CharField(max_length=255,unique=True)
    Room_Type = models.CharField(max_length=255)
    Room_Floor = models.CharField(max_length=255)
    Room_Facility = models.CharField(max_length=500)
    Room_Price = models.IntegerField()
    Room_Image = models.ImageField(upload_to='rooms/')
    Status = models.CharField(max_length=20, choices=ROOM_STATUS, default='Available')
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"Room {self.Room_Number} ({self.Status})"
    class Meta:
        db_table = 'Add_Room'

# --- NEW PMS MODULES ---

class GuestCharge(models.Model):
    """Tracks individual charges on a guest folio (Room, Restaurant, Laundry, etc.)"""
    CHARGE_TYPES = [
        ('Room', 'Room'),
        ('Restaurant', 'Restaurant'),
        ('Laundry', 'Laundry'),
        ('Conference', 'Conference'),
        ('Other', 'Other'),
    ]
    Id = models.AutoField(primary_key=True)
    # Link to either online or offline booking
    Online_Booking = models.ForeignKey(Online_Booking, on_delete=models.CASCADE, null=True, blank=True)
    Offline_Booking = models.ForeignKey(Offline_Booking, on_delete=models.CASCADE, null=True, blank=True)
    
    Charge_Type = models.CharField(max_length=50, choices=CHARGE_TYPES)
    Description = models.CharField(max_length=255)
    Amount = models.IntegerField()
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)

class GuestPayment(models.Model):
    """Records manual payments received at reception"""
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('M-Pesa', 'M-Pesa'),
        ('Card', 'Card'),
        ('Bank Transfer', 'Bank Transfer'),
    ]
    Id = models.AutoField(primary_key=True)
    Online_Booking = models.ForeignKey(Online_Booking, on_delete=models.CASCADE, null=True, blank=True)
    Offline_Booking = models.ForeignKey(Offline_Booking, on_delete=models.CASCADE, null=True, blank=True)
    
    Amount_Paid = models.IntegerField()
    Payment_Method = models.CharField(max_length=50, choices=PAYMENT_METHODS)
    Receipt_Number = models.CharField(max_length=100, unique=True)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)

class MaintenanceTicket(models.Model):
    """Staff can report issues for specific rooms"""
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
    Id = models.AutoField(primary_key=True)
    Room = models.ForeignKey(Add_Room, on_delete=models.CASCADE)
    Issue = models.CharField(max_length=255)
    Priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='Medium')
    Status = models.CharField(max_length=20, choices=TICKET_STATUS, default='Open')
    Assigned_To = models.CharField(max_length=255, blank=True, null=True)
    Date_Reported = models.DateField(auto_now_add=True)
    Date_Resolved = models.DateField(null=True, blank=True)

class EmployeeSalary(models.Model):
    Employee_Id = models.ForeignKey(Add_Employee,on_delete=models.CASCADE)
    Employee_Name = models.CharField(max_length=255)
    Mobile_Number = models.CharField(max_length=255)
    Email = models.EmailField(max_length=500)
    Departments = models.CharField(max_length=255)
    Salary = models.IntegerField()
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return str(self.Employee_Id)
    class Meta:
        db_table = 'Employee_Salaries'
