from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views import View
from django.contrib import messages
from requests import request
import stripe
import paypalrestsdk
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def index(request):

    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Process the form data (e.g., save to database or send an email)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Add a success message
        messages.success(request, 'Your message has been sent successfully!, We will contact you shortly.')

        # Redirect to the same page to clear the form
        return redirect('contact')  # Replace 'contact' with the name of your URL pattern

    return render(request, 'contact.html')

def rooms(request):
    return render(request, 'rooms.html')

def book(request):
    return render(request, 'book.html')

def amenities(request):
    return render(request, 'amenities.html')

def Dining(request):
    return render(request, 'Dining.html')


def login_view(request):
    if request.method == "POST":

        # Get the username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # If the user is authenticated, redirect to the home page
            login(request,user)
            return redirect('/')
        else:
            # If authentication fails, show an error message
            return render(request, 'signin.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('name')  # Full Name
        email = request.POST.get('email')  # Email Address
        password = request.POST.get('password')  # Password

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different username.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please use a different email.')
            return render(request, 'register.html')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Show success message and redirect to the signin page
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')  # Redirect to the signin page
    else:
        return render(request, 'register.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to home page after logout

def reserve_table(request):
    if request.method == 'POST':
        # Process the form data here
        # Example: Save the reservation to the database
        context = {
            'reservation_success': True,  # Flag to indicate success
        }
        return render(request, 'Dining.html', context)
    return render(request, 'Dining.html')

from django.shortcuts import render, redirect

@login_required
def booking(request):
    # Get room details from query parameters
    room_name = request.GET.get('room_name', 'Unknown Room')
    room_rate = request.GET.get('room_rate', '0')  # Default to '0' if not provided

    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        guests = request.POST.get('guests')
        rooms_required = request.POST.get('rooms_required')
        special_requests = request.POST.get('special_requests')

        # Calculate the total amount
        from datetime import datetime
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
        nights = (checkout_date - checkin_date).days
        total_amount = nights * float(room_rate) * int(rooms_required)
        # Calculate rooms required
        max_guests_per_room = 2
        rooms_required = ceil(int(guests) / max_guests_per_room)
        taxes = total_amount * 0.18  # 10% tax
        grand_total = total_amount + taxes

        # Save booking to the database
        # from .models import Booking
        # Booking.objects.create(
        #     user=request.user,
        #     room_name=room_name,
        #     checkin=checkin_date,
        #     checkout=checkout_date,
        #     guests=guests,
        #     rooms_required=rooms_required,
        #     total_amount=grand_total
        # )

        # Redirect to a confirmation page or process the booking
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'checkin': checkin,
            'checkout': checkout,
            'guests': guests,
            'special_requests': special_requests,
            'room_name': room_name,
            'room_rate': room_rate,
            'rooms_required': rooms_required,
            'nights': nights,
            'total_amount': total_amount,
            'taxes': taxes,
            'grand_total': grand_total,
        }
        return render(request, 'confirmation.html', context)

    # Render the booking page
    context = {
        'room_name': room_name,
        'room_rate': room_rate,
    }
    return render(request, 'booking.html', context)

from math import ceil  # Import ceil to round up the number of rooms

from math import ceil  # Import ceil to round up the number of rooms

from math import ceil  # Import ceil to round up the number of rooms

from math import ceil

def confirmation(request):
    if request.method == 'POST':
        # Retrieve form data
        guests = int(request.POST.get('guests', 0))  # Ensure guests is an integer
        room_rate = float(request.POST.get('room_rate', 0))  # Ensure room_rate is a float
        nights = int(request.POST.get('nights', 0))  # Ensure nights is an integer
        rooms_required = int(request.POST.get('rooms_required',0))
        phone = request.POST.get('phone', 'Unknown Phone')  # Retrieve phone from POST request
        # Calculate rooms required
        max_guests_per_room = 2
        rooms_required = ceil(guests / max_guests_per_room)

    
        # Calculate total amount, taxes, and grand total
        total_amount = room_rate * nights * rooms_required
        taxes = total_amount * 0.18  # 18% tax
        grand_total = total_amount + taxes

        # Pass data to the template
        context = {
            'name':request.POST.get('name', 'Unknown Room'),    
            'room_name': request.POST.get('room_name', 'Unknown Room'),
            'room_rate': room_rate,
            'checkin': request.POST.get('checkin', 'N/A'),
            'checkout': request.POST.get('checkout', 'N/A'),
            'nights': nights,
            'guests': guests,
            'phone': phone,
            'rooms_required': rooms_required,
            'special_requests': request.POST.get('special_requests', 'None'),
            'total_amount': total_amount,
            'taxes': taxes,
            'grand_total': grand_total,
        }
        return render(request, 'confirmation.html', context)
    return redirect('booking')  # Redirect to booking page if not POST



stripe.api_key = settings.STRIPE_SECRET_KEY

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})
def create_stripe_session(request):
    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            # Parse the JSON body
            import json
            data = json.loads(request.body)

            # Debug the received data
            print("Received Data:", data)

            room_name = data.get('room_name', 'Hotel Booking')
            total_amount = data.get('total_amount', 0)

            # Debug the total amount
            print("Total Amount:", total_amount)

            # Create Stripe Checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': room_name,
                            },
                            'unit_amount': int(float(total_amount) * 100),  # Convert to cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://127.0.0.1:8000/payment-success/',
                cancel_url='http://127.0.0.1:8000/payment-cancel/',
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            print("Stripe Error:", str(e))
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def create_paypal_payment(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            import json
            data = json.loads(request.body)

            # Debug the received data
            print("Received Data:", data)

            total_amount = data.get('total_amount', 0)

            # Debug the total amount
            print("Total Amount:", total_amount)

            # Create a PayPal payment
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal",
                },
                "redirect_urls": {
                    "return_url": "http://127.0.0.1:8000/payment-success/",
                    "cancel_url": "http://127.0.0.1:8000/payment-cancel/",
                },
                "transactions": [
                    {
                        "amount": {
                            "total": f"{total_amount}",
                            "currency": "USD",
                        },
                        "description": "Hotel Booking Payment",
                    }
                ],
            })

            # Handle payment creation
            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        print("Approval URL:", link.href)  # Debug the approval URL
                        return JsonResponse({'approval_url': link.href})
            else:
                # Log the error for debugging
                print("PayPal Payment Error:", payment.error)
                return JsonResponse({'error': payment.error}, status=400)
        except Exception as e:
            print("PayPal Error:", str(e))
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def cod_payment(request):
    # Handle Cash on Delivery (COD)
    return render(request, 'payment_success.html', {'message': 'Your booking has been confirmed with Cash on Delivery (COD).'})



