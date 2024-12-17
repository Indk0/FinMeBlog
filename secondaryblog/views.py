from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def secondaryblog_me(request):
    return HttpResponse("This would be the another page for my blog")