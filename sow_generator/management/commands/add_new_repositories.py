from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings


class Command(BaseCommand):
    help = """Scan SOW Generator metadata files for repositories not in the \
database"""

    @transaction.commit_on_success
    def handle(self, *args, **options):
        pass
