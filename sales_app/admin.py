from django.contrib import admin
from sales_app.models import Customer, Quotation, Product, Category,CashSale, Invoice

admin.site.register(Customer)
admin.site.register(Quotation)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CashSale)
admin.site.register(Invoice)