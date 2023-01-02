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
         name='custom-login'),
    path('password-reset-request/',
         views.RequestPasswordResetEmailView.as_view(),
         name='password-reset-request'),
    path('password-reset-confirm/<str:email>/<str:token>/',
         views.ConfirmPasswordResetView.as_view(),
         name='password-reset-confirm'),
    path('password-reset-complete',
         views.CompletePasswordResetView.as_view(),
         name='password-reset-complete'),
]
