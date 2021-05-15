from django.contrib import admin
from .models import User, Advisor, Booking

# Register your models here.
admin.site.register(User)
admin.site.register(Advisor)
admin.site.register(Booking)
