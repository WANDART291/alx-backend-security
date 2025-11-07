# ip_tracking/models.py

from django.db import models

# --- Task 0 & 2: IP Logging and Geolocation Model ---
class RequestLog(models.Model):
    """
    Model to store basic information and geolocation about incoming requests.
    """
    ip_address = models.CharField(max_length=45, verbose_name="IP Address")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    path = models.CharField(max_length=200, verbose_name="Request Path")
    
    # Fields for Geolocation (Task 2)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.ip_address} accessed {self.path} ({self.city}, {self.country})"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Request Log"
        verbose_name_plural = "Request Logs"

# --- Task 1: IP Blacklisting Model ---
class BlockedIP(models.Model):
    """
    Model to store IP addresses that are permanently blocked.
    """
    ip_address = models.CharField(
        max_length=45, 
        unique=True, 
        verbose_name="IP Address to Block"
    )
    reason = models.TextField(blank=True, verbose_name="Reason for Block") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ip_address

    class Meta:
        verbose_name = "Blocked IP"
        verbose_name_plural = "Blocked IPs"

# --- Task 4: Anomaly Detection/Suspicious IPs Model ---
class SuspiciousIP(models.Model):
    """
    Model to store IPs flagged for suspicious activity (high rate or sensitive path access).
    """
    ip_address = models.CharField(max_length=45, unique=True, verbose_name="Suspicious IP")
    reason = models.CharField(max_length=255, verbose_name="Reason for Flag")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.reason}"

    class Meta:
        verbose_name = "Suspicious IP"
        verbose_name_plural = "Suspicious IPs"

