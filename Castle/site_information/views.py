from django.shortcuts import render
# Create your views here.

def site_information(request):
    return render(request, "site_information/about_us.html")