# backend_security_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Use a clear path for the sensitive view
    path('sensitive/', include('ip_tracking.urls')), 
]
