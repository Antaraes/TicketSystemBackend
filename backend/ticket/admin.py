from django.contrib import admin
from .models import Ticket,UserProfile,Order

admin.site.register(Ticket)
admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.site_header = "Ticket Management"
admin.site.index_title = "Welcome to Ticket Admin Portal"


