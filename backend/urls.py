"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import include, path
from rest_framework import routers
from incidents.views import UserViewSet, IncidentViewSet
from incidents.views import UserRegistrationView
from .views import UserLoginView
from .views import ForgotPasswordView
from django.urls import path
from .views import IncidentCreateView
from .views import IncidentUpdateView
from .views import IncidentRetrieveView
from . import views
from incidents.views import IncidentSearchView


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'incidents', IncidentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('incidents/<uuid:incident_id>/', IncidentUpdateView.as_view(), name='incident-update'),
    path('api/login/', views.login, name='login'),
    path('api/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('incidents/create/', IncidentCreateView.as_view(), name='incident-create'),
    path('incidents/<int:pk>/update/', IncidentUpdateView.as_view(), name='incident-update'),
    path('incidents/<int:pk>/', IncidentRetrieveView.as_view(), name='incident-retrieve'),
    path('incidents/search/', IncidentSearchView.as_view(), name='incident-search'),
]
