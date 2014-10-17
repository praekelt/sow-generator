from github3 import login
from github3.models import GitHubError

from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from sow_generator.models import Repository, AuthToken


@task(max_retries=5)
def sync_repository(id):
    obj = Repository.objects.get(id=id)
    dirty = False
    token = AuthToken.objects.get(id=1).token
    gh = login(token=token)
    dc = gh.user()
    org, name = obj.orgname
    repo = gh.repository(org, name)
    if repo is not None:
        readme = repo.contents('README.rst')
        if readme is not None:
            obj.readme = readme.decoded
            dirty = True

    if dirty:
        obj.save()


@periodic_task(run_every=crontab(hour='*', minute='0', day_of_week='*'))
def sync_repositories():
    """Sync all repositories"""
    pass
