from rest_framework import serializers
from .models import Ticket,Order,User,Payment
from django.db import transaction
class TicketSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Ticket
        fields = ['id','number','status','user','created_at']
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [ 'order', 'p_Name', 'p_Type', 'p_Amount', 'p_Phone', 'p_TransactionID', 'p_Date']

    def create(self, validated_data):
        order = validated_data.pop('order')
        payment = Payment.objects.create(order=order, **validated_data)
        return payment
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']
class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    numbers = serializers.JSONField()
    payment = PaymentSerializer(read_only=True)
    # image_url = serializers.SerializerMethodField('get_image_url')
    class Meta:
        model = Order
        fields = ['id','user', 'order_image', 'numbers', 'paid_amount', 'order_date','payment']
    @classmethod
    def create_tickets(cls, user, order, numbers):
        existing_tickets = Ticket.objects.filter(number__in=numbers, status__in=['C', 'P'])
        if existing_tickets.exists():
            raise ValueError('Some ticket numbers are already chosen or pending')

        with transaction.atomic():
            created_tickets = []
            for number in numbers:
                ticket = Ticket.objects.create(user=user, order=order, number=number, status='P')
                created_tickets.append(number)


        return created_tickets

