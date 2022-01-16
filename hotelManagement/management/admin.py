import site
from django.contrib import admin
from .models import UserProfile ,Room,Reservations
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Room)
admin.site.register(Reservations)