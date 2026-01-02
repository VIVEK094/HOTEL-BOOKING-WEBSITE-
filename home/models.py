from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

# Booking model
class Booking_Successful(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    room_name=models.CharField(max_length=100)
    room_rate=models.DecimalField(max_digits=10, decimal_places=2)
    checkin=models.DateField()
    checkout=models.DateField()
    guests=models.IntegerField()
    rooms_required=models.IntegerField(default=1)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2)
    taxes=models.DecimalField(max_digits=10, decimal_places=2)
    grand_total=models.DecimalField(max_digits=10, decimal_places=2)
    payment_status=models.CharField(max_length=50, default='Pending')
    invoice_pdf=models.FileField(upload_to='invoices/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    message = models.TextField(null=True)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return f"Booking Successful for {self.name}"
# Feedback model
# class Feedback(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.TextField()
#     rating = models.IntegerField(default=5)


#     def __str__(self):
#         return f"Feedback by {self.user.username} at {self.submitted_at}"

# Career Application model
class CareerApplication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application by {self.name} at {self.applied_at}"

# Membership model
class Membership_Confirmation(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    plan_name = models.CharField(max_length=100)
    plan_rate = models.DecimalField(max_digits=10, decimal_places=2)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Membership Confirmation for {self.name}"

