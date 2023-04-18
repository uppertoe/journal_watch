import datetime
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from tinymce.models import HTMLField
# Local apps
from core.models import TimeStampedModel
from core.utils import unique_slugify


class Tag(models.Model):
    text = models.CharField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
        )
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True)
    active = models.BooleanField(default=True)
    articles = models.ManyToManyField('Article', related_name='tags')
    
    def all_tags_list():
       tags = (Tag.objects.all()
                 .exclude(active=False)
                 .annotate(article_count=models.Count('articles'))
                 .order_by('-article_count')
                 .values_list('text', flat=True))
       return [str(tag) for tag in tags]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.text))
        return super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('tag-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.text


class Journal(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True)
    abbreviation = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(TimeStampedModel):
    name = models.TextField()
    tags_string = models.TextField(verbose_name='Add #hashtags that describe this article')
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

    def tags_list(self):
        '''
        Returns a list of unique 'hashtag' strings
        '''
        hashtag_list = []
        for word in self.text.split(' #'):
            if slugify(word):  # Ensure non-empty string after slugify
                hashtag_list.append(slugify(word[:255]))
        return list(set(hashtag_list))

    def create_tag_objects(self):
        '''
        Creates new Tag objects from the self.tags_string where these
        do not already exist
        '''
        for tag in self.tags_list():
            try:
                match = Tag.objects.get(name=tag)
            except Tag.DoesNotExist:
                new_tag = Tag(text=tag)
                new_tag.save()
                new_tag.articles.add(self)
                continue
            except Tag.MultipleObjectsReturned:
                print(f'Warning: multiple matching tags for {tag}')
                continue
            match.articles.add(self) #  Will not duplicate relation, but triggers signals

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
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    body = HTMLField()
    pageviews = models.IntegerField(default=0, blank=True, null=True)
    active = models.BooleanField(default=False)

    def increment_pageview(self):
        self.pageviews += 1
        return self.pageviews

    def get_absolute_url(self):
        reverse('review-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.article.name))
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'Review: ' + self.article.name


class Issue(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateField()
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True)
    body = HTMLField()
    reviews = models.ManyToManyField(
        Review,
        blank=True,
        related_name='issues',
        )
    pageviews = models.IntegerField(default=0, blank=True, null=True)
    active = models.BooleanField(default=False)

    def increment_pageview(self):
        self.pageviews += 1
        return self.pageviews

    def get_absolute_url(self):
        reverse('issue-detail', kwargs={'slug': self.slug})

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
        blank=True,
        null=True,
    )


