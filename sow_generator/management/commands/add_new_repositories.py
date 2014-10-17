import os

import yaml

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.conf import settings

from sow_generator.models import Repository


class Command(BaseCommand):
    help = """Scan SOW Generator metadata files for repositories not in the \
database"""

    @transaction.commit_on_success
    def handle(self, *args, **options):
        top = os.path.join(os.path.dirname(__file__), "..", "..", "documents")
        for root, dirs, files in os.walk(top):
            for file in files:
                if file == "metadata.yaml":
                    fp = open(os.path.join(root, file), "r")
                    try:
                        di = yaml.load(fp)
                    finally:
                        fp.close()
                    for name in di.get("required_modules", []) \
                        + di.get("optional_modules", []):
                        obj, dc = Repository.objects.get_or_create(name=name)
