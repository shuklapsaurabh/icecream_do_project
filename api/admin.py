from django.contrib import admin

# Register your models here.
from .models import Flavor, Order

admin.site.register(Flavor)
admin.site.register(Order)