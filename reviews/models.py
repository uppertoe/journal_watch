import datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from tinymce.models import HTMLField
# Local apps
from core.models import TimeStampedModel
from core.utils import unique_slugify


class Journal(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, unique=True)
    abbreviation = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(TimeStampedModel):
    name = models.TextField()
    journal = models.ForeignKey(
        Journal,
        on_delete=models.CASCADE
    )
    year = models.IntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year + 1),
            ],
        default=datetime.date.today().year,
        )
    url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Review(TimeStampedModel):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name='reviews'
        )
    slug = models.SlugField(max_length=255, null=False, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    body = HTMLField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.article.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Review: ' + self.article.name


class Issue(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateField()
    slug = models.SlugField(max_length=255, null=False, unique=True)
    body = HTMLField()
    reviews = models.ManyToManyField(
        Review,
        blank=True,
        related_name='issues',
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(TimeStampedModel):
    body = models.TextField()
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
