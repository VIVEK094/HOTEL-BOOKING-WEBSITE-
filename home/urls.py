from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns =[
    path('', views.index, name='home'),  # Home page
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('rooms/', views.rooms, name='rooms'),
    path('book/', views.book, name='book'),
    path('amenities/', views.amenities, name='amenities'),
    path('Dining/', views.Dining, name='Dining'),  
    path('booking/', views.booking, name='booking'),
    path('payment_page/', views.payment_page, name='payment_page'),
    path('create-stripe-session/', views.create_stripe_session, name='create_stripe_session'),
    path('create-paypal-payment/', views.create_paypal_payment, name='create_paypal_payment'),
    path('cod-payment/', views.cod_payment, name='cod_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancel/', views.payment_cancel, name='payment_cancel'),
    path('booking_successful/', views.booking_successful, name='booking_successful'),
    path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
    path('mybookings/', views.mybookings_view, name='mybookings'),
    path('create_razorpay_order/', views.create_razorpay_order, name='create_razorpay_order'),
    path('career/', views.career, name='career'),
    path('submit_application/', views.submit_application, name='submit_application'),
    path('gallery/', views.gallery, name='gallery'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('membership_page/', views.membership_page, name='membership_page'),
    path('membership_details/', views.membership_details, name='membership_details'),
    path('membership_confirmation/', views.membership_confirmation, name='membership_confirmation'),
    path('membership_payment_page/', views.membership_payment_page, name='membership_payment_page'),
    path('invoice/download/', views.download_invoice, name='download_invoice'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

   
]


