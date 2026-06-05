from django.shortcuts import render,redirect
import sqlite3
from django.contrib.auth import authenticate,logout,login
from .import models
from .forms import Online_Booking_form,offline_Booking_form,Add_Employee_form,Add_Room_form,EmployeeSalaryForm
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def Home(request):
    rooms = models.Add_Room.objects.all().order_by('?')[:6]
    return render(request, 'Home.html', {'rooms': rooms})

def all(request):
    return render(request,'allinclude.html')

def OnlineBooking(request):
    rooms = models.Add_Room.objects.filter(Status='Available')
    
    initial_data = {
        'Check_in': request.GET.get('Check_in', ''),
        'Check_out': request.GET.get('Check_out', ''),
        'ADULT': request.GET.get('ADULT', '1 ADULT'),
        'CHILDREN': request.GET.get('CHILDREN', '0 CHILDREN'),
    }

    if request.method == 'POST':
        room_no = request.POST.get('Room_No')
        check_in = request.POST.get('Check_in')
        check_out = request.POST.get('Check_out')
        nid_no = request.POST.get('Nid_No')
        phone = request.POST.get('Phone_Number')
        
        if not nid_no.isdigit():
            messages.error(request, "Identity Number must contain only digits.")
            return render(request, 'online_booking_page.html', {'rooms': rooms, 'initial_data': initial_data})
            
        if not phone.isdigit():
            messages.error(request, "Phone Number must contain only digits.")
            return render(request, 'online_booking_page.html', {'rooms': rooms, 'initial_data': initial_data})

        room_obj = models.Add_Room.objects.get(Room_Number=room_no)
        if room_obj.Status != 'Available':
             messages.warning(request, f"Sorry, Room {room_no} is currently {room_obj.Status}.")
             return render(request, 'online_booking_page.html', {'rooms': rooms, 'initial_data': initial_data})

        exists = models.Online_Booking.objects.filter(Room_No=room_no, Check_in=check_in).exclude(Status='Cancelled').exists() or \
                 models.Offline_Booking.objects.filter(Room_Number=room_no, Check_in=check_in).exclude(Status='Cancelled').exists()
        
        if exists:
            messages.warning(request, "This room is already booked for the selected date.")
            return render(request, 'online_booking_page.html', {'rooms': rooms, 'initial_data': initial_data})

        MyData = models.Online_Booking()
        MyData.Check_in = check_in
        MyData.Check_out = check_out
        MyData.ADULT = request.POST.get('ADULT')
        MyData.CHILDREN = request.POST.get('CHILDREN')
        MyData.Name = request.POST.get('Name')
        MyData.Surname = request.POST.get('Surname')
        MyData.Email = request.POST.get('Email')
        MyData.Phone_Number = phone
        MyData.Nid_No = nid_no
        MyData.City = request.POST.get('City')
        MyData.Country = request.POST.get('Country')
        MyData.Address = request.POST.get('Address')
        MyData.Room_No = room_no
        MyData.Status = 'Reserved'
        MyData.save()
        
        room_obj.Status = 'Reserved'
        room_obj.save()
        
        messages.success(request, f"Reservation confirmed! ID: #{MyData.Id}")
        return redirect('Home')
        
    return render(request, 'online_booking_page.html', {'rooms': rooms, 'initial_data': initial_data})

from django.db import IntegrityError

def Author_login(request):
    if request.method == 'POST':
        User_email = request.POST.get('Email')
        User_password = request.POST.get('Password')
        try:
            user = models.AuthorRegistration.objects.filter(Email=User_email, Password=User_password).first()
            if user:
                request.session['role'] = user.Role
                request.session['user_name'] = user.Fname
                request.session['user_email'] = user.Email
                messages.success(request, f"Welcome back, {user.Fname} ({user.Role})")
                return redirect("Adminpage")
            else:
                messages.error(request, "Invalid email or password.")
        except Exception as e:
            messages.error(request, "An unexpected error occurred during login.")
    return render(request,'Author_login_page.html')

