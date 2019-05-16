from django.shortcuts import render

from apartments.models import Apartment
from sellers.models import Seller


def sellers_list(request):
    # Information on all sellers
    context = {'sellers': Seller.objects.all().order_by('address')}
    return render(request, "sellers/sellers_list.html", context)

def seller_info(request, pk):
    # Information on individual sellers
    seller = Seller.objects.get(pk=pk)
    return render(request, 'sellers/seller_info.html', {
        'seller': seller,
        'apartments': Apartment.objects.filter(seller=seller, sold=False)
    })