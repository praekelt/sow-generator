import requests

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseRedirect
from django.middleware.csrf import _sanitize_token, _get_new_csrf_key
from django.contrib import messages
from django.conf import settings

from sow_generator.models import AuthToken, AuthState
from sow_generator import tasks


@staff_member_required
def ajax_sync_repository(request, id):
    tasks.sync_repository.delay(id=id)
    return HttpResponse("")


@staff_member_required
def get_auth_token(request):
    """Retrieve an auth token for a user that can see all our repositories"""
    obj = AuthState.objects.create(state=_sanitize_token(_get_new_csrf_key()))
    url = "https://github.com/login/oauth/authorize"
    qs = "client_id=%s&scope=repo&state=%s" % (
        settings.SOW_GENERATOR["github-client-id"],
        obj.state
    )
    return HttpResponseRedirect(url + "?" + qs)


@staff_member_required
def get_auth_token_callback(request):
    """Use return code to get an access token"""

    state = request.GET["state"]
    if not AuthState.objects.get(state=state):
        msg = "The system has received an invalid or expired state."
        messages.error(request, msg, fail_silently=True)
        return HttpResponseRedirect("/admin")

    r = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": settings.SOW_GENERATOR["github-client-id"],
            "client_secret": settings.SOW_GENERATOR["github-client-secret"],
            "code": request.GET["code"]
        },
        headers={"Accept": "application/json"}
    )
    token = r.json()["access_token"]
    AuthToken.objects.create(token=token)
    msg = "We have successfully retrieved an access token."
    messages.success(request, msg, fail_silently=True)
    return HttpResponseRedirect("/admin")
