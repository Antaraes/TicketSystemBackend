from django.shortcuts import render
from rest_framework import viewsets
from django.db import transaction
from rest_framework.response import Response
from .models import Ticket,Order
from rest_framework.views import APIView
from rest_framework import permissions,status
from .serializers import TicketSerializer,OrderSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from .image import imageDetect
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
            numbers = request.data.get('numbers')
            with transaction.atomic():
                order = serializer.save(user=user)
                tickets = serializer.create_tickets(user=user, order=order, numbers=numbers)

                # serializer.save(user=user,numbers=numbers_list)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_image_url(self, image):
        # Assuming the image is stored locally
        return settings.BASE_URL + image.url