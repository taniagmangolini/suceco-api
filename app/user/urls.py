"""
Urls mapping for the User API.
"""
from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/',
         views.CustomTokenObtainPairView.as_view(),
         name='custom_login'),
]
