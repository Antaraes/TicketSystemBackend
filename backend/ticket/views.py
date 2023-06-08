from django.shortcuts import render
from rest_framework import viewsets
from django.db import transaction
from rest_framework.response import Response
from .models import Ticket,Order
from rest_framework.views import APIView
from rest_framework import permissions,status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import TicketSerializer,OrderSerializer,PaymentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from django.conf import settings
from .I_image2text import image
import ast
# Create your views here.
class TicketViewSet(viewsets.ModelViewSet):
    
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    def create(self, request, *args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        authentication_classes = [JWTAuthentication]
        user = request.user
        # number = request.data.get('number')
        number = request.data.get('number')
        print(number)
        if Ticket.objects.filter(number=number,status__in=['C','P']).exists():
            return Response({'error':"Ticket number already chosen or pending"},status=400)
        # created_tickets = Ticket.create_tickets(user, number)
        ticket = Ticket.objects.create(user = user , number=number,status='P')
        serializer = self.get_serializer(ticket)
        # serializer = self.get_serializer(created_tickets)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial',False)
        instance = self.get_object()    
        status = request.data.get('status')
        if status == 'C':
            instance.status = 'C'
            instance.save()
        return Response("Update SuccessFully")

class TicketDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self,pk):
        try:
            return Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return None
    def get(self, request, pk, *args, **kwargs):
        ticket = self.get_object(pk)
        if ticket is None:
            return Response({'error': 'Ticket not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = Ticket(ticket)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class OrderView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        # number_list = []
        # for number in numbers:
        #     number_list.append(number)
        # print([int(number) for number in number_list if number.isdigit()])

        if serializer.is_valid():
            user = request.user
            numbers_json = request.data.get('numbers')
            numbers = json.loads(numbers_json)
            order_image = request.data.get('order_image')
            file_name = default_storage.save('orderImages/' + order_image.name, ContentFile(order_image.read()))
            image_url = self.get_image_url(file_name)

            data = image.imageDetect(image_url[1:])
            print(data)
            if data != False:
                get_Name = data["Name"]
                get_Type = data["Type"]
                get_Amount = data["Amount"]
                get_Phone = data["Phone"]
                get_Date = data["Date"]
                get_TransactionID = data['Transaction Id']
                print(get_Date,get_Name)
                with transaction.atomic():

                    order = serializer.save(user=user)
                    payment_serializer = PaymentSerializer(data={
                        'order': order.id,
                        'p_Name': get_Name,
                        'p_Type': get_Type,
                        'p_Amount': get_Amount,
                        'p_Phone': get_Phone,
                        'p_TransactionID': get_TransactionID,
                        'p_Date': get_Date
                    })
                    if not payment_serializer.is_valid():
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    payment = payment_serializer.save()
                    tickets = serializer.create_tickets(user=user, order=order, numbers=numbers)
                    order.payment = payment
                    order.save()
                    # serializer.save(user=user,numbers=numbers_list)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Invalid Photo")
                return Response({"message": "Invalid Photo"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = OrderSerializer.errors
            errors.update(PaymentSerializer.errors)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Delete the order_image file if it exists
        if instance.order_image:
            default_storage.delete(instance.order_image.name)

        return super().destroy(request, *args, **kwargs)
    def get_image_url(self, image):
        # Assuming the image is stored locally
        return settings.MEDIA_URL  +  image