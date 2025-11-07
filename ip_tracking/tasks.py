# ip_tracking/tasks.py

from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.db.models import Count
from django.db import IntegrityError # To handle unique=True constraint

from ip_tracking.models import RequestLog, SuspiciousIP, BlockedIP

# Define sensitive paths for flagging
SENSITIVE_PATHS = ['/admin', '/login', '/sensitive'] 
REQUEST_COUNT_THRESHOLD = 100

@shared_task
def flag_suspicious_ips():
    """
    Runs hourly to check logs for IPs exceeding a request threshold or accessing sensitive paths.
    """
    # Look at logs from the last one hour
    time_threshold = timezone.now() - timedelta(hours=1)
    
    # --- 1. Rule: Check for IPs accessing sensitive paths ---
    # Find IPs that accessed any sensitive path in the last hour
    sensitive_ips = RequestLog.objects.filter(
        timestamp__gte=time_threshold,
        path__in=SENSITIVE_PATHS
    ).values_list('ip_address', flat=True).distinct()

    for ip in sensitive_ips:
        try:
            SuspiciousIP.objects.create(
                ip_address=ip,
                reason="Accessed sensitive paths in the last hour."
            )
        except IntegrityError:
            # IP is already flagged; skip or update reason if needed
            pass 

    # --- 2. Rule: Check for IPs exceeding 100 requests/hour ---
    
    # Aggregate data: Count requests per IP in the last hour
    high_count_ips = RequestLog.objects.filter(timestamp__gte=time_threshold).values('ip_address')
    high_count_ips = high_count_ips.annotate(request_count=Count('ip_address'))
    
    # Filter for IPs exceeding the threshold
    high_count_ips = high_count_ips.filter(request_count__gt=REQUEST_COUNT_THRESHOLD)
    
    for item in high_count_ips:
        ip = item['ip_address']
        count = item['request_count']
        
        try:
            SuspiciousIP.objects.create(
                ip_address=ip,
                reason=f"Exceeded request threshold: {count} requests in 1 hour."
            )
        except IntegrityError:
            # Already flagged
            pass

    return f"Suspicious IP analysis complete. Flagged {len(sensitive_ips) + high_count_ips.count()} IPs."