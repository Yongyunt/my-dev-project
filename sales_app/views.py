from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "index.html")

def quotations(request):
    return render(request, "quotations.html")

def products(request):
    return render(request, "products.html")

def contacts(request):
    return render(request, "contacts.html")
