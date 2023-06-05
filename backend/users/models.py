from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.query import QuerySet

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN','Admin'
        CUSTOMER = "CUSTOMER",'CUSTOMER'
    base_role = Role.ADMIN
    role = models.CharField(max_length=50,choices=Role.choices)
    def save(self,*args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other staff-related fields
class Customer(User):
    customer_id = models.AutoField(primary_key=True)
    base_role = User.Role.CUSTOMER
    class Meta:
        verbose_name_plural = "Customers"
    def __str__(self):
        return self.username
    

# class Ticket(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     ticket_number = models.ForeignKey(Ticket,on_delete=models.CASCADE)
#     purchase_datetime = models.DateTimeField(auto_now_add=True)
    # Add other ticket-related fields
