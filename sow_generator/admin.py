import os

import requests
import pandoc

from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.middleware.csrf import _sanitize_token, _get_new_csrf_key
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import patterns
from django.contrib import messages
from django.utils import timezone
from django.conf import settings

from sow_generator.models import Repository, AuthToken, AuthState
from sow_generator import tasks
from sow_generator import DOCUMENTS
from sow_generator.forms import GenerateForm
from sow_generator.utils import unpack_document_by_key


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
    key = request.GET["document_key"]
    document, header, footer, repos = unpack_document_by_key(key)
    extra = {
        "document": document,
        "header": header,
        "footer": footer,
        "repos": repos,
        "form": GenerateForm(document_key=key, allowed_repos=repos)
    }
    return render_to_response(
        "admin/sow_generator/create_sow_two.html",
        extra,
        context_instance=RequestContext(request)
    )


@admin.site.register_view(
    "generate-sow",
    "_",
    urlname="sow-generator-generate-sow",
    visible=False,
)
def generate_sow(request):
    key = request.POST["document_key"]
    document, header, footer, repos = unpack_document_by_key(key)
    form = GenerateForm(request.POST, document_key=key, allowed_repos=repos)
    dc = form.is_valid()
    # Assemble a single concatenated markdown file
    md = "%s\n%s\n%s" % (
        header,
        "\n".join([r.readme_md for r in form.cleaned_data["repos"]]),
        footer
    )
    # Markdown needs to be converted, so pandoc
    doc = pandoc.Document()
    doc.markdown = md
    response = HttpResponse(
        doc.html,
        content_type="text/html",
    )
    filename = "Untitled %s scope of work - created %s.html" % (key, timezone.now().strftime("%Y-%m-%d %H:%M"))
    response["Content-Disposition"] = 'attachment; filename="%s"' % filename
    return response


admin.site.register(Repository, RepositoryAdmin)
