from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
# from donate.models import DonateGoal


def index(request):
    return HttpResponse("""
    <!DOCTYPE html>
<html>
<head>
	<title></title>
</head>
<body>
<p>
	<a href="https://storage.cloud.google.com/snry_ue4/ue_d01.zip?hl=ru">ue_demo_01(280mb)</a>
</p>
</body>
</html>
    
    """)

# class BookListView(ListView):
#     model = DonateGoal

#     def head(self, *args, **kwargs):
#         DonateGoal_s = self.get_queryset()
#         response = HttpResponse('')

#         return response