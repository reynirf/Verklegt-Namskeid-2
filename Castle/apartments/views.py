from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import datetime

from apartments.forms import ContactInfoForm, PaymentInfoForm
from sellers.models import Sales
from users.models import Search_history
from .models import Apartment, Apartment_featured, Zipcode, Apartment_images

class LazyEncoder(DjangoJSONEncoder):
    # Making sure JSON and the Zipcode table work together
    def default(self, obj):
        if isinstance(obj, Zipcode):
            return str(obj)
        return super().default(obj)


def home(request):
    today = datetime.date.today()
    # Finding the newest apartments and apartments that are featured today
    context = {
        'newest': Apartment.objects.filter(sold=False).order_by('-date_added')[:12],
        'featured': Apartment_featured.objects.filter(start_date__lte=today, end_date__gte=today)
    }
    return render(request, "apartments/home.html", context)

def apartment_list(request):
    # Finding all available apartments an ordering by address
    apartments = Apartment.objects.select_related().all().filter(sold=False).order_by('address')
    search = dict()
    json = False
    home = False
    # Setting initial search parameters
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

    # Filtering by given address
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        apartments = apartments.filter(address__icontains=search_filter)
        json = True
        search['address'] = search_filter

    # Filtering by given price range
    if 'min_price' in request.GET and 'max_price' in request.GET:
        price_min = request.GET['min_price']
        price_max = request.GET['max_price']
        apartments = apartments.filter(price__gte=price_min)
        apartments = apartments.filter(price__lte=price_max)
        json = True
        search['min_price'] = price_min
        search['max_price'] = price_max

    # Filtering by given size range
    if 'min_size' in request.GET and 'ma_size' in request.GET:
        min_size = request.GET['min_size']
        max_size = request.GET['max_size']
        apartments = apartments.filter(size__gte=min_size)
        apartments = apartments.filter(size__lte=max_size)
        json = True
        search['min_size'] = min_size
        search['max_size'] = max_size

    # Filtering by rooms selected
    if 'rooms' in request.GET:
        amount_rooms = request.GET['rooms']
        if amount_rooms == 'Rooms':
            pass
        elif amount_rooms == '6':
            apartments = apartments.filter(rooms__gte=6)
        elif amount_rooms.isdigit():
            apartments = apartments.filter(rooms__exact=int(amount_rooms))
        search['rooms'] = amount_rooms

    # Filtering by the zipcodes chosen
    if 'zipcodes' in request.GET:
        zipcodes = request.GET['zipcodes']
        if zipcodes != '':
            zipcodes_list = zipcodes.split(',')
            zipcodes_list = list(map(int, zipcodes_list))
            apartments = apartments.filter(zip_code__in=zipcodes_list)
            search['zipcodes'] = zipcodes

    # Loading the apartment list with all filters applied
    if json and home:
        return render(request, "apartments/apartment_list.html", {'apartments': apartments, 'details': search})
    elif json:
        apartments = serializers.serialize('json', apartments, cls=LazyEncoder, use_natural_foreign_keys = True)
        return HttpResponse(apartments, content_type='application/json')

    # Loading the apartment list with all default parameters
    context = {'apartments': apartments.order_by('address'), 'details': search}
    return render(request, "apartments/apartment_list.html", context)

def apartment_info(request, pk):
    # Getting information on a single aparment
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.user.is_authenticated:
        if not request.user.user_info.seller:
            # If user is logged in as a buyer:
            try:
                # Update search history for that apartment
                search_apt = Search_history.objects.get(apartment=pk, user=request.user.id)
                print(search_apt.search_date)
                search_apt.search_date = str(datetime.datetime.now())
                search_apt.save()
            except Search_history.DoesNotExist:
                # Or add to search history
                search = Search_history(user=request.user, apartment=apartment)
                search.save()
            except Search_history.MultipleObjectsReturned:
                pass

    return render(request, 'apartments/apartment_info.html', {
        'apartment': apartment
    })

# Buying apartment - contact information step
@login_required
def buy_contact(request, pk):
    if request.user.user_info.seller:
        # If user is a seller redirect to homepage
        return redirect('homepage')
    if request.method == 'POST':
        # When form is submitted save contact information to session and move to payment step
        contact = ContactInfoForm(data=request.POST)
        if contact.is_valid():
            request.session['contact'] = contact.cleaned_data
            return redirect('buy_payment', pk)
    try:
        # Getting information from session when moving between steps
        form = ContactInfoForm(data=request.session['contact'])
    except KeyError:
        form = ContactInfoForm()
    return render(request, 'apartments/buy_contact.html', {
        'pk': pk,
        'form': form
    })

# Buying apartment - payment information step
@login_required
def buy_payment(request, pk):
    if request.user.user_info.seller:
        # If user is a seller redirect to homepage
        return redirect('homepage')
    if request.method == 'POST':
        # When form is submitted save payment information to session and move to review step
        payment = PaymentInfoForm(data=request.POST)
        if payment.is_valid():
            request.session['payment'] = payment.cleaned_data
            return redirect('buy_review', pk)
    try:
        # Getting information from session when moving between steps
        form = PaymentInfoForm(data=request.session['payment'])
    except KeyError:
        form = PaymentInfoForm()
    return render(request, 'apartments/buy_payment.html', {
        'pk': pk,
        'form': form
    })

# Buying apartment - review step
@login_required
def buy_review(request, pk):
    if request.user.user_info.seller:
        # If user is a seller redirect to homepage
        return redirect('homepage')
    if request.method == 'POST':
        # save sale to database
        apartment = get_object_or_404(Apartment, pk=pk)
        sale = Sales(
            buyer=request.user.buyer,
            apartment=apartment,
            seller=apartment.seller,
            price=apartment.price)
        sale.save()
        # change apartment status to sold
        apartment.sold = True
        apartment.save(update_fields=['sold'])
        # remove extra images
        Apartment_images.objects.filter(apartment=apartment).delete()
        # remove from featured apartments and search history
        Apartment_featured.objects.filter(apartment=apartment).delete()
        Search_history.objects.filter(apartment=apartment).delete()
        return redirect('buy_success', pk)
    # If contact or payment information is missing, redirect to homepage
    try:
        contact = request.session['contact']
    except KeyError:
        return redirect('homepage')
    try:
        payment = request.session['payment']
    except KeyError:
        return redirect('homepage')

    # Send all information to html template
    return render(request, 'apartments/buy_review.html', {
        'pk': pk,
        'apartment': get_object_or_404(Apartment, pk=pk),
        'contact': request.session['contact'],
        'payment': request.session['payment']
    })

# Buying apartment - success
@login_required
def buy_success(request, pk):
    if request.user.user_info.seller:
        # If user is a seller redirect to homepage
        return redirect('homepage')
    return render(request, 'apartments/buy_success.html', {
        'apartment': get_object_or_404(Apartment, pk=pk)
    })

@login_required
def remove_apartment(request, pk):
    apartment = get_object_or_404(Apartment, pk=pk)
    if request.method == 'GET':
        if apartment:
            # Checking that the user is the seller of this apartment before deleting
            if request.user.seller.id == apartment.seller.id:
                apartment.delete()
                return redirect('profile')

    return render(request, 'apartments/apartment_info.html', {
        'apartment': apartment,
    })