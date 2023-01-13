"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/',
         SpectacularSwaggerView.as_view(url_name='api-schema'),
         name='api-docs'),
    path('api/user/', include('user.urls')),
    path('api/forest/', include('forest.urls')),
    path('api/species/', include('species.urls')),
    path('api/reference/', include('reference.urls')),
    path('api/register/', include('register.urls')),
    path('api/login/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/login/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('api/login/verify/',
         TokenVerifyView.as_view(),
         name='token_verify'),
]
