# ip_tracking/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Map the URL
    path('access/', views.sensitive_access_view, name='sensitive_access'),
]