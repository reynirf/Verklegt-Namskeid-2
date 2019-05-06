from django.shortcuts import render

# Create your views here.

def sellers_list(request):
    return render(request, "sellers/sellers_list.html")