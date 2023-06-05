from django.urls import include, path
from rest_framework import routers
from .views import TicketViewSet,OrderView

router = routers.DefaultRouter()
router.register(r'tickets', TicketViewSet)
router.register(r'order',OrderView)
urlpatterns = [
    path('api/', include(router.urls)),
]
