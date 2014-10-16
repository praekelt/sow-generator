from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from sow_generator import tasks


@staff_member_required
def ajax_sync_repository(self, id):
    tasks.sync_repository.delay(id=id)
    return HttpResponse("")
