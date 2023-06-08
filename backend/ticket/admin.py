from django.contrib import admin
from .models import Ticket,UserProfile,Order,Payment

admin.site.register(Ticket)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.site_header = "Ticket Management"
admin.site.index_title = "Welcome to Ticket Admin Portal"


