from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from . import models, forms

# --- Public Views ---

def Home(request):
    # Optimized: Select only needed fields and limit query
    rooms = models.Room.objects.filter(status='Available').only('room_type', 'price', 'facility', 'image')[:6]
    return render(request, 'Home.html', {'rooms': rooms})

def all_include(request):
    return render(request, 'allinclude.html')

def OnlineBooking(request):
    rooms = models.Room.objects.filter(status='Available').only('id', 'room_type', 'room_number', 'price', 'facility', 'image', 'floor')
    initial_data = {
        'check_in': request.GET.get('check_in', ''),
        'check_out': request.GET.get('check_out', ''),
        'adults': request.GET.get('adults', '1'),
        'children': request.GET.get('children', '0'),
    }

    if request.method == 'POST':
        form = forms.OnlineBookingForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['room']
            check_in = form.cleaned_data['check_in']
            
            # Optimized: Combine existence checks
            if models.OnlineBooking.objects.filter(room=room, check_in=check_in).exclude(status='Cancelled').exists() or \
               models.OfflineBooking.objects.filter(room=room, check_in=check_in).exclude(status='Cancelled').exists():
                messages.warning(request, "This room is already booked for the selected date.")
                return render(request, 'online_booking_page.html', {'rooms': rooms, 'initial_data': initial_data, 'form': form})

            booking = form.save(commit=False)
            booking.status = 'Reserved'
            booking.save()
            
            room.status = 'Reserved'
            room.save()
            
            messages.success(request, f"Reservation confirmed! ID: #{booking.id}")
            return redirect('Home')
            
    return render(request, 'online_booking_page.html', {'rooms': rooms, 'initial_data': initial_data})

# --- Authentication ---

def Author_login(request):
    if request.user.is_authenticated:
        return redirect('Adminpage')
        
    next_url = request.GET.get('next', 'Adminpage')
        
    if request.method == 'POST':
        identifier = request.POST.get('Email', '').strip()
        password = request.POST.get('Password', '')
        
        # Optimized: Single query to find the user by email or username
        user_obj = models.CustomUser.objects.filter(Q(email__iexact=identifier) | Q(username__iexact=identifier)).first()
                   
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Security: Prevent Open Redirects
                redirect_to = request.POST.get('next', next_url)
                if not url_has_allowed_host_and_scheme(url=redirect_to, allowed_hosts={request.get_host()}):
                    redirect_to = 'Adminpage'
                    
                messages.success(request, f"Welcome back, {user.first_name or user.username} ({user.role})")
                return redirect(redirect_to)
            else:
                messages.error(request, "Invalid password.")
        else:
            messages.error(request, "User not found. Please check your email/username.")
            
    return render(request, 'Author_login_page.html', {'next': next_url})

def auth_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('Home')

