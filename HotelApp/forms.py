from django import forms
from .import models

class OnlineBookingForm(forms.ModelForm):
    class Meta:
        model = models.OnlineBooking
        fields = "__all__"
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

class OfflineBookingForm(forms.ModelForm):
    class Meta:
        model = models.OfflineBooking
        fields = "__all__"
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = "__all__"
        widgets = {
            'joining_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = models.Room
        fields = "__all__"

class EmployeeSalaryForm(forms.ModelForm):
    class Meta:
        model = models.EmployeeSalary
        fields = "__all__"
