from django.db import models
from django.conf import settings
from django.utils.text import slugify
from tinymce.models import HTMLField

from core.models import TimeStampedModel
from core.utils import unique_slugify


class Journal(TimeStampedModel):
    name = models.CharField(max_length=255, null=True, blank=True)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)

class JournalArticle(TimeStampedModel):
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE
    )
    year = models.IntegerField()
    url = models.URLField(max_length=255, null=True, blank=True)

class Review(TimeStampedModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, null=False, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = HTMLField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        return super().save(*args, **kwargs)