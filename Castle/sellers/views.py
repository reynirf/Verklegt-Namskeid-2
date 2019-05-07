from django.shortcuts import render
from sellers.models import Seller

# Create your views here.

def sellers_list(request):
    context = {'sellers': Seller.objects.all().order_by('address')}
    return render(request, "sellers/sellers_list.html", context)