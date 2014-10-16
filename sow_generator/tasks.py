from celery import task
from celery.decorators import periodic_task

from sow_generator.models import Repository


@task(max_retries=5)
def sync_repository(id):
    obj = Repository.objects.get(id=id)
    # Talk to github


@periodic_task(run_every=crontab(hour='*', minute='0', day_of_week='*'))
def sync_repositories():
    """Sync all repositories"""
    pass
