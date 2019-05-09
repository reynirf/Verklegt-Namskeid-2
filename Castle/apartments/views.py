from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Apartment

# Create your views here.

def home(request):
    return render(request, "apartments/home.html")

def apartment_list(request, context={'apartments': Apartment.objects.all().order_by('address')}):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        print(search_filter)
        apartments = list(Apartment.objects.filter(address__icontains=search_filter).values())
        print(apartments)
        return JsonResponse({ 'data': apartments })
    return render(request, "apartments/apartment_list.html", context)

def apartment_info(request, pk):
    return render(request, 'apartments/apartment_info.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })

