"""URLs mapping for the Register APIs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from register_picture import views

router = DefaultRouter()
router.register('registers_pictures', views.RegisterPictureViewSet)

app_name = 'register_picture'

urlpatterns = [
    path('', include(router.urls)),
]
