"""
NexGear URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.catalog.urls')),
    path('auth/', include('apps.accounts.urls')),
    path('orders/', include('apps.orders.urls')),
    path('manager/', include('apps.manager.urls')),

    # REST API
    path('api/', include('apps.catalog.api_urls')),
    path('api/auth/', include('apps.accounts.api_urls')),
    path('api/', include('apps.orders.api_urls')),

    # Favicon — 404 xatosini oldini olish (base.html da SVG data URI ishlatiladi)
    path('favicon.ico', lambda request: HttpResponse(status=204)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

