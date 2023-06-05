from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User,Customer
from django.contrib.admin import AdminSite

class FounderSite(AdminSite):
    site_header = "Adminstration Site"
    index_title = "Welcome to Admin Portal"
founder_admin_site = FounderSite(name='event_admin')
admin.site.register(User)
admin.site.register(Customer)