# ip_tracking/admin.py

from django.contrib import admin
from .models import RequestLog, BlockedIP # <-- Make sure BlockedIP is imported

# Register RequestLog (from Task 0)
@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'timestamp')
    search_fields = ('ip_address', 'path')
    list_filter = ('timestamp',)

# Register BlockedIP (for Task 1)
@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'created_at')
    search_fields = ('ip_address', 'reason')


