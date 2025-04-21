from django.contrib import admin
from sales_app.models import Customer, Quotation, Product, Category,CashSale, Invoice,QuotationItem

admin.site.register(Customer)
admin.site.register(Quotation)
admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku']
admin.site.register(QuotationItem)
admin.site.register(Category)
admin.site.register(CashSale)
admin.site.register(Invoice)