def payment_page(request):
    # Retrieve booking details from query parameters with proper defaults
    name = request.GET.get('name', 'Unknown Name')
    email = request.GET.get('email', 'Unknown email')
    phone = request.GET.get('phone', 'Unknown phone')
    room_name = request.GET.get('room_name', 'Unknown Room')
    room_rate = float(request.GET.get('room_rate', 0) or 0)  # Default to 0 if empty
    checkin = request.GET.get('checkin', 'N/A')
    checkout = request.GET.get('checkout', 'N/A')
    nights = int(request.GET.get('nights', 0) or 0)  # Default to 0 if empty
    guests = request.GET.get('guests', 'N/A')
    rooms_required = int(request.GET.get('rooms_required', 0) or 0)  # Default to 0 if empty
    total_amount = float(request.GET.get('total_amount', 0) or 0)  # Default to 0 if empty
    taxes = float(request.GET.get('taxes', 0) or 0)  # Default to 0 if empty
    grand_total = float(request.GET.get('grand_total', 0) or 0)  # Default to 0 if empty

    # Debug the grand total
    print("Grand Total:", grand_total)

    # Pass the details to the payment page
    context = {
        'name': name,
        'email': email,
        'phone': phone,
        'room_name': room_name,
        'room_rate': room_rate,
        'checkin': checkin,
        'checkout': checkout,
        'nights': nights,
        'guests': guests,
        'rooms_required': rooms_required,
        'total_amount': total_amount,
        'taxes': taxes,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'payment_page.html', context)


def payment_cancel(request):
    # Your payment cancel logic here
    pass 

import razorpay
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

