# Hotel Grand View (Django)

A full-stack (server-rendered) Django web application for managing a hotel website with user authentication, reservations/room booking, multi-provider payments (Stripe, PayPal, Razorpay), COD option, booking confirmation, invoice PDF generation, WhatsApp notifications (Twilio), membership plans, career applications, and user “My Bookings”.

---

## Features

### Public website pages
- **Home**, **About**, **Rooms**, **Amenities**, **Gallery**
- **Contact** form with success message feedback
- **Dining** reservation flow (simple UI endpoint)
- **Check availability** endpoint (returns room availability page/content)

### Authentication
- **Register**
- **Login**
- **Logout**

### Booking & Confirmation
- **Booking page** (`/booking/`) accepts room details via query parameters and collects guest details via POST.
- Calculates:
  - nights (based on check-in/out)
  - number of rooms required (2 guests per room)
  - taxes (18% of total)
  - grand total
- **Booking confirmation page** (`/booking_successful/`) creates a `Booking_Successful` record using query parameters.
- Sends notifications:
  - **Email** confirmation with an attached **invoice PDF**
  - **WhatsApp** message via **Twilio**

### Payments
Payment-related endpoints provided:
- **Stripe Checkout session**: `/create-stripe-session/`
- **PayPal payment creation**: `/create-paypal-payment/`
- **Razorpay order creation**: `/create_razorpay_order/`
- **Cash on Delivery (COD)**: `/cod-payment/`

### Invoice PDF
- Generates PDF using:
  - `pdfkit` to convert HTML template (`templates/invoice_pdf.html`) into PDF
  - `wkhtmltopdf` binary (configured via an absolute path in `home/views.py`)
- **Download invoice PDF**: `/invoice/download/`

### Membership
- Membership request workflow:
  - `/membership_page/`
  - `/membership_details/`
  - `/membership_confirmation/` (creates `Membership_Confirmation`)
  - `/membership_payment_page/`

### Career
- Job listing page: `/career/`
- Career application form submission: `/submit_application/` (creates `CareerApplication`)

### User bookings
- User-specific booking history:
  - `/mybookings/` (shows `Booking_Successful` for the logged-in user)

---

## Tech Stack

- **Python 3.x**
- **Django** (server-side rendered pages)
- **SQLite** (default DB)
- **Stripe** (Checkout session creation)
- **PayPal** (payment creation)
- **Razorpay** (order creation)
- **Twilio** (WhatsApp message sending)
- **pdfkit + wkhtmltopdf** (invoice PDF generation)
- **SMTP EmailBackend** (Gmail configured in settings)

---

## Project Structure

- `manage.py` – Django entry point
- `hotel/` – Project settings and URL routing
  - `hotel/settings.py` – configuration (DB, templates, payment keys, email, Twilio, etc.)
  - `hotel/urls.py` – includes app URLs
- `home/` – Main application
  - `home/views.py` – all view/controller logic
  - `home/urls.py` – URL routes
  - `home/models.py` – data models
  - `home/migrations/` – migrations history
- `templates/` – HTML templates
- `static/` – static assets

---

## Prerequisites

1. **Python** installed
2. **wkhtmltopdf** installed (required for PDF generation)
   - `home/views.py` currently references:
     - `C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe`
3. Credentials for the integrations you plan to enable:
   - Stripe
   - PayPal
   - Razorpay
   - Twilio (WhatsApp)
   - SMTP email (Gmail/your provider)

---

## Setup & Run Locally

### 1) Create/activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment / secrets

This project currently contains integration keys in `hotel/settings.py`.

**Recommended:** Move secrets to environment variables and update settings accordingly.

Minimum you must ensure are set (or present in settings) for the features you use:
- `STRIPE_SECRET_KEY`, `STRIPE_PUBLIC_KEY`
- `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_MODE`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_NUMBER`
- SMTP email:
  - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`
- Razorpay keys:
  - `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`

> Note: `home/models.py` includes `os.getenv(...)` for some keys, but the runtime code in `home/views.py` uses values from `django.conf.settings`. Ensure the keys used by views are correctly configured.

### 4) Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5) Create an admin user

```bash
python manage.py createsuperuser
```

### 6) Run the development server

```bash
python manage.py runserver
```

Open: `http://127.0.0.1:8000/`