def Author_Reg(request):
    if request.method == 'POST':
        fname = request.POST.get('Fname', '').strip()
        lname = request.POST.get('Lname', '').strip()
        email = request.POST.get('Email', '').strip()
        phone = request.POST.get('Phone_Number', '').strip()
        role = request.POST.get('Role', 'Receptionist')
        password = request.POST.get('Password', '')
        con_password = request.POST.get('Con_password', '')
        
        if password != con_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'Author_Register_Page.html')
            
        if not email:
            messages.error(request, "Email is required.")
            return render(request, 'Author_Register_Page.html')
            
        try:
            # Use full email as username to ensure uniqueness
            username = email
            user = models.CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fname,
                last_name=lname,
                role=role,
                phone_number=phone
            )
            messages.success(request, "Registration successful. Please login.")
            return redirect('Author_login')
        except IntegrityError:
            messages.error(request, "An account with this email is already registered.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            
    return render(request, 'Author_Register_Page.html')

@login_required
def UserProfile(request):
    return render(request, 'admin/Profile.html', {'user': request.user})

@login_required
def UserSettings(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('Fname')
        request.user.last_name = request.POST.get('Lname')
        request.user.phone_number = request.POST.get('Phone_Number')
        request.user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('UserProfile')
    return render(request, 'admin/Settings.html', {'user': request.user})

def Author_ForgotPass(request):
    return render(request, 'Author_forgetpass_page.html')

# --- Admin/Staff Views ---

@login_required
def all_admin(request):
    return render(request, 'admin/AdminAllinclude.html')

@login_required
def Admin(request):
    total_online = models.OnlineBooking.objects.count()
    total_offline = models.OfflineBooking.objects.count()
    total_bookings = total_online + total_offline
    total_staff = models.Employee.objects.count()
    total_rooms = models.Room.objects.count()
    
    occupied_rooms = models.Room.objects.filter(status='Occupied').count()
    occupancy_rate = int((occupied_rooms / total_rooms * 100)) if total_rooms > 0 else 0
    
    recent_online = models.OnlineBooking.objects.all().order_by('-created_at')[:5]
    recent_offline = models.OfflineBooking.objects.all().order_by('-created_at')[:5]
    
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

@login_required
def Housekeeping(request):
    rooms = models.Room.objects.all().order_by('room_number')
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        new_status = request.POST.get('status')
        room = get_object_or_404(models.Room, id=room_id)
        room.status = new_status
        room.save()
        messages.success(request, f"Room {room.room_number} status updated to {new_status}")
        return redirect('Housekeeping')
    return render(request, 'admin/Housekeeping.html', {'rooms': rooms})

@login_required
def CheckIn(request, type, id):
    if type == 'online':
        booking = get_object_or_404(models.OnlineBooking, id=id)
        room = booking.room
    else:
        booking = get_object_or_404(models.OfflineBooking, id=id)
        room = booking.room
    
    booking.status = 'Checked In'
    booking.save()
    if room:
        room.status = 'Occupied'
        room.save()
        messages.success(request, f"Checked in to Room {room.room_number}")
    else:
        messages.warning(request, "No room assigned to this booking.")
        
    return redirect('Adminpage')

@login_required
def CheckOut(request, type, id):
    if type == 'online':
        booking = get_object_or_404(models.OnlineBooking, id=id)
        room = booking.room
    else:
        booking = get_object_or_404(models.OfflineBooking, id=id)
        room = booking.room
        
    booking.status = 'Checked Out'
    booking.save()
    if room:
        room.status = 'Dirty'
        room.save()
        messages.success(request, f"Checked out Room {room.room_number}")
    
    return redirect('Adminpage')

@login_required
def Maintenance(request):
    tickets = models.MaintenanceTicket.objects.all().order_by('-reported_at')
    rooms = models.Room.objects.all()
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        issue = request.POST.get('issue')
        priority = request.POST.get('priority')
        room = get_object_or_404(models.Room, id=room_id)
        
        ticket = models.MaintenanceTicket.objects.create(
            room=room, 
            issue=issue, 
            priority=priority
        )
        room.status = 'Maintenance'
        room.save()
        messages.warning(request, f"Room {room.room_number} sent to maintenance.")
        return redirect('Maintenance')
    return render(request, 'admin/Maintenance.html', {'tickets': tickets, 'rooms': rooms})

@login_required
def Billing(request, type, id):
    if type == 'online':
        booking = get_object_or_404(models.OnlineBooking, id=id)
        charges = models.GuestCharge.objects.filter(online_booking=booking)
        payments = models.GuestPayment.objects.filter(online_booking=booking)
    else:
        booking = get_object_or_404(models.OfflineBooking, id=id)
        charges = models.GuestCharge.objects.filter(offline_booking=booking)
        payments = models.GuestPayment.objects.filter(offline_booking=booking)
    
    total_charges = sum(c.amount for c in charges)
    total_payments = sum(p.amount_paid for p in payments)
    balance = total_charges - total_payments
    
    if request.method == 'POST':
        if 'add_charge' in request.POST:
            models.GuestCharge.objects.create(
                online_booking=booking if type == 'online' else None,
                offline_booking=booking if type == 'offline' else None,
                charge_type=request.POST.get('charge_type'),
                description=request.POST.get('description'),
                amount=request.POST.get('amount')
            )
        elif 'add_payment' in request.POST:
            models.GuestPayment.objects.create(
                online_booking=booking if type == 'online' else None,
                offline_booking=booking if type == 'offline' else None,
                amount_paid=request.POST.get('amount'),
                payment_method=request.POST.get('method'),
                receipt_number=request.POST.get('receipt')
            )
        return redirect('Billing', type=type, id=id)

    return render(request, 'admin/Billing.html', {
        'booking': booking, 'charges': charges, 'payments': payments,
        'total_charges': total_charges, 'total_payments': total_payments, 
        'balance': balance, 'type': type, 'id': id
    })

@login_required
def Reports(request):
    today = timezone.now().date()
    
    # 1. Arrivals & Departures
    arrivals_today = models.OnlineBooking.objects.filter(check_in=today).count() + \
                    models.OfflineBooking.objects.filter(check_in=today).count()
                    
    departures_today = models.OnlineBooking.objects.filter(check_out=today).count() + \
                      models.OfflineBooking.objects.filter(check_out=today).count()
    
    # 2. Occupancy Metrics
    total_rooms = models.Room.objects.count()
    occupied_rooms = models.Room.objects.filter(status='Occupied').count()
    dirty_rooms = models.Room.objects.filter(status='Dirty').count()
    maintenance_rooms = models.Room.objects.filter(status='Maintenance').count()
    available_rooms = models.Room.objects.filter(status='Available').count()
    
    occupancy_pct = int((occupied_rooms / total_rooms * 100)) if total_rooms > 0 else 0
    
    # 3. Revenue Reports
    payments_today = models.GuestPayment.objects.filter(created_at__date=today)
    total_revenue_today = sum(p.amount_paid for p in payments_today)
    
    mpesa_revenue = sum(p.amount_paid for p in payments_today.filter(payment_method='M-Pesa'))
    cash_revenue = sum(p.amount_paid for p in payments_today.filter(payment_method='Cash'))
    
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

@login_required
def Addemployee(request):
    if request.method == 'POST':
        form = forms.EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff member successfully added.")
            return redirect('Addemployee')
        else:
            messages.error(request, "Error adding staff. Please check the form.")

    data = models.Employee.objects.all().order_by('-employee_id')
    return render(request, 'admin/addemployee.html', {'data': data, 'form': forms.EmployeeForm()})

@login_required
def Editemployee(request, id):
    employee = get_object_or_404(models.Employee, employee_id=id)
    if request.method == 'POST':
        form = forms.EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee updated.")
            return redirect('Allemployee')
    else:
        form = forms.EmployeeForm(instance=employee)
    return render(request, 'admin/Editemployee.html', {'data': employee, 'form': form})

@login_required
def Allemployee(request):
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        data = models.Employee.objects.filter(
            Q(employee_id__icontains=search) | 
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        ).order_by('-employee_id')
    else:
        data = models.Employee.objects.all().order_by('-employee_id')
    return render(request, 'admin/allemployee.html', {'data': data})

@login_required
def online_Booking_info(request):
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        data = models.OnlineBooking.objects.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        ).order_by('-created_at')
    else:
        data = models.OnlineBooking.objects.all().order_by('-created_at')
    return render(request, 'admin/Online_Booking.html', {'data': data})

@login_required
def Edit_online_Booking(request, id):
    booking = get_object_or_404(models.OnlineBooking, id=id)
    if request.method == 'POST':
        form = forms.OnlineBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated.")
            return redirect('online_Booking_info')
    else:
        form = forms.OnlineBookingForm(instance=booking)
    return render(request, 'admin/EditonlineBooking.html', {'data': booking, 'form': form})

@login_required
def AddCustomer(request):
    if request.method == 'POST':
        form = forms.OfflineBookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer booking added.")
            return redirect('AddCustomer')

    data = models.OfflineBooking.objects.all().order_by('-created_at')
    return render(request, 'admin/AddCustomer.html', {'data': data, 'form': forms.OfflineBookingForm()})

@login_required
def AllCustomer(request):
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        data = models.OfflineBooking.objects.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        ).order_by('-created_at')
    else:
        data = models.OfflineBooking.objects.all().order_by('-created_at')
    return render(request, 'admin/AllCustomer.html', {'data': data})

