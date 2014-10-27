from github3 import login
from github3.models import GitHubError

from celery import task
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from sow_generator.models import Repository, AuthToken

def _sync_repository(obj):
    dirty = False
    token = AuthToken.objects.get(id=1).token
    gh = login(token=token)
    dc = gh.user()
    org, name = obj.orgname
    repo = gh.repository(org, name)
    if repo is not None:
        # Find RST or MD files. Markdown takes precedence.
        for fieldname in ("readme", "sow"):
            v = repo.contents("%s.rst" % fieldname.upper())
            if v is not None:
                setattr(obj, fieldname, v.decoded)
                setattr(obj, "%s_format" % fieldname, "rst")
                dirty = True
            v = repo.contents("%s.md" % fieldname.upper())
            if v is not None:
                setattr(obj, fieldname, v.decoded)
                setattr(obj, "%s_format" % fieldname, "md")
                dirty = True

    if dirty:
        obj.save()


@task(max_retries=5)
def sync_repository(id):
    obj = Repository.objects.get(id=id)
    _sync_repository(obj)


@periodic_task(run_every=crontab(hour='*', minute='0', day_of_week='*'))
def sync_repositories():
    """Sync all repositories"""
    for obj in Repository.objects.all():
        _sync_repository(obj)
