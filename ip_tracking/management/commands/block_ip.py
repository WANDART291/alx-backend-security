# ip_tracking/management/commands/block_ip.py

from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Blocks a specific IP address by adding it to the BlockedIP table.'

    def add_arguments(self, parser):
        # The command requires one argument: the IP address to block
        parser.add_argument('ip_address', type=str, help='The IP address to block.')
        parser.add_argument('--reason', type=str, default='', help='Optional reason for blocking the IP.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options['reason']

        # Basic validation (optional but recommended)
        if not ip_address:
            raise CommandError("You must provide an IP address to block.")

        try:
            BlockedIP.objects.create(ip_address=ip_address, reason=reason)
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
        except IntegrityError:
            raise CommandError(f'IP address {ip_address} is already blocked.')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')