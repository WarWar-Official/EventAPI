'''
URL configuration for EventAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
'''
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, AddEventView, DeleteEventView, UpdateEventView, GetEventView, LeaveEventView, JoinEventView, GetEventPsrticipantsView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='My API',
        default_version='v1',
        description='API documentation',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/event/add/', AddEventView.as_view(), name='add_event'),
    path('api/event/get/', GetEventView.as_view(), name='get_event'),
    path('api/event/get/participants/', GetEventPsrticipantsView.as_view(), name='get_event'),
    path('api/event/delete/', DeleteEventView.as_view(), name='delete_event'),
    path('api/event/update/', UpdateEventView.as_view(), name='update_event'),
    path('api/event/join/', JoinEventView.as_view(), name='join_event'),
    path('api/event/leave/', LeaveEventView.as_view(), name='leave_event'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