def create_razorpay_order(request):
    if request.method == 'POST':
        total_amount = float(request.POST.get('total_amount', 0)) * 100  # Convert to paise (INR)
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Create a Razorpay order
            order = client.order.create({
                "amount": int(total_amount),  # Amount in paise
                "currency": "INR",
                "payment_capture": 1,  # Auto-capture payment
            })
            return JsonResponse({'order_id': order['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)


from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import redirect
from django.contrib import messages

# def submit_feedback(request):
#     if request.method == 'POST':
#         rating = request.POST.get('rating')
#         feedback = request.POST.get('feedback')

#         # from .models import Feedback
#         # Feedback.objects.create(
#         #     rating=rating,
#         #     content=feedback
#         # )
#         if feedback and rating:
#             # Save feedback and rating to the database or send it via email
#             # Example: Feedback.objects.create(rating=rating, content=feedback)
#             messages.success(request, 'Thank you for your feedback!')
#         else:
#             messages.error(request, 'Please provide both a rating and feedback.')
#         return redirect('booking_successful')
        


from twilio.rest import Client
from django.conf import settings
from django.shortcuts import render

def payment_success(request):
    # Get all required fields from POST (or use GET if you use GET requests)
    name = request.POST.get('name', 'Unknown Name')
    phone = request.POST.get('phone', 'Unknown Phone')
    checkin = request.POST.get('checkin', 'N/A')
    checkout = request.POST.get('checkout', 'N/A')
    room_name = request.POST.get('room_name', 'Deluxe Room')
    room_rate = request.POST.get('room_rate', '100')
    nights = request.POST.get('nights', '2')
    guests = request.POST.get('guests', '4')
    rooms_required = request.POST.get('rooms_required', '2')
    total_amount = request.POST.get('total_amount', '400')
    taxes = request.POST.get('taxes', '72')
    grand_total = request.POST.get('grand_total', '472')
    user_phone = request.POST.get('phone', '+1234567890')  # WhatsApp number

    # Twilio client setup
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Message content
    message_body = (
        f"Thank you for your booking!\n\n"
        f"Room: {room_name}\n"
        f"Rate: ${room_rate} / night\n"
        f"Nights: {nights}\n"
        f"Guests: {guests}\n"
        f"Rooms Required: {rooms_required}\n"
        f"Total Amount: ${total_amount}\n"
        f"Taxes: ${taxes}\n"
        f"Grand Total: ${grand_total}\n\n"
        f"We look forward to hosting you!"
    )

    try:
        # Send WhatsApp message
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f"whatsapp:{user_phone}"
        )
        print(f"WhatsApp message sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return render(request, 'payment_success.html', {'message': 'Your payment was successful!'})

    # Store all invoice data in session
    invoice_data = {
        'name': name,
        'phone': phone,
        'room_name': room_name,
        'room_rate': room_rate,
        'checkin': checkin,
        'checkout': checkout,
        'nights': nights,
        'guests': guests,
        'rooms_required': rooms_required,
        'total_amount': total_amount,
        'taxes': taxes,
        'grand_total': grand_total,
        # Add these two lines:
        'invoice_no': generate_invoice_no(),
        'invoice_date': datetime.now().strftime('%d-%m-%Y'),
    }
    request.session['invoice_data'] = invoice_data
    return render(request, 'payment_success.html', invoice_data)
                                                                        



from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render


def booking_successful(request):
    # Validate checkin and checkout dates
    # checkin = request.GET.get('checkin', 'N/A')
    # checkout = request.GET.get('checkout', 'N/A')

    # Parse dates and handle invalid formats
    # try:
    #     checkin_date = parse_date(checkin)
    #     checkout_date = parse_date(checkout)
    #     if not checkin_date or not checkout_date or checkin_date >= checkout_date:
    #         raise ValidationError("Invalid check-in or check-out date.")
    # except ValidationError as e:
    # return redirect('booking_successful')

    import random
    import string
    from datetime import datetime
    from twilio.rest import Client

    
    from .models import Booking_Successful
    email = request.GET.get('email', None)

    # Validate email
    try:
        validate_email(email)
    except ValidationError:
        return redirect('booking_successful')

    Booking_Successful.objects.create(
        name=request.GET.get('name', 'Unknown Name'),
        email=request.GET.get('email', 'Unknown email'),
        phone=request.GET.get('phone', 'Unknown phone'),
        room_name=request.GET.get('room_name', 'Unknown Room'),
        room_rate=float(request.GET.get('room_rate', 0) or 0),
        checkin=request.GET.get('checkin', '2004-08-12'),
        checkout=request.GET.get('checkout', '2004-08-12'),
        guests=int(request.GET.get('guests', 0) or 0),
        rooms_required=int(request.GET.get('rooms_required', 0) or 0),
        total_amount=float(request.GET.get('total_amount', 0) or 0),
        taxes=float(request.GET.get('taxes', 0) or 0),
        grand_total=float(request.GET.get('grand_total', 0) or 0),
        payment_status='Paid',
        invoice_pdf=request.FILES.get('invoice'),
        user=request.user,
        rating=request.GET.get('rating', 5),
        message=request.GET.get('feedback', 'No feedback provided'),
    )

    # Retrieve booking details from query parameters with proper defaults
    name = request.GET.get('name', 'Unknown Name')
    email = request.GET.get('email', 'Unknown email')
    phone = request.GET.get('phone', 'Unknown phone')
    room_name = request.GET.get('room_name', 'Unknown Room')
    room_rate = float(request.GET.get('room_rate', 0) or 0)
    checkin = request.GET.get('checkin', '2004-08-12')
    checkout = request.GET.get('checkout', '2004-08-12')
    nights = int(request.GET.get('nights', 0) or 0)
    guests = request.GET.get('guests', 'N/A')
    rooms_required = int(request.GET.get('rooms_required', 0) or 0)
    total_amount = float(request.GET.get('total_amount', 0) or 0)
    taxes = float(request.GET.get('taxes', 0) or 0)
    grand_total = float(request.GET.get('grand_total', 0) or 0)
    

    # Generate invoice number
    def generate_invoice_no():
        date_part = datetime.now().strftime('%Y%m%d')
        rand_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        return f"INV-{date_part}-{rand_part}"

    
    invoice_data = {
        'name': name,
        'email': email,
        'phone': phone,
        'room_name': room_name,
        'room_rate': room_rate,
        'checkin': checkin,
        'checkout': checkout,
        'nights': nights,
        'guests': guests,
        'rooms_required': rooms_required,
        'total_amount': total_amount,
        'taxes': taxes,
        'grand_total': grand_total,
        'invoice_no': generate_invoice_no(),
        'invoice_date': datetime.now().strftime('%d-%m-%Y'),
    }
    # Send confirmation email
    subject = "Booking Confirmation - Hotel Grand View"
    message = (
        f"Dear {name},\n\n"
        f"Thank you for booking with Hotel Grand View!\n"
        f"Your booking details:\n"
        f"Room: {room_name}\n"
        f"Check-in: {checkin}\n"
        f"Check-out: {checkout}\n"
        f"Guests: {guests}\n"
        f"Rooms Required: {rooms_required}\n"
        f"Grand Total: ${grand_total}\n\n"
        f"We look forward to hosting you!\n"
        f"Hotel Grand View"
    )
    send_mail(subject, message, None, [email])
    from django.core.mail import EmailMessage  # Add this import at the top of the file if not already present

    email_msg = EmailMessage(
        subject=subject,
        body=message,
        from_email=None,  # Replace with your email if needed
        to=[email],
    )
    # Generate the PDF content
    html = render_to_string('invoice_pdf.html', invoice_data)
    pdf = pdfkit.from_string(html, False, configuration=config)

    # Attach the generated PDF to the email
    email_msg.attach('invoice.pdf', pdf, 'application/pdf')
    email_msg.send()
    request.session['invoice_data'] = invoice_data

    # Twilio WhatsApp message
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        message_body = (
            f"Thank you for your booking, {name}!\n\n"
            f"Booking Details:\n"
            f"Room: {room_name}\n"
            f"Rate: ${room_rate} / night\n"
            f"Check-In: {checkin}\n"
            f"Check-Out: {checkout}\n"
            f"Nights: {nights}\n"
            f"Guests: {guests}\n"
            f"Rooms Required: {rooms_required}\n"
            f"Total Amount: ${total_amount}\n"
            f"Taxes: ${taxes}\n"
            f"Grand Total: ${grand_total}\n\n"
            f"We look forward to hosting you!"
        )
        message = client.messages.create(
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            body=message_body,
            to=f"whatsapp:{phone}"
        )
        print(f"WhatsApp message sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")

    # sms_message = client.messages.create(
    #     from_=settings.TWILIO_PHONE_NUMBER,  # Your Twilio SMS number
    #     body=message_body,
    #     to=phone  # Make sure phone is in format '+911234567890'
    # )
    # print(f"SMS sent: {sms_message.sid}")

    # Pass the details to the template
    context = invoice_data.copy()
    context['stripe_public_key'] = settings.STRIPE_PUBLIC_KEY
    return render(request, 'booking_successful.html', context)
    # Pass the details to the payment page
# context ={
#     'name':name,
#     'email':email,
#     'phone':phone,
#     'room_name': room_name,
#     'room_rate': room_rate,
#     'checkin': checkin,
#     'checkout': checkout,
#     'nights': nights,
#     'guests': guests,
#     'rooms_required': rooms_required,
#     'total_amount': total_amount,
#     'taxes': taxes,
#     'grand_total': grand_total,
#     'invoice_no': generate_invoice_no(),
#     'invoice_date': datetime.now().strftime('%d-%m-%Y'),
#     'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
#     # return render(request, 'booking_successful.html', context)
#     }
    
from django.contrib import messages

def submit_feedback(request):

    # from .models import Feedback
    # Feedback.objects.create(
    #     user = request.user,
    #     rating=request.POST.get('rating'),
    #     message=request.POST.get('feedback')
    # )
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        if feedback and rating:
            messages.success(request, 'Thank you for your feedback!')
        else:
            messages.error(request, 'Please provide both a rating and feedback.')
        return redirect('booking_successful')

from django.shortcuts import render
from .models import  Booking_Successful
def mybookings_view(request):
    if request.user.is_authenticated:
        # Fetch bookings for the logged-in user
        bookings = Booking_Successful.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'mybookings.html', {'bookings': bookings})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('signin')

from django.core.mail import send_mail

def submit_application(request):

    from .models import CareerApplication
    CareerApplication.objects.create (
        name=request.POST.get('name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        resume=request.FILES.get('resume'),
        cover_letter=request.POST.get('message')    
    )
            
    if request.method == 'POST':
        # Use parentheses () instead of square brackets []
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        resume = request.FILES.get('resume')
        message = request.POST.get('message')

        # Save the application or send an email
        # Example: Sending an email
        # send_mail(
        #     f"New Job Application from {name}",
        #     f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}",
        #     'your_email@example.com',  # Replace with your email
        #     ['hr@example.com'],  # Replace with HR's email
        #     fail_silently=False,
        # )

        # Add a success message
        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('career')

    return render(request, 'career.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

@login_required
def career(request):
    # Job listings (you can fetch these from a database if needed)
    job_listings = [
        {
            'title': 'Front Desk Executive',
            'location': 'Hotel Grand View, City Center',
            'responsibilities': 'Managing guest check-ins and check-outs, handling reservations, and providing exceptional customer service.',
        },
        {
            'title': 'Housekeeping Staff',
            'location': 'Hotel Grand View, City Center',
            'responsibilities': 'Ensuring rooms and public areas are clean and well-maintained, and attending to guest requests promptly.',
        },
        {
            'title': 'Restaurant Manager',
            'location': 'Hotel Grand View, City Center',
            'responsibilities': 'Overseeing restaurant operations, managing staff, and ensuring a high-quality dining experience for guests.',
        },
    ]

    return render(request, 'career.html', {'job_listings': job_listings})
    
def gallery(request):
    return render(request, 'gallery.html')

from django.http import JsonResponse
from datetime import datetime

def check_availability(request):
    if request.method == 'GET':
        guests = request.GET.get('guests')
        checkin = request.GET.get('checkin')
        checkout = request.GET.get('checkout')

        # Convert check-in and check-out dates to datetime objects
        try:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d')
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Example logic to check availability (replace with your database query)
        if checkin_date >= checkout_date:
            return JsonResponse({'error': 'Check-out date must be after check-in date'}, status=400)

        # Simulate room availability check
        available_rooms = [
            {'room_type': 'Presidential Suite'},
            {'room_type': 'Royal Suite'},
            {'room_type': 'Suite'},
            {'room_type': 'Junior Suite'},
            {'room_type': 'Deluxe Room'},
        ]

        # Return available rooms as JSON
        return render(request, 'check_availability.html', {
            'available_rooms': available_rooms,
            'guests': guests,
            'checkin': checkin,
            'checkout': checkout,
        })
from django.shortcuts import render

@login_required
def membership_page(request):
    if request.method == "POST":
        # Handle form submission here (save to DB, send email, etc.)
        # For now, just show a thank you message
        return render(request, 'membership_page.html', {'success': True})
    return render(request, 'membership_page.html')

def membership_details(request):
    plan_name = request.GET.get('plan_name', 'Unknown Plan')
    plan_rate = request.GET.get('plan_rate', '0')  # Default to '0' if not provided
    if request.method == "POST":
        # Collect details and proceed (e.g., save to DB, redirect to payment, etc.)
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date', 'N/A')
        # You can save or process these details as needed
        # For now, just show a thank you page or message
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'plan_name': plan_name,
            'plan_rate': plan_rate,
            'date':date,
        }
        return render(request, 'membership_confirmation.html', context)  
    context = {
        'plan_name': plan_name,
        'plan_rate': plan_rate,
    }
    return render(request, 'membership_details.html', context)

def membership_confirmation(request):
    from .models import Membership_Confirmation
    # Calculate grand_total if not provided
    plan_rate = float(request.POST.get('plan_rate', 0))
    total_amount = plan_rate
    taxes = total_amount * 0.18
    grand_total = total_amount + taxes

    Membership_Confirmation.objects.create(
        name=request.POST.get('name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        date=request.POST.get('date'),
        plan_name=request.POST.get('plan_name'),
        plan_rate=plan_rate,
        grand_total=grand_total,
    )
    if request.method == 'POST':
        name = request.POST.get('name', 'Unknown Name')
        email = request.POST.get('email', 'Unknown Email')
        phone = request.POST.get('phone', 'Unknown Phone')
        date = request.POST.get('date', 'N/A')
        plan_name = request.POST.get('plan_name', 'Unknown Plan')
        plan_rate = float(request.POST.get('plan_rate', 0))

        total_amount = plan_rate
        taxes = total_amount * 0.18
        grand_total = total_amount + taxes
        context = {
            'name': name,
            'email': email,
            'phone': phone,
            'date': date,
            'plan_name': plan_name,
            'plan_rate': plan_rate,
            'total_amount': total_amount,
            'taxes': taxes,
            'grand_total': grand_total,
        }
        return render(request, 'membership_confirmation.html', context)
    return redirect('membership_page')

def membership_payment_page(request):
    # Retrieve booking details from query parameters (GET)
    name = request.GET.get('name', 'Unknown Name')
    email = request.GET.get('email', 'Unknown Email')
    phone = request.GET.get('phone', 'Unknown Phone')
    date = request.GET.get('date', 'N/A')
    plan_name = request.GET.get('plan_name', 'Unknown Plan')
    plan_rate = float(request.GET.get('plan_rate', 0) or 0)
    total_amount = float(request.GET.get('total_amount', 0) or 0)
    taxes = float(request.GET.get('taxes', 0) or 0)
    grand_total = float(request.GET.get('grand_total', 0) or 0)

    context = {
        'name': name,
        'email': email,
        'phone': phone,
        'date': date,
        'plan_name': plan_name,
        'plan_rate': plan_rate,
        'total_amount': total_amount,
        'taxes': taxes,
        'grand_total': grand_total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'membership_payment_page.html', context)


from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit  # or use xhtml2pdf, WeasyPrint, etc.
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')  # Update path as needed

def download_invoice(request):
    invoice_data = request.session.get('invoice_data')
    if not invoice_data:
        return redirect('booking_successful')
    html = render_to_string('invoice_pdf.html', invoice_data)
    pdf = pdfkit.from_string(html, False, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response

import random
import string

def generate_invoice_no():
    date_part = datetime.now().strftime('%Y%m%d')
    rand_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"INV-{date_part}-{rand_part}"


from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Feedback  # Assuming you have a Feedback model

def submit_feedback(request):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback_text = request.POST.get('feedback')
        if rating and feedback_text:
            # Save feedback to the database
            Feedback.objects.create(rating=rating, feedback=feedback_text)
            # Return a JSON response for success
            return JsonResponse({'success': True, 'message': 'Feedback submitted successfully!'})
        else:
            # Return a JSON response for error
            return JsonResponse({'success': False, 'message': 'Please fill in all fields.'}, status=400)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking_Successful

@login_required
def book_room(request):
    if request.method == 'POST':
        # Get booking details from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        room_name = request.POST.get('room_name')
        room_rate = request.POST.get('room_rate')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        guests = request.POST.get('guests')
        rooms_required = request.POST.get('rooms_required')
        total_amount = request.POST.get('total_amount')
        taxes = request.POST.get('taxes')
        grand_total = request.POST.get('grand_total')

        # Save booking details to the database
        booking = Booking_Successful.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            room_name=room_name,
            room_rate=room_rate,
            checkin=checkin,
            checkout=checkout,
            guests=guests,
            rooms_required=rooms_required,
            total_amount=total_amount,
            taxes=taxes,
            grand_total=grand_total,
            payment_status='Pending'
        )
        booking.save()

        # Add a success message
        messages.success(request, 'Your booking was successful!')
        return redirect('booking_successful')  # Redirect to the booking successful page
    return render(request, 'booking.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Booking_Successful

@login_required
def my_bookings(request):
    # Fetch all bookings for the logged-in user
    bookings = Booking_Successful.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'mybookings.html', {'bookings': bookings})