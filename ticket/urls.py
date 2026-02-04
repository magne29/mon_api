from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TicketViewSet
from  .views import DepartmentViewSet
from django.urls import path


router = DefaultRouter()
router.register(r'ticket', TicketViewSet)
router.register(r'department', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),

]