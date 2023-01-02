"""
Views for the User API.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.response import Response

from user.serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    RequestPasswordResetEmailSerializer,
    CompletePasswordResetSerializer,
)

from utils.mail_service import send_reset_password_email


class CreateUserView(generics.CreateAPIView):
    """Create a new user."""
    serializer_class = UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom CustomTokenObtainPairView."""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)


class RequestPasswordResetEmailView(generics.GenericAPIView):
    """Request password reset by e-mail API"""
    serializer_class = RequestPasswordResetEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = request.data['email']
            user = get_user_model().objects.filter(email=email).first()
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('user:password-reset-confirm',
                                   kwargs={'email': email, 'token': token})
            url = 'http://' + current_site + relativeLink
            send_reset_password_email({'email': email, 'url': url})
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPasswordResetView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, email, token):
        """Validate if the token to change the password is still valid."""
        user = get_user_model().objects.filter(email=email).first()
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({'error': 'Invalid token.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        return Response(status=status.HTTP_200_OK)


class CompletePasswordResetView(generics.GenericAPIView):
    serializer_class = CompletePasswordResetSerializer
    permission_classes = (AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)
