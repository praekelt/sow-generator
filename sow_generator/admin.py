import os

import yaml
import requests

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.middleware.csrf import _sanitize_token, _get_new_csrf_key
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import patterns
from django.contrib import messages
from django.conf import settings

from sow_generator.models import Repository, AuthToken, AuthState
from sow_generator import tasks
from sow_generator import DOCUMENTS


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "description", "_actions")
    search_fields = ("name", "title",)

    def _actions(self, obj):
        url = "/admin/ajax-sync-repository?id=%s" % obj.id
        return """<a href="%s">Sync now</a>""" % url
    _actions.short_description = "Actions"
    _actions.allow_tags = True


@admin.site.register_view(
    "ajax-sync-repository",
    "_",
    urlname="sow-generator-ajax-sync-repository",
    visible=False,
)
def ajax_sync_repository(request):
    id = request.GET["id"]
    tasks.sync_repository.delay(id=id)
    return HttpResponse("")


@admin.site.register_view(
    "get-auth-token",
    "Refresh Github auth token",
    urlname="sow-generator-get-auth-token"
)
def get_auth_token(request):
    """Retrieve an auth token for a user that can see all our repositories"""
    obj = AuthState.objects.create(state=_sanitize_token(_get_new_csrf_key()))
    url = "https://github.com/login/oauth/authorize"
    qs = "client_id=%s&scope=repo&state=%s" % (
        settings.SOW_GENERATOR["github-client-id"],
        obj.state
    )
    return HttpResponseRedirect(url + "?" + qs)


@admin.site.register_view(
    "get-auth-token-callback",
    "_",
    urlname="sow-get-auth-token-callback",
    visible=False,
)
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


@admin.site.register_view(
    "create-sow-one",
    "Create scope of work",
    urlname="sow-generator-create-sow-one"
)
def create_sow_one(request):
    extra = {"documents": DOCUMENTS}
    return render_to_response(
        "admin/sow_generator/create_sow_one.html",
        extra,
        context_instance=RequestContext(request)
    )


@admin.site.register_view(
    "create-sow-two",
    "_",
    urlname="sow-generator-create-sow-two",
    visible=False
)
def create_sow_two(request):
    document_key = request.GET["document_key"]
    document = DOCUMENTS[document_key]

    # Split template into parts
    # todo: regex for more leniency
    header, footer = document["template"].split(
        "<!--- modules - do not remove or alter this line -->"
    )

    repos = []
    modules = document.get("required_modules", []) \
        + document.get("optional_modules", [])
    for module in modules:
        try:
            repo = Repository.objects.get(name=module)
        except Repository.DoesNotExist:
            continue
        repos.append(repo)

    extra = {
        "document": document,
        "header": header,
        "footer": footer,
        "repos": repos
    }
    return render_to_response(
        "admin/sow_generator/create_sow_two.html",
        extra,
        context_instance=RequestContext(request)
    )


admin.site.register(Repository, RepositoryAdmin)