@login_required
def EditCustomer(request, id):
    booking = get_object_or_404(models.OfflineBooking, id=id)
    if request.method == 'POST':
        form = forms.OfflineBookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated.")
            return redirect('AllCustomer')
    else:
        form = forms.OfflineBookingForm(instance=booking)
    return render(request, 'admin/EditCustomer.html', {'data': booking, 'form': form})

@login_required
def Delete(request, id):
    booking = get_object_or_404(models.OnlineBooking, id=id)
    booking.delete()
    messages.info(request, "Booking deleted.")
    return redirect('online_Booking_info')

@login_required
def Search(request):
    if request.method == 'POST':
        search = request.POST.get('serch', '').strip()
        data = models.OfflineBooking.objects.filter(
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        ).order_by('-created_at')
        return render(request, 'admin/AllCustomer.html', {"data": data})
    return redirect('AllCustomer')

@login_required
def AddCustpage_Delete(request, id):
    booking = get_object_or_404(models.OfflineBooking, id=id)
    booking.delete()
    return redirect('AddCustomer')

@login_required
def AllCustpage_Delete(request, id):
    booking = get_object_or_404(models.OfflineBooking, id=id)
    booking.delete()
    return redirect('AllCustomer')

@login_required
def AddEmplopage_Delete(request, id):
    employee = get_object_or_404(models.Employee, employee_id=id)
    employee.delete()
    return redirect('Addemployee')

