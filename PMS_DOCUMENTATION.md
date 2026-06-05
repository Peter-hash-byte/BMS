# Kivulini Safari Lodge & Resort - PMS Documentation

## 1. Project Overview
**Kivulini Safari Lodge & Resort Property Management System (PMS)** is a professional, high-performance administrative suite designed to manage the end-to-end guest lifecycle. Built on Django with a modern Tailwind CSS and Alpine.js frontend, the system prioritizes HCI (Human-Computer Interaction) standards, operational efficiency, and a refined "Premium Resort" aesthetic.

---

## 2. Core Modules & Functionality

### 2.1 Reservations & Front Desk
*   **Online Booking Engine:** A responsive guest-facing portal for direct reservations.
*   **Walk-in (Offline) Management:** Receptionist interface for manual guest registration.
*   **Smart Check-In/Out:** Automated workflows that transition room states between `Reserved`, `Occupied`, and `Dirty`.
*   **Availability Guard:** Backend logic prevents double-bookings and respects maintenance blocks.

### 2.2 Room & Housekeeping Management
*   **Room Inventory:** Real-time tracking of room types, rates, and facilities.
*   **Status Lifecycle:** Professional room states: `Available` → `Reserved` → `Occupied` → `Dirty` → `Cleaning` → `Available`.
*   **Housekeeping Dashboard:** Dedicated module for cleaning staff to update room readiness and report facility issues.

### 2.3 Financial Management (Manual Model)
*   **Guest Folio:** Ability to post diverse charges (Room, Restaurant, Laundry, etc.) to a guest's account.
*   **Manual Payment Recording:** Supports recording of physical payments via M-Pesa, Cash, Card, or Bank Transfer.
*   **Settlement Tracking:** Real-time balance calculation for transparent guest check-outs.

### 2.4 Maintenance & Operations
*   **Maintenance Ticketing:** Staff can report room issues; tickets automatically block rooms from the booking engine.
*   **Staff HR & Payroll:** Management of employee profiles, departments, and historical salary records.
*   **Operational Reports:** High-level dashboard and detailed reports for:
    *   Daily Revenue (categorized by payment method).
    *   Occupancy Percentage.
    *   Arrivals/Departures Traffic.
    *   Inventory Status breakdown.

---

## 3. Technology Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Django (Python 3.13) |
| **Frontend Styling** | Tailwind CSS & DaisyUI |
| **Interactivity** | Alpine.js |
| **Database** | SQLite3 |
| **Animations** | Textillate.js (Hero Typography), Slick Slider (Hero & Gallery) |
| **Date Handling** | Modern HTML5 Date Pickers |

---

## 4. Role-Based Access Control (RBAC)
Access to system modules is strictly controlled based on staff roles:

*   **Administrator / Manager:** Full system access (HR, Payroll, Reports, Room Setup).
*   **Receptionist:** Access to Front Desk, Reservations, Billing, and Room Inventory.
*   **Housekeeper:** Access to Housekeeping status management and Maintenance reporting.

---

## 5. Security & HCI Features

*   **Security through Obscurity:** All technical framework versions and environment details are stripped from headers and public templates.
*   **Graceful Error Handling:** Database constraints (e.g., duplicate emails) are handled via friendly user alerts rather than technical error pages.
*   **HCI Principles:**
    *   **Reduced Friction:** Document upload requirements removed from booking.
    *   **Visibility:** High-contrast palette (Amber/Slate) for statistics and primary actions.
    *   **Accessibility:** Sticky headers for persistent navigation across long pages.
    *   **Optimized Input:** Numeric-only fields for IDs and Phones to improve entry speed.

---

## 6. Installation & Deployment

### Prerequisites
*   Python 3.13+
*   Node.js & npm (for Tailwind builds)

### Setup Steps
1.  **Clone & Venv:**
    ```bash
    git clone <repo-url>
    python -m venv venv
    source venv/bin/activate
    ```
2.  **Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Tailwind Initialization:**
    ```bash
    python manage.py tailwind install
    python manage.py tailwind build
    ```
4.  **Database:**
    ```bash
    python manage.py migrate
    ```

---

## 7. Operational Workflow (Standard)

1.  **Guest Reservation:** Guest selects dates and room via homepage or online portal.
2.  **Confirmation:** Receptionist confirms details; room status moves to `Reserved`.
3.  **Check-In:** Receptionist assigns room; status moves to `Occupied`. Folio is opened.
4.  **Stay:** Staff posts additional charges (Meal, Laundry) to the Guest Folio.
5.  **Manual Payment:** Reception collects funds at front desk and records payment method/receipt in system.
6.  **Check-Out:** Receptionist verifies zero balance; guest status moves to `Checked Out`. Room moves to `Dirty`.
7.  **Turnaround:** Housekeeper cleans room and marks it `Available` in the Housekeeping module.