def auth_logout(request):
    logout(request)
    request.session.flush()
    return redirect('Home')

def Author_Reg(request):
    if request.method == 'POST':
        Data = models.AuthorRegistration()
        Data.Fname = request.POST.get('Fname')
        Data.Lname = request.POST.get('Lname')
        Data.Email = request.POST.get('Email')
        Data.Phone_Number = request.POST.get('Phone_Number')
        Data.Role = request.POST.get('Role', 'Receptionist')
        Data.Password = request.POST.get('Password')
        Con_password = request.POST.get('Con_password')
        
        if Data.Password != Con_password:
            messages.error(request, "Passwords do not match.")
            return render(request,'Author_Register_Page.html')
            
        try:
            Data.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('Author_login')
        except IntegrityError:
            messages.error(request, "This email address is already registered.")
        except Exception as e:
            messages.error(request, "An error occurred during registration.")
            
    return render(request,'Author_Register_Page.html')

def UserProfile(request):
    if 'user_email' not in request.session:
        return redirect('Author_login')
    user = models.AuthorRegistration.objects.get(Email=request.session['user_email'])
    return render(request, 'admin/Profile.html', {'user': user})

def UserSettings(request):
    if 'user_email' not in request.session:
        return redirect('Author_login')
    user = models.AuthorRegistration.objects.get(Email=request.session['user_email'])
    if request.method == 'POST':
        user.Fname = request.POST.get('Fname')
        user.Lname = request.POST.get('Lname')
        user.Phone_Number = request.POST.get('Phone_Number')
        user.save()
        request.session['user_name'] = user.Fname
        messages.success(request, "Profile updated successfully.")
        return redirect('UserProfile')
    return render(request, 'admin/Settings.html', {'user': user})

def Author_ForgotPass(request):
    return render(request,'Author_forgetpass_page.html')

def all_admin(request):
    return render(request,'admin/AdminAllinclude.html')

def Admin(request):
    total_online = models.Online_Booking.objects.count()
    total_offline = models.Offline_Booking.objects.count()
    total_bookings = total_online + total_offline
    total_staff = models.Add_Employee.objects.count()
    total_rooms = models.Add_Room.objects.count()
    
    occupied_rooms = models.Add_Room.objects.filter(Status='Occupied').count()
    occupancy_rate = int((occupied_rooms / total_rooms * 100)) if total_rooms > 0 else 0
    
    recent_online = models.Online_Booking.objects.all().order_by('-Id')[:5]
    recent_offline = models.Offline_Booking.objects.all().order_by('-Customer_Id')[:5]
    
    context = {
        'recent_online': recent_online,
        'recent_offline': recent_offline,
        'total_bookings': total_bookings,
        'total_staff': total_staff,
        'total_rooms': total_rooms,
        'new_customers': total_offline,
        'occupancy_rate': occupancy_rate,
    }
    return render(request, 'admin/Admin.html', context)

def Housekeeping(request):
    rooms = models.Add_Room.objects.all().order_by('Room_Number')
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        new_status = request.POST.get('status')
        room = models.Add_Room.objects.get(Id=room_id)
        room.Status = new_status
        room.save()
        messages.success(request, f"Room {room.Room_Number} status updated to {new_status}")
        return redirect('Housekeeping')
    return render(request, 'admin/Housekeeping.html', {'rooms': rooms})

def CheckIn(request, type, id):
    if type == 'online':
        booking = models.Online_Booking.objects.get(Id=id)
        room_no = booking.Room_No
    else:
        booking = models.Offline_Booking.objects.get(Customer_Id=id)
        room_no = booking.Room_Number
    
    booking.Status = 'Checked In'
    booking.save()
    room = models.Add_Room.objects.get(Room_Number=room_no)
    room.Status = 'Occupied'
    room.save()
    
    messages.success(request, f"Checked in to Room {room_no}")
    return redirect('Adminpage')

def CheckOut(request, type, id):
    if type == 'online':
        booking = models.Online_Booking.objects.get(Id=id)
        room_no = booking.Room_No
    else:
        booking = models.Offline_Booking.objects.get(Customer_Id=id)
        room_no = booking.Room_Number
        
    booking.Status = 'Checked Out'
    booking.save()
    room = models.Add_Room.objects.get(Room_Number=room_no)
    room.Status = 'Dirty'
    room.save()
    
    messages.success(request, f"Checked out Room {room_no}")
    return redirect('Adminpage')

def Maintenance(request):
    tickets = models.MaintenanceTicket.objects.all().order_by('-Date_Reported')
    rooms = models.Add_Room.objects.all()
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        issue = request.POST.get('issue')
        priority = request.POST.get('priority')
        ticket = models.MaintenanceTicket(Room_id=room_id, Issue=issue, Priority=priority)
        ticket.save()
        room = models.Add_Room.objects.get(Id=room_id)
        room.Status = 'Maintenance'
        room.save()
        messages.warning(request, f"Room {room.Room_Number} sent to maintenance.")
        return redirect('Maintenance')
    return render(request, 'admin/Maintenance.html', {'tickets': tickets, 'rooms': rooms})

def Billing(request, type, id):
    if type == 'online':
        booking = models.Online_Booking.objects.get(Id=id)
        charges = models.GuestCharge.objects.filter(Online_Booking=booking)
        payments = models.GuestPayment.objects.filter(Online_Booking=booking)
    else:
        booking = models.Offline_Booking.objects.get(Customer_Id=id)
        charges = models.GuestCharge.objects.filter(Offline_Booking=booking)
        payments = models.GuestPayment.objects.filter(Offline_Booking=booking)
    
    total_charges = sum(c.Amount for c in charges)
    total_payments = sum(p.Amount_Paid for p in payments)
    balance = total_charges - total_payments
    
    if request.method == 'POST':
        if 'add_charge' in request.POST:
            models.GuestCharge.objects.create(
                Online_Booking=booking if type == 'online' else None,
                Offline_Booking=booking if type == 'offline' else None,
                Charge_Type=request.POST.get('charge_type'),
                Description=request.POST.get('description'),
                Amount=int(request.POST.get('amount'))
            )
        elif 'add_payment' in request.POST:
            models.GuestPayment.objects.create(
                Online_Booking=booking if type == 'online' else None,
                Offline_Booking=booking if type == 'offline' else None,
                Amount_Paid=int(request.POST.get('amount')),
                Payment_Method=request.POST.get('method'),
                Receipt_Number=request.POST.get('receipt')
            )
        return redirect('Billing', type=type, id=id)

    return render(request, 'admin/Billing.html', {
        'booking': booking, 'charges': charges, 'payments': payments,
        'total_charges': total_charges, 'total_payments': total_payments, 
        'balance': balance, 'type': type, 'id': id
    })

def Reports(request):
    from datetime import date
    today = date.today()
    
    # 1. Arrivals & Departures
    arrivals_today = models.Online_Booking.objects.filter(Check_in=today).count() + \
                    models.Offline_Booking.objects.filter(Check_in=today).count()
                    
    departures_today = models.Online_Booking.objects.filter(Check_out=today).count() + \
                      models.Offline_Booking.objects.filter(Check_out=today).count()
    
    # 2. Occupancy Metrics
    total_rooms = models.Add_Room.objects.count()
    occupied_rooms = models.Add_Room.objects.filter(Status='Occupied').count()
    dirty_rooms = models.Add_Room.objects.filter(Status='Dirty').count()
    maintenance_rooms = models.Add_Room.objects.filter(Status='Maintenance').count()
    available_rooms = total_rooms - occupied_rooms - maintenance_rooms
    
    occupancy_pct = int((occupied_rooms / total_rooms * 100)) if total_rooms > 0 else 0
    
    # 3. Revenue Reports (Manual payments recorded today)
    payments_today = models.GuestPayment.objects.filter(Date=today)
    total_revenue_today = sum(p.Amount_Paid for p in payments_today)
    
    # Revenue by Method
    mpesa_revenue = sum(p.Amount_Paid for p in payments_today.filter(Payment_Method='M-Pesa'))
    cash_revenue = sum(p.Amount_Paid for p in payments_today.filter(Payment_Method='Cash'))
    
    context = {
        'arrivals': arrivals_today,
        'departures': departures_today,
        'total_rooms': total_rooms,
        'occupied_rooms': occupied_rooms,
        'available_rooms': available_rooms,
        'dirty_rooms': dirty_rooms,
        'maintenance_rooms': maintenance_rooms,
        'occupancy_pct': occupancy_pct,
        'revenue_today': total_revenue_today,
        'mpesa_revenue': mpesa_revenue,
        'cash_revenue': cash_revenue,
        'today': today
    }
    
    return render(request, 'admin/Reports.html', context)

