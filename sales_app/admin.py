from django.contrib import admin
from sales_app.models import Customer, Quotation, Product, Category, CashSale, Invoice, QuotationItem, Receipt,InvoiceItem,CashSaleItem

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(QuotationItem)
admin.site.register(Category)
admin.site.register(CashSale)
admin.site.register(Invoice)
admin.site.register(Receipt)
admin.site.register(InvoiceItem)
admin.site.register(CashSaleItem)

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'quotation_date', 'total_amount', 'status_display']

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'สถานะ'
