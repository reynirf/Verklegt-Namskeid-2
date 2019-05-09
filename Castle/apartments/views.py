from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Apartment

# Create your views here.

def home(request):
    return render(request, "apartments/home.html")

def apartment_list(request):
    apartments = Apartment.objects.all()
    context = {'apartments': apartments.order_by('address')}
    json = False

    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        apartments = apartments.filter(address__icontains=search_filter)
        json = True

    if 'min_price' in request.GET and 'max_price' in request.GET:
        price_min = request.GET['min_price']
        price_max = request.GET['max_price']
        apartments = apartments.filter(price__gte=price_min)
        apartments = apartments.filter(price__lte=price_max)
        json = True

    if 'min_size' in request.GET and 'max_size' in request.GET:
        min_size = request.GET['min_size']
        max_size = request.GET['max_size']
        apartments = apartments.filter(size__gte=min_size)
        apartments = apartments.filter(size__lte=max_size)
        json = True

    if json:
        return JsonResponse({'data': list(apartments.order_by('address').values()) })
    return render(request, "apartments/apartment_list.html", context)

def apartment_info(request, pk):
    return render(request, 'apartments/apartment_info.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })

