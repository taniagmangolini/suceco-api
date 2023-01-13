"""URLs mapping for the Register APIs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from register import views

router = DefaultRouter()
router.register('registers', views.RegisterViewSet)

app_name = 'register'

urlpatterns = [
    path('', include(router.urls)),
]
