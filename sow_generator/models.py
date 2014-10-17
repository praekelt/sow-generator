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
    business = models.TextField(null=True, editable=False)

    class Meta:
        verbose_name_plural = "Repositories"

    def __unicode__(self):
        if self.title:
            if self.description:
                return "%s - %s" % (self.title, self.description)
            else:
                return self.title
        return self.name

    @property
    def orgname(self):
        li = self.name.split("/")
        return li[0], li[1]

class AuthToken(models.Model):
    token = models.CharField(max_length=512, editable=False)

    def save(self, *args, **kwargs):
        self.id = 1
        super(AuthToken, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class AuthState(models.Model):
    state = models.CharField(max_length=512, editable=False)
