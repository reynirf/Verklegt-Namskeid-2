from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Apartment, Apartment_featured
from datetime import date

# Create your views here.

def home(request):
    today = date.today()
    context = {
        'newest': Apartment.objects.all().order_by('date_added')[:10],
        'featured': Apartment_featured.objects.filter(start_date__lte=today, end_date__gte=today)
    }
    return render(request, "apartments/home.html", context)

def apartment_list(request):
    apartments = Apartment.objects.all()
    context = {'apartments': apartments.order_by('address')}
    search = dict()
    json = False
    home = False

    if 'from_home' in request.GET:
        from_home = request.GET['from_home']
        if from_home == 'True' or from_home == 'true' or from_home == '1':
            home = True

    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        apartments = apartments.filter(address__icontains=search_filter)
        json = True
        search['address'] = search_filter

    if 'min_price' in request.GET and 'max_price' in request.GET:
        price_min = request.GET['min_price']
        price_max = request.GET['max_price']
        apartments = apartments.filter(price__gte=price_min)
        apartments = apartments.filter(price__lte=price_max)
        json = True
        search['min_price'] = price_min
        search['max_price'] = price_max

    if 'min_size' in request.GET and 'max_size' in request.GET:
        min_size = request.GET['min_size']
        max_size = request.GET['max_size']
        apartments = apartments.filter(size__gte=min_size)
        apartments = apartments.filter(size__lte=max_size)
        json = True
        search['min_size'] = min_size
        search['max_size'] = max_size

    if json and home:
        return render(request, "apartments/apartment_list.html", {'apartments': apartments, 'search_details': search})
    elif json:
        return JsonResponse({'data': list(apartments.order_by('address').values())})
    return render(request, "apartments/apartment_list.html", context)

def apartment_info(request, pk):
    return render(request, 'apartments/apartment_info.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })

