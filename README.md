# Kivulini Safari Lodge & Resort - Professional PMS

A modern, integrated Property Management System (PMS) tailored for boutique hotels and resorts. Built with a focus on HCI (Human-Computer Interaction), responsiveness, and professional operational workflows.

## Core Modules
- **Reservations**: Smart availability tracking and dual online/walk-in booking engines.
- **Front Desk**: Integrated Check-In/Check-Out with automated room status sync.
- **Housekeeping**: Live room status management (Vacant, Occupied, Dirty, Maintenance).
- **Operations**: Staff directory, HR management, and payroll records.
- **Analytics**: Real-time dashboard with property KPIs and occupancy metrics.
- **Maintenance**: Ticketing system for facility repairs.

## Technical Summary
- **Backend Architecture**: High-performance request processing.
- **Frontend Architecture**: Modern utility-first responsive design.
- **Interactivity Engine**: Lightweight reactive components.
- **Persistence Layer**: Robust relational storage.
## Localization (Kenya)

The project has been specifically tailored for the Kenyan market:
- **Timezone**: Set to `Africa/Nairobi`.
- **Currency**: Prices are handled in Kenyan Shillings (Ksh).
- **Contact Information**: Localized addresses and phone numbers (+254).
- **Country Options**: Default country options include Kenya.

## Technology Stack

- **Backend**: Django (Python)
- **Database**: SQLite3 (Default)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Image Processing**: Pillow

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Django_practice_Pro_hotel_management_system-main
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a Superuser** (Optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://127.0.0.1:8000/`.

## Usage

- Access the homepage to view general information.
- Use the `/OnlineBooking` URL for customer bookings.
- Use the `/Author_login` URL to access the admin dashboard.

## Credits

YouTube Video Link: [Hotel Management System Demo](https://youtu.be/AnyOmDWZZ9A)