---

## Admin Panel

After creating a superuser, visit:
- `http://127.0.0.1:8000/admin/`

Register models via `home/admin.py` (if not already configured, update `home/admin.py` to manage models like bookings, feedback, career applications, and membership confirmations).

---

## URL Reference (Main Routes)

All routes are registered in `home/urls.py` and included from `hotel/urls.py`.

### Public pages
- `/` → `index`
- `/about/` → `about`
- `/contact/` → `contact`
- `/rooms/` → `rooms`
- `/book/` → `book`
- `/amenities/` → `amenities`
- `/Dining/` → `Dining`
- `/gallery/` → `gallery`
- `/career/` → `career`
- `/check_availability/` → `check_availability`

### Auth
- `/login/` → `login_view`
- `/register/` → `register_view`
- `/logout/` → `logout_view`

### Booking
- `/booking/` → `booking` (requires login)
- `/booking_successful/` → `booking_successful`
- `/mybookings/` → `my_bookings` (requires login)

### Payments
- `/payment_page/` → `payment_page`
- `/create-stripe-session/` → `create_stripe_session`
- `/create-paypal-payment/` → `create_paypal_payment`
- `/create_razorpay_order/` → `create_razorpay_order`
- `/cod-payment/` → `cod_payment`
- `/payment_success/` → `payment_success`
- `/payment_cancel/` → `payment_cancel` (placeholder)

### Invoice
- `/invoice/download/` → `download_invoice`

### Membership
- `/membership_page/` → `membership_page`
- `/membership_details/` → `membership_details`
- `/membership_confirmation/` → `membership_confirmation`
- `/membership_payment_page/` → `membership_payment_page`

### Career applications
- `/submit_application/` → `submit_application`

---

## Data Models (Overview)

Defined in `home/models.py`:

- **Booking_Successful**
  - Customer + booking details (name, email, phone, room, dates, guests, amounts)
  - Invoice storage: `invoice_pdf` (`FileField`)
  - Payment metadata: `payment_status`
  - Links to Django `User`

- **Feedback**
  - `rating`, `feedback`, `created_at`

- **CareerApplication**
  - `name`, `email`, `phone`, uploaded `resume`, `cover_letter`, `applied_at`

- **Membership_Confirmation**
  - Customer details + plan info + `grand_total`

(Additional models exist but are not fully wired in the current flow; core flow relies on `Booking_Successful`, `CareerApplication`, and `Membership_Confirmation`.)

---

## Payment Flow Notes

1. Booking UI computes pricing (tax = 18%).
2. Payment endpoints generate checkout/order/payment objects.
3. After successful payment, the app renders **`payment_success.html`** and stores invoice data in the session.
4. On/after confirmation, **`booking_successful`** creates a persistent booking record, sends email + WhatsApp, and renders `booking_successful.html`.

> If you enable payment webhooks later, ensure you verify payment status server-side rather than relying only on client redirects.

---

## Invoice PDF Generation

- Uses `templates/invoice_pdf.html`.
- Uses `pdfkit.from_string(...)` with a `wkhtmltopdf` path.

### Common issues
- **wkhtmltopdf not found** → install `wkhtmltopdf` and update the path in `home/views.py`.
- **PDF generation fails** → ensure template renders correctly and required session data exists.

---

## Troubleshooting

### 1) Email sending fails
- Confirm SMTP credentials in `hotel/settings.py`.
- Gmail often requires App Passwords.

### 2) Twilio WhatsApp fails
- Confirm Twilio credentials and that the WhatsApp-enabled sender number is correctly configured.
- Verify the destination `phone` formatting.

### 3) Payment failures
- Ensure Stripe/PayPal/Razorpay keys are valid and you are using the correct sandbox/live settings.
- Stripe success/cancel URLs are currently hard-coded to `http://127.0.0.1:8000/...`.

---

## Security & Production Notes

- `DEBUG = True` and API keys are present in code. For production:
  - set `DEBUG = False`
  - rotate exposed secrets
  - move all secrets to environment variables
- Add HTTPS and secure cookie/session settings.
- Prefer server-side payment verification (webhooks).

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

## Acknowledgements

Built using Django and integrated with payment/notification providers (Stripe, PayPal, Razorpay, Twilio) and PDF generation (`wkhtmltopdf`).

