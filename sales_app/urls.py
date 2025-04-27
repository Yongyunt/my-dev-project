from django.urls import path
from sales_app import views

urlpatterns = [
    path('', views.index),
    path('quotations', views.quotations),
    path('products', views.products),
    path('contacts', views.contacts)
]