def Addemployee(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        Data = models.Add_Employee()
        Data.Employee_Id = request.POST.get('Employee_Id')
        Data.First_Name = request.POST.get('First_Name')
        Data.Last_Name = request.POST.get('Last_Name')
        Data.Email = request.POST.get('Email')
        Data.Mobile_Number = request.POST.get('Mobile_Number')
        Data.Joining_Date = request.POST.get('Joining_Date')
        Data.Dateof_Birth = request.POST.get('Dateof_Birth')
        Data.Departments = request.POST.get('Departments')
        Data.Gender = request.POST.get('Gender')
        Data.Blood_Group = request.POST.get('Blood_Group')
        Data.Education = request.POST.get('Education')
        Data.Personal_Identity = request.POST.get('Personal_Identity')
        Data.Guardian = request.POST.get('Guardian')
        Data.Guardian_Number = request.POST.get('Guardian_Number')
        Data.Upload_Image = upload_image
        Data.Address = request.POST.get('Address')
        Data.save()
        messages.success(request, "Staff added.")
        return redirect('Addemployee')

    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/addemployee.html',{'data':data})

def Editemployee(request,id):
    data = models.Add_Employee.objects.get(Employee_Id=id)
    if request.method == 'POST':
        form = Add_Employee_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('Allemployee')
    return render(request,'admin/Editemployee.html',{'data': data})

def Allemployee(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request, 'admin/allemployee.html', {"data": data})
    data = models.Add_Employee.objects.all().order_by('-Employee_Id')
    return render(request,'admin/allemployee.html',{'data': data})

def online_Booking_info(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        show = models.Online_Booking.objects.filter(Name=Serch) or models.Online_Booking.objects.filter(Email=Serch)
        return render(request,'admin/Online_Booking.html',{"data":show})
    data = models.Online_Booking.objects.all().order_by('-Id')
    return render(request,'admin/Online_Booking.html',{'data':data})

def Edit_online_Booking(request,id):
    data = models.Online_Booking.objects.get(Id=id)
    if request.method == 'POST':
        form = Online_Booking_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('online_Booking_info')
    return render(request,'admin/EditonlineBooking.html',{'data': data})

def AddCustomer(request):
    if request.method == 'POST':
        upload_image = request.FILES.get('Upload_Image')
        Data = models.Offline_Booking()
        Data.Check_in = request.POST.get('Check_in')
        Data.Check_out = request.POST.get('Check_out')
        Data.First_Name = request.POST.get('First_Name')
        Data.Last_Name = request.POST.get('Last_Name')
        Data.Email = request.POST.get('Email')
        Data.Mobile_Number = request.POST.get('Mobile_Number')
        Data.ADULT = request.POST.get('ADULT')
        Data.CHILDREN = request.POST.get('CHILDREN')
        Data.Total_Person = request.POST.get('Total_Person')
        Data.Select_Room = request.POST.get('Select_Room')
        Data.Room_Number = request.POST.get('Room_Number')
        Data.Gender = request.POST.get('Gender')
        Data.Personal_Identity = request.POST.get('Personal_Identity')
        Data.Country = request.POST.get('Country')
        Data.Address = request.POST.get('Address')
        Data.save()
        return redirect('AddCustomer')

    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AddCustomer.html',{'data': data})

def AllCustomer(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter(Email=Serch)
        return render(request, 'admin/AllCustomer.html', {"data": data})
    data = models.Offline_Booking.objects.all().order_by('-Customer_Id')
    return render(request,'admin/AllCustomer.html',{'data': data})

def EditCustomer(request,id):
    data = models.Offline_Booking.objects.get(Customer_Id=id)
    if request.method == 'POST':
        form = offline_Booking_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('AllCustomer')
    return render(request,'admin/EditCustomer.html',{'data': data})

def Delete(request,id):
    models.Online_Booking.objects.get(Id=id).delete()
    return redirect('online_Booking_info')

def Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        data = models.Offline_Booking.objects.filter(First_Name=Serch) or models.Offline_Booking.objects.filter(Email=Serch)
        return render(request, 'admin/AddCustomer.html', {"data": data})

def AddCustpage_Delete(request,id):
    models.Offline_Booking.objects.get(Customer_Id=id).delete()
    return redirect('AddCustomer')

def AllCustpage_Delete(request,id):
    models.Offline_Booking.objects.get(Customer_Id=id).delete()
    return redirect('AllCustomer')

def AddEmplopage_Delete(request,id):
    models.Add_Employee.objects.get(Employee_Id=id).delete()
    return redirect('Addemployee')

def Add_Employee_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        data = models.Add_Employee.objects.filter(Employee_Id=Serch) or models.Add_Employee.objects.filter(First_Name=Serch)
        return render(request,'admin/addemployee.html', {"data": data})

def AllEmployee_Delete(request,id):
    models.Add_Employee.objects.get(Employee_Id=id).delete()
    return redirect('Allemployee')

def Add_room(request):
    if request.method == 'POST':
        Data = models.Add_Room()
        Data.Room_Number = request.POST.get('Room_Number')
        Data.Room_Type = request.POST.get('Room_Type')
        Data.Room_Floor = request.POST.get('Room_Floor')
        Data.Room_Facility = request.POST.get('Room_Facility')
        Data.Room_Price = request.POST.get('Room_Price')
        Data.Room_Image = request.FILES.get('Room_Image')
        Data.save()
        return redirect('Add_room')
    data = models.Add_Room.objects.all().order_by('-Room_Number')
    return render(request, 'admin/AddRoom.html',{'data': data})

def Add_Room_Search(request):
    if request.method == 'POST':
        Serch = request.POST.get('serch')
        data = models.Add_Room.objects.filter(Room_Number=Serch)
        return render(request, 'admin/AddRoom.html',{"data": data})

def AddRooms_Delete(request,id):
    models.Add_Room.objects.get(Id=id).delete()
    return redirect('Add_room')

def EditRooms(request,id):
    data = models.Add_Room.objects.get(Id=id)
    if request.method == 'POST':
        form = Add_Room_form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('All_Room')
    return render(request,'admin/EditRooms.html',{'data': data})

def All_Room(request):
    if request.method == 'POST':
        Serch = request.POST.get('search')
        data = models.Add_Room.objects.filter(Room_Number=Serch)
        return render(request, 'admin/AllRooms.html',{"data": data})
    data = models.Add_Room.objects.all().order_by('-Id')
    return render(request, 'admin/AllRooms.html',{'data': data})

def AllRooms_Delete(request,id):
    models.Add_Room.objects.get(Id=id).delete()
    return redirect('All_Room')

def AddEmployeeSalary(request):
    if request.method == 'POST':
        Data = models.EmployeeSalary()
        Data.Employee_Id_id = request.POST.get('Employee_Id')
        Data.Employee_Name = request.POST.get('Employee_Name')
        Data.Email = request.POST.get('Email')
        Data.Mobile_Number = request.POST.get('Mobile_Number')
        Data.Departments = request.POST.get('Departments')
        Data.Salary = request.POST.get('Salary')
        Data.save()
        return redirect('AddEmployeeSalary')
    return render(request, 'admin/AddEmployeeSalary.html')

def EmployeeShow(request):
    return render(request, 'admin/EmployeeShow.html')
