from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
# from donate.models import DonateGoal


def index(request):
    return HttpResponse("dnt")

# class BookListView(ListView):
#     model = DonateGoal

#     def head(self, *args, **kwargs):
#         DonateGoal_s = self.get_queryset()
#         response = HttpResponse('')

#         return response