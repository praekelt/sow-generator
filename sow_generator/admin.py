from django import forms
from django.contrib import admin
from django.core.urlresolvers import reverse

from sow_generator.models import Repository


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "description", "_actions")
    search_fields = ("url", "title",)


    def _actions(self, obj):
        url = reverse("sow-generator-ajax-sync-repository", args=[obj.id])
        return """<a href="%s">Sync now</a>""" % url
    _actions.short_description = "Actions"
    _actions.allow_tags = True


admin.site.register(Repository, RepositoryAdmin)
