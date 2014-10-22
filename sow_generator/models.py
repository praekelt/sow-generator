import pandoc

from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


class Repository(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        help_text="Eg. praekelt/jmbo-post"
    )
    title = models.CharField(max_length=256, null=True, editable=False)
    description = models.TextField(null=True, editable=False)
    readme = models.TextField(null=True, editable=False)
    readme_format = models.CharField(max_length=8, null=True, editable=False)
    business = models.TextField(null=True, editable=False)
    business_format = models.CharField(max_length=8, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Repositories"

    def __unicode__(self):
        if self.title:
            if self.description:
                return "%s - %s" % (self.title, self.description)
            else:
                return self.title
        return self.name

    def save(self, *args, **kwargs):
        # Prefix name with praekelt if organisation not supplied
        li = self.name.split("/")
        if len(li) == 1:
            self.name = "praekelt/%s" % self.name
        super(Repository, self).save(*args, **kwargs)

    @property
    def orgname(self):
        # Return name split into organisation and repo name
        li = self.name.split("/")
        if len(li) == 2:
            return li[0], li[1]
        else:
            return "praekelt", li[0]

    @property
    def readme_html(self):
        if not self.readme:
            return ""
        # todo: cache
        doc = pandoc.Document()
        if self.readme_format == "rst":
            doc.rst = self.readme
        elif self.readme_format == "md":
            doc.markdown = self.readme
        return doc.html


class AuthToken(models.Model):
    token = models.CharField(max_length=512, editable=False)

    def save(self, *args, **kwargs):
        self.id = 1
        super(AuthToken, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class AuthState(models.Model):
    state = models.CharField(max_length=512, editable=False)
