from django.urls import path
from . import api_views

urlpatterns = [
    path('register/', api_views.api_register, name='api-register'),
    path('login/', api_views.api_login, name='api-login'),
    path('users/me/', api_views.api_me, name='api-me'),
    path('addresses/', api_views.api_addresses, name='api-addresses'),
]
