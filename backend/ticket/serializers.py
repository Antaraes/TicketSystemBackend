from rest_framework import serializers
from .models import Ticket,Order,User
from django.db import transaction
class TicketSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Ticket
        fields = ['id','number','status','user','created_at']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    numbers = serializers.ListField(child=serializers.IntegerField())
    # image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Order
        fields = ['user', 'order_image', 'numbers', 'paid_amount', 'order_date']
    @classmethod
    def create_tickets(cls, user, order, numbers):
        existing_tickets = Ticket.objects.filter(number__in=numbers, status__in=['C', 'P'])
        if existing_tickets.exists():
            raise ValueError('Some ticket numbers are already chosen or pending')

        with transaction.atomic():
            created_tickets = []
            for number in numbers:
                ticket = Ticket.objects.create(user=user, order=order, number=number, status='P')
                created_tickets.append(ticket)

        return created_tickets
    