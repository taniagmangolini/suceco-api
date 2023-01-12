"""URLs mapping for the Reference APIs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reference import views

router = DefaultRouter()
router.register('references', views.ReferenceViewSet)

app_name = 'reference'

urlpatterns = [
    path('', include(router.urls)),
]
