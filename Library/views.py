from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    msg=request.META
    return HttpResponse(msg)
