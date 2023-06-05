
from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.
def upload_to(instance,filename):
    return 'orderImages/c{filename}'.format(filename=filename)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    numbers = ArrayField(models.IntegerField(max_length=10), blank=True,null=True)
    order_image = models.ImageField(upload_to=upload_to,default='orderImages/default.jpg')
    paid_amount = models.DecimalField(max_digits=8,decimal_places=2,blank=True,null=True)

    class Meta:
        verbose_name_plural = "Orders"

    def get_image(self):
        if self.order_image:
            return 'http://127.0.0.1:8000' + self.order_image.url
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    NUMBER_STATUS_CHOICES = [
        ('A','Active'),
        ('P','Pending'),
        ('C','Chosen')
    ]
    number = models.IntegerField(unique=True)
    status = models.CharField(max_length=1,choices=NUMBER_STATUS_CHOICES,default='A')
    created_at = models.DateTimeField(auto_now_add=True)
    #for create multiple numbers
    

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)


        