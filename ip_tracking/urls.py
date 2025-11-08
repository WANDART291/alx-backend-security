# ip_tracking/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # This points to the rate-limited view from Task 3
    path('access/', views.sensitive_access_view, name='sensitive_access'), 
]
