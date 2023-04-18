from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from .models import Review

class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'
    template_name = 'reviews/review_detail.html'


class ReviewListView(ListView):
    model = Review
    context_object_name = 'review_list'
    template_name = 'reviews/review_list.html'
    queryset = (Review.objects.all()
                .exclude(active=False)
                .order_by('-created'))