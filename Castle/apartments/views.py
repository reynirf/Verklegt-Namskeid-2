from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Apartment

# Create your views here.

def home(request):
    context = {
        'newest': Apartment.objects.all().order_by('date_added')[:10]
    }
    return render(request, "apartments/home.html", context)

def apartment_list(request):
    all_apartments = Apartment.objects.all()
    context = {'apartments': all_apartments.order_by('address')}
    # if 'order_by' in request.GET:
    #     order_by = request.GET['order_by']
    #     print('order_by:', order_by)
    #     if order_by == 'Name A-Z':
    #         pass
    #     elif order_by == 'Name Z-A':
    #         context = {'apartments': all_apartments.order_by('-address')}
    #     elif order_by == 'Price from highest':
    #         context = {'apartments': all_apartments.order_by('price')}
    #     elif order_by == 'Price from lowest':
    #         context = {'apartments': all_apartments.order_by('-price')}

    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        #apartments = list(Apartment.objects.filter(address__icontains=search_filter).values())
        apartments = list(all_apartments.filter(address__icontains=search_filter).values())
        return JsonResponse({ 'data': apartments })
    return render(request, "apartments/apartment_list.html", context)

def apartment_info(request, pk):
    return render(request, 'apartments/apartment_info.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })

