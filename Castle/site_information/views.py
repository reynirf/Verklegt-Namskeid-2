from django.shortcuts import render
# Create your views here.

def about_us(request):
    return render(request, "site_information/about_us.html")

def contact_us(request):
    return render(request, "site_information/contact_us.html")