@login_required
def Add_Employee_Search(request):
    if request.method == 'POST':
        search = request.POST.get('serch', '').strip()
        data = models.Employee.objects.filter(
            Q(employee_id__icontains=search) | 
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        ).order_by('-employee_id')
        return render(request, 'admin/addemployee.html', {"data": data})
    return redirect('Addemployee')

@login_required
def AllEmployee_Delete(request, id):
    employee = get_object_or_404(models.Employee, employee_id=id)
    employee.delete()
    return redirect('Allemployee')

@login_required
def Add_room(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Room added.")
            return redirect('Add_room')
    data = models.Room.objects.all().order_by('room_number')
    return render(request, 'admin/AddRoom.html', {'data': data, 'form': forms.RoomForm()})

@login_required
def Add_Room_Search(request):
    if request.method == 'POST':
        search = request.POST.get('serch', '').strip()
        data = models.Room.objects.filter(room_number__icontains=search).order_by('room_number')
        return render(request, 'admin/AddRoom.html', {"data": data})
    return redirect('Add_room')

@login_required
def AddRooms_Delete(request, id):
    room = get_object_or_404(models.Room, id=id)
    room.delete()
    return redirect('Add_room')

@login_required
def EditRooms(request, id):
    room = get_object_or_404(models.Room, id=id)
    if request.method == 'POST':
        form = forms.RoomForm(request.POST, request.FILES, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated.")
            return redirect('All_Room')
    else:
        form = forms.RoomForm(instance=room)
    return render(request, 'admin/EditRooms.html', {'data': room, 'form': form})

@login_required
def All_Room(request):
    if request.method == 'POST':
        search = request.POST.get('search', '').strip()
        data = models.Room.objects.filter(
            Q(room_number__icontains=search) | 
            Q(room_type__icontains=search)
        ).order_by('room_number')
    else:
        data = models.Room.objects.all().order_by('room_number')
    return render(request, 'admin/AllRooms.html', {'data': data})

@login_required
def AllRooms_Delete(request, id):
    room = get_object_or_404(models.Room, id=id)
    room.delete()
    return redirect('All_Room')

@login_required
def AddEmployeeSalary(request):
    if request.method == 'POST':
        form = forms.EmployeeSalaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Salary record added.")
            return redirect('AddEmployeeSalary')
    employees = models.Employee.objects.all()
    return render(request, 'admin/AddEmployeeSalary.html', {'employees': employees})

@login_required
def EmployeeShow(request):
    return render(request, 'admin/EmployeeShow.html')
