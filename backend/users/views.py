from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from rest_framework import views, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.middleware import csrf
from backend import settings
from .serializer import UserSerializer,LoginSerializer
from ticket.serializers import TicketSerializer,OrderSerializer
from ticket.models import Ticket,Order
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
class MyTokenObtainPariView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
class UsersAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)
    
class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data =request.data 
        serializer = LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'data':serializer.errors,
            })
        response = Response()
        data =serializer.get_jwt_token(serializer.data)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=data['access'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response['Authorization'] = f"Bearer {data['access']}"
        print(data['access'])
        csrf.get_token(request)
        response.data = {"Success" : "Login successfully","data":data}
        return response


class LogoutView(APIView):
    def post(self, request):
        # Delete the user's refresh token
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                # Handle any exception that might occur
                return Response({'detail': 'Invalid refresh token.'}, status=400)

        # Perform regular logout
        logout(request)
        
        return Response({'detail': 'Logout successful.'})


class RegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data['email']
            )
            return Response({'detail': 'Registration successful.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from .models import Customer, User
from .serializer import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
class CustomerAPIView(APIView):
    def get(self, request):
        token = request.COOKIES.get('access_token')
        users = Customer.objects.all()
        serializer = CustomerSerializer(users, many = True)
        return Response(serializer.data,token)
    def post(self, request):
        serializer = CustomerSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            Customer.objects.create(request.data)
            return Response(serializer.data, status = 201)
        return Response(serializer.errors, status = 400)


class UserPostAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, id, *args, **kwargs):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        customer = Customer.objects.filter(id=id).first()
        tickets = Ticket.objects.filter(user=customer.id)
        orders = Order.objects.filter(user=customer.id)
        customer_serializer = CustomerSerializer(customer)
        ticket_serializer = TicketSerializer(tickets, many=True)
        order_serializer = OrderSerializer(orders,many=True)
        response_data = {
            'customer': customer_serializer.data,
            'tickets': ticket_serializer.data,
            "order":order_serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
# class TicketListAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         posts = Ticket.objects.all()
#         serializer = TicketSerializer(posts, many = True)
#         return Response(serializer.data, status = status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         data = {
#             'user': request.user.id,
#             'ticket_number' : request.data.get('ticket_number')
#         }
#         serializer = TicketSerializer(data = data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status = status.HTTP_201_CREATED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
# class PostDetailAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self, pk):
#         try:
#             return Ticket.objects.get(pk = pk)
#         except Ticket.DoesNotExist:
#             return None

#     def get(self, request, pk, *args, **kwargs):
#         post = self.get_object(pk)
#         if post is None:
#             return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
#         serializer = TicketSerializer(post)
#         return Response(serializer.data, status = status.HTTP_200_OK)

#     def put(self, request, pk, *args, **kwargs):
#         post = self.get_object(pk)
#         if post is None:
#             return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
#         data = {
#             'user': request.user.id,
#             'ticket_number':request.data.get('ticket_number')
#         }
#         serializer = TicketSerializer(post, data = data, partial = True)
#         if serializer.is_valid():
#             if post.user.id == request.user.id:
#                 serializer.save()
#                 return Response(serializer.data, status = status.HTTP_200_OK)
#             return Response({"error": "You are not authorized to edit this ticket"}, status = status.HTTP_401_UNAUTHORIZED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, *args, **kwargs):
#         post = self.get_object(pk)
#         if post is None:
#             return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
#         if post.user.id == request.user.id:
#             post.delete()
#             return Response({"res": "Object deleted!"}, status = status.HTTP_200_OK)
#         return Response({"error": "You are not authorized to delete this post"}, status = status.HTTP_401_UNAUTHORIZED)
