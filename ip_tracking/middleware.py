# ip_tracking/middleware.py

from ip_tracking.models import RequestLog, BlockedIP
from ipware import get_client_ip
from django.http import HttpResponseForbidden
from django.core.cache import cache 
from django_ip_geolocation.utils import get_geolocation # CORRECTED IMPORT
import logging

logger = logging.getLogger('ip_tracking.middleware')

# --- Task 1: IP Blacklisting Middleware (Must run FIRST) ---
class BlacklistMiddleware:
    """Blocks requests from IPs listed in the BlockedIP model."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        client_ip = ip if ip else 'unknown'

        # Check if the IP is blacklisted
        is_blocked = BlockedIP.objects.filter(ip_address=client_ip).exists()

        if is_blocked:
            logger.warning(f"BLOCKED ACCESS (403): IP {client_ip} is blacklisted.")
            # Return 403 Forbidden immediately
            return HttpResponseForbidden("Access Denied: Your IP address is blacklisted.")

        response = self.get_response(request)
        return response

# --- Task 0 & 2: IP Logging and Geolocation Middleware ---
class IPLoggingMiddleware:
    """Logs IP, path, and performs cached geolocation lookup."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.CACHE_TIMEOUT = 60 * 60 * 24 # 24 hours

    def get_geo_data(self, ip_address):
        """Fetches and caches geolocation data for a given IP."""
        # Skip lookup for local or unknown IPs
        if ip_address in ['unknown', '127.0.0.1']:
            return None, None

        # 1. Try to fetch from cache
        cache_key = f'geo_ip_{ip_address}'
        geo_data = cache.get(cache_key)

        if geo_data is None:
            # 2. If not in cache, perform API lookup
            try:
                # get_geolocation returns a dict
                geo_data = get_geolocation(ip_address)
                
                # 3. Cache the result
                cache.set(cache_key, geo_data, self.CACHE_TIMEOUT)
                
            except Exception as e:
                logger.warning(f"Geolocation API lookup failed for IP {ip_address}: {e}")
                return None, None 
        
        # Extract required fields (keys depend on the geolocation service)
        # Using common keys provided by django-ip-geolocation
        country = geo_data.get('country')
        city = geo_data.get('city')
        
        return country, city


    def __call__(self, request):
        ip, is_routable = get_client_ip(request)
        client_ip = ip if ip else 'unknown'
        request_path = request.path
        
        # Skip logging/geolocation for static files
        if request_path.startswith('/static/'):
            return self.get_response(request)

        # Get Geolocation Data (Task 2)
        country, city = self.get_geo_data(client_ip)
        
        # Save the log (Task 0/2)
        try:
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request_path,
                country=country,  
                city=city         
            )
            logger.info(f"Logged IP: {client_ip} ({country}/{city}), Path: {request_path}")
        except Exception as e:
            logger.error(f"Error saving request log: {e}")

        response = self.get_response(request)
        return response