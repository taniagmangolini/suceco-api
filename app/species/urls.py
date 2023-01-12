"""URLs mapping for the Reference APIs."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from species import views

router = DefaultRouter()
router.register('species', views.SpeciesViewSet)

app_name = 'species'

urlpatterns = [
    path('', include(router.urls)),
]
