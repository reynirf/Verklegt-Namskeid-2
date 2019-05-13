from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from apartments.forms import ContactInfoForm
from users.models import Search_history
from .models import Apartment, Apartment_featured, Zipcode
from datetime import date
from django.core import serializers

# Create your views here.
def home(request):
    today = date.today()
    context = {
        'newest': Apartment.objects.all().order_by('date_added')[:10],
        'featured': Apartment_featured.objects.filter(start_date__lte=today, end_date__gte=today)
    }
    return render(request, "apartments/home.html", context)

def apartment_list(request):
    apartments = Apartment.objects.select_related().all().order_by('address')
    context = {'apartments': apartments.order_by('address')}
    search = dict()
    json = False
    home = False
    search['address'] = ''
    search['min_price'] = 20000000
    search['max_price'] = 90000000
    search['min_size'] = 40
    search['max_size'] = 250
    search['rooms'] = 'Rooms'
    search['zipcodes'] = ''

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

    if 'min_size' in request.GET and 'ma_size' in request.GET:
        min_size = request.GET['min_size']
        max_size = request.GET['max_size']
        apartments = apartments.filter(size__gte=min_size)
        apartments = apartments.filter(size__lte=max_size)
        json = True
        search['min_size'] = min_size
        search['max_size'] = max_size

    if 'rooms' in request.GET:
        amount_rooms = request.GET['rooms']
        if amount_rooms == 'Rooms':
            pass
        elif amount_rooms == '6':
            apartments = apartments.filter(rooms__gte=6)
        elif amount_rooms.isdigit():
            apartments = apartments.filter(rooms__exact=int(amount_rooms))
        search['rooms'] = amount_rooms

    if 'zipcodes' in request.GET:
        zipcodes = request.GET['zipcodes']
        print(zipcodes)
        if zipcodes != '':
            zipcodes_list = zipcodes.split(',')
            zipcodes_list = list(map(int, zipcodes_list))
            apartments = apartments.filter(zip_code__in=zipcodes_list)
            search['zipcodes'] = zipcodes

    if json and home:
        return render(request, "apartments/apartment_list.html", {'apartments': apartments, 'details': search})
    elif json:

        apartments = serializers.serialize('json', apartments, use_natural_foreign_keys = True, use_natural_primary_keys = True)
        return HttpResponse(apartments, content_type='application/json')

    context = {'apartments': apartments.order_by('address'), 'details': search}
    return render(request, "apartments/apartment_list.html", context)

def apartment_info(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.user.is_authenticated:
        if not request.user.user_info.seller:
            search = Search_history(user=request.user, apartment=apartment)
            search.save()
    return render(request, 'apartments/apartment_info.html', {
        'apartment': apartment
    })

@login_required
def buy_contact(request, pk):
    if request.method == 'POST':
        contact = ContactInfoForm(data=request.POST)
        if contact.is_valid():
            return render(request, 'apartments/buy_payment.html', {
                'apartment': get_object_or_404(Apartment, pk=pk)
            })
    return render(request, 'apartments/buy_contact.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })

@login_required
def buy_payment(request, pk):
    # if request.method == 'POST':
    #     contact = ContactInfoForm(data=request.POST)
    #     if contact.is_valid():
    return render(request, 'apartments/buy_payment.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })

@login_required
def buy_review(request, pk):
    return render(request, 'apartments/buy_review.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })