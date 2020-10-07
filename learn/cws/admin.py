from django.contrib import admin
from cws.models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Address)