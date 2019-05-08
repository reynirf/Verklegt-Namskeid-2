from django.shortcuts import render
from apartments.models import Apartment

# Create your views here.

def home(request):
    return render(request, "apartments/home.html")

def apartment_list(request, context={'apartments': Apartment.objects.all().order_by('address')}):
    return render(request, "apartments/apartment_list.html", context)

def apartment_info(request, pk):
    apartment = Apartment.objects.get(pk=pk)
    return render(request, 'apartments/apartment_info.html', {
        'apartment': apartment
    })

