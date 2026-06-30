# Trio Self Drive

A complete, production-quality Django web application for a self-drive car rental business.
Customers can browse cars, submit booking requests without creating an account, and track their
booking status. The business owner manages everything — cars, bookings, customers, and reports —
through a custom-built staff dashboard (not the default Django admin).

**Business:** Self Drive Car Rental
**Phone:** 9392798251

---

## Features

### Public Website
- **Home** — Hero banner, featured cars, "Why Choose Us", "How It Works", testimonials, FAQ preview, and a call-to-action banner.
- **Cars** — Searchable, filterable (fuel type, transmission), sortable (price), paginated car listing.
- **Car Details** — Full specifications, description, related cars from the same brand, and a "Book Now" call-to-action.
- **Book a Car** — A no-account-required booking form (name, phone, optional email, driving license upload, pickup/return date & time) with a live, JavaScript-powered price estimator.
- **My Bookings** — Customers search their bookings using just their phone number, view status, and cancel a booking while it's still pending.
- **About** — Company story, stats, and mission.
- **Contact** — A contact form that stores messages in the database.
- **FAQ** — Frequently asked questions in an accordion layout.
- **Floating WhatsApp Button** — Always-visible button linking directly to a pre-filled WhatsApp chat.
- Fully responsive, premium **Blue & White** Bootstrap 5 design with smooth hover effects and Bootstrap Icons.

### Booking Logic
- No customer accounts — bookings are tracked purely by phone number.
- **Automatic double-booking prevention**: if a new booking's date/time range overlaps with any existing pending or approved booking for the same car, the booking is rejected with a clear error message.
- **Automatic price calculation**: total rental days and total price are calculated automatically from the pickup and return date/time (any part of a day beyond a full 24-hour block counts as an additional day).
- Booking statuses: Pending → Approved / Rejected, plus Cancelled (by customer) and Completed (by staff).
- No online payment — payment is handled directly between the customer and the business.

### Custom Staff Dashboard (NOT Django Admin)
Accessible at `/dashboard/`, protected by Django's authentication system.

- **Statistics** — Total cars, available cars, total bookings, pending/approved/rejected/cancelled bookings, today's bookings.
- **Car Management** — Add, edit, and delete cars (brand, name, model, price/day, fuel type, transmission, seats, mileage, description, image, availability toggle).
- **Booking Management** — Search/filter bookings by status, view full details, approve or reject pending bookings (with an optional note), mark approved bookings as completed, or delete a booking. The dashboard re-checks for double bookings before allowing an approval.
- **Customer List** — Aggregated view of every customer who has booked, with booking counts by status. Click through to see a customer's full booking history.
- **Reports** — Total and monthly revenue, bookings grouped by status, and the most-booked cars.

The default Django admin (`/admin/`) is still available for low-level data management (e.g. managing FAQs, testimonials, and contact messages), but it is not used as the primary business dashboard.

---

## Technology Stack

- Python 3.13+ (tested with 3.12, fully compatible with 3.13)
- Django 5.x
- SQLite (default database, zero configuration)
- Bootstrap 5 (via CDN) + Bootstrap Icons
- Vanilla HTML, CSS, and JavaScript (no frontend frameworks, no Tailwind, no Django REST Framework)
- Pillow (for image uploads and processing)

---

## Project Structure

```
trio_self_drive/
├── config/                 # Project configuration (settings, root urls, wsgi/asgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── core/                   # Public pages: home, about, contact, FAQ
│   ├── models.py           # ContactMessage, FAQ, Testimonial
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── context_processors.py
│   └── management/commands/seed_data.py   # Sample data seeder
├── cars/                   # Car catalog
│   ├── models.py           # Car
│   ├── views.py            # Public listing & detail views
│   ├── forms.py            # CarForm used by the dashboard
│   ├── urls.py
│   └── admin.py
├── bookings/                # Booking system
│   ├── models.py            # Booking (with overlap detection & price calculation)
│   ├── views.py              # Book, success, search, status, cancel
│   ├── forms.py               # BookingForm, BookingSearchForm
│   ├── urls.py
│   └── admin.py
├── dashboard/                # Custom staff dashboard
│   ├── views.py               # Auth, stats, car/booking/customer management, reports
│   ├── forms.py                # Login form, booking decision form
│   └── urls.py
├── templates/
│   ├── base.html               # Public site base template
│   ├── partials/                # navbar, footer, messages, WhatsApp button
│   ├── core/                     # home, about, contact, faq
│   ├── cars/                      # car_list, car_detail
│   ├── bookings/                   # book_car, booking_success, booking_search, booking_status, booking_cancel_confirm
│   └── dashboard/                   # base_dashboard, login, dashboard_home, car_*, booking_*, customer_*, reports
├── static/
│   ├── css/style.css                # Main site stylesheet (design tokens, components)
│   ├── css/dashboard.css             # Dashboard-specific stylesheet (sidebar, stat cards)
│   ├── js/main.js                     # Public site JavaScript
│   └── js/dashboard.js                 # Dashboard JavaScript
├── media/                                # Uploaded car images & driving licenses (created at runtime)
├── manage.py
├── requirements.txt
└── README.md
```

---

## Installation Instructions

### 1. Prerequisites
- Python 3.13+ installed (3.10+ will also work)
- pip (Python package manager)

### 2. Clone / extract the project
Place the project folder anywhere on your machine, then open a terminal inside it (the folder containing `manage.py`).

### 3. Create a virtual environment (recommended)

```bash
python3 -m venv venv

# Activate it:
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. (Optional but recommended) Seed sample data

This creates 10 sample cars, 8 FAQs, 6 testimonials, and a default admin user so you can explore
the site immediately:

```bash
python manage.py seed_data
```

This will print the admin credentials, which are also documented below.

Alternatively, create your own admin user manually:

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

### 8. Open the application
- **Public website:** http://127.0.0.1:8000/
- **Staff dashboard:** http://127.0.0.1:8000/dashboard/login/
- **Django admin (optional, low-level data tools):** http://127.0.0.1:8000/admin/

---

## Default Login (after running `seed_data`)

| Field    | Value             |
|----------|-------------------|
| Username | `admin`           |
| Password | `TrioAdmin@123`   |

**Important:** Change this password immediately in a real deployment, e.g. via `python manage.py changepassword admin`.

---

## Configuring the Business Phone Number / WhatsApp

All business contact details are centralized in `config/settings.py`:

```python
BUSINESS_PHONE = '9392798251'
BUSINESS_PHONE_DISPLAY = '+91 93927 98251'
WHATSAPP_NUMBER = '919392798251'   # Country code + number, no symbols
BUSINESS_EMAIL = 'info@trioselfdrive.com'
BUSINESS_ADDRESS = 'Trio Self Drive, Main Road, Telangana, India'
```

These values are injected into every template automatically via a context processor
(`core/context_processors.py`), so updating them here updates the entire site, including the
floating WhatsApp button, navbar phone link, and footer.

---

## How Booking Validation Works

1. A customer fills out the booking form on a car's "Book Now" page (no login required).
2. On submission, `BookingForm.clean()` checks the requested pickup/return range against every
   **pending** or **approved** booking that already exists for that same car.
3. If any existing booking's range overlaps with the new request, the form is rejected with the
   message: *"This car is already booked for an overlapping time period."*
4. If valid, the `Booking` model's `save()` method automatically computes `total_days` (rounding
   any partial day up to a full day) and `total_price` (`total_days × car.price_per_day`).
5. The booking is created with status **Pending**. Staff must approve it from the dashboard before
   it is considered confirmed. The dashboard re-validates for overlaps at approval time as a safety net.

---

## Notes on Image Uploads

- Car images and driving license uploads are handled via Pillow and Django's `ImageField`.
- Uploaded files are stored under `media/cars/` and `media/licenses/` respectively.
- Maximum upload size is 5 MB (configurable via `MAX_UPLOAD_SIZE` in `config/settings.py`).
- In development, Django serves these files directly. In production, configure your web server
  (e.g. Nginx) to serve the `MEDIA_ROOT` directory, or use a cloud storage backend.

---

## Production Deployment Checklist

This project ships with development-friendly defaults. Before deploying to production:

1. Set `DEBUG = False` in `config/settings.py`.
2. Set a strong, unique `SECRET_KEY` (ideally loaded from an environment variable).
3. Set `ALLOWED_HOSTS` to your actual domain(s).
4. Run `python manage.py collectstatic` and serve the `staticfiles/` directory via your web server.
5. Configure your web server to serve `media/` files, or move to a cloud storage backend such as Amazon S3.
6. Use a production-grade WSGI server such as Gunicorn behind Nginx (the built-in `runserver` is
   for development only).
7. Consider switching from SQLite to PostgreSQL for higher-concurrency production workloads
   (SQLite works well for small to medium traffic).
8. Change the default admin password immediately.

---

## License

This project was built as a custom business solution for Trio Self Drive. All rights reserved.
