from django.contrib import admin

from .models import CustomUser
from orders.models import CourierProfile

admin.site.register(CustomUser)
admin.site.register(CourierProfile)
