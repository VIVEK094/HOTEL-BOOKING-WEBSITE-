from django.contrib import admin
from .models import Booking_Successful
# from .models import Feedback
from .models import CareerApplication
from .models import Membership_Confirmation
from .models import Contact
from .models import dining
from .models import Feedback


# Register your models here.
admin.site.register(Booking_Successful)
admin.site.register(Feedback)
admin.site.register(CareerApplication)
admin.site.register(Membership_Confirmation)
admin.site.register(Contact)
admin.site.register(dining)





