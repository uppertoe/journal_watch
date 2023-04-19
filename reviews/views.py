from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from . import models


class PageviewMixin():
    '''
    Calls obj.increment_pageview() and obj.save()
    '''
    def get_object(self):
        obj = super().get_object
        obj.increment_pageview()
        obj.save()
        return obj

class ReviewDetailView(PageviewMixin, DetailView):
    model = models.Review
    context_object_name = 'review'
    template_name = 'reviews/review_detail.html'


class ReviewListView(ListView):
    model = models.Review
    context_object_name = 'review_list'
    template_name = 'reviews/review_list.html'
    queryset = (models.Review.objects.all()
                .exclude(active=False)
                .order_by('-created'))

class IssueDetailView(PageviewMixin, DetailView):
    model = models.Issue
    context_object_name = 'issue'
    template_name = 'issues/issue_detail.html'


class IssueListView(ListView):
    model = models.Issue
    context_object_name = 'issue_list'
    template_name = 'issues/issue_list.html'
    queryset = (models.Issue.objects.all()
                .exclude(active=False)
                .order_by('-created'))


class TagListView(ListView):
    model = models.Tag
    context_object_name = 'tag_list'
    template_name = 'tags/tag_list.html'
    queryset = (models.Tag.objects.all()
                .exclude(active=False)
                .order_by('text'))


class TagDetailView(DetailView):
    model = models.Tag
    context_object_name = 'tag'
    template_name = 'tags/tag_detail.html'
