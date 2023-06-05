from django.urls import path, include
from .views import UsersAPIView,UserPostAPIView,CustomerViewSet,CustomerAPIView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('users/', UsersAPIView.as_view()),
    path('customers/',CustomerAPIView.as_view()),
    path('users/<int:id>/', UserPostAPIView.as_view())
]