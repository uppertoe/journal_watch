from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from . import models

class ReviewDetailView(DetailView):
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

class IssueDetailView(DetailView):
    pass


class IssueListView(ListView):
    pass


class TagListView(ListView):
    pass


class TagDetailView(DetailView):
    pass
