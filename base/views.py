from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def dashboard(request):
    return render(request,'base/dashboard.html')
def about(request):
    return render(request,'base/about.html')
