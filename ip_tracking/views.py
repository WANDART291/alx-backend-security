# ip_tracking/views.py

from django.http import HttpResponse
# Import the decorator
from django_ratelimit.decorators import ratelimit
# Import redirect for a more realistic scenario (e.g., login failure)
from django.shortcuts import redirect 

# We will apply two different rate limits to the same view.
# The decorator checks are done in the order they are listed.

# 1. Limit for ANONYMOUS users (key='ip', 5/m rate)
@ratelimit(key='ip', rate='5/m', block=True)
# 2. Limit for AUTHENTICATED users (key='user', 10/m rate)
@ratelimit(key='user', rate='10/m', block=True)
def sensitive_access_view(request):
    """
    Simulates a sensitive endpoint (like a login attempt or API call).
    The rate limits are enforced by the decorators above.
    """
    
    # Check if the request was blocked by EITHER decorator
    if getattr(request, 'limited', False):
        # The client hit their specific limit (5/m for anon, 10/m for auth)
        return HttpResponse("Rate limit exceeded (403 Forbidden). Try again later.", status=403)
        
    # Content returned if limits are not exceeded
    user_status = "Authenticated" if request.user.is_authenticated else "Anonymous"
    return HttpResponse(f"Welcome, {user_status} user! Access granted.", status=200)
