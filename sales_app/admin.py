from django.contrib import admin
from sales_app.models import Customer, Quotation, Product, Category, CashSale, Invoice, QuotationItem, Receipt,InvoiceItem,CashSaleItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','address','phone_number')
    search_fields = ('name',)

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ['customer', 'id', 'quotation_date', 'total_amount', 'status_display']

    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'สถานะ'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock_quantity', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent_category')
    search_fields = ('name',)
    list_filter = ('parent_category',)

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer',  'invoice_date', 'total_amount', 'payment_status')
    search_fields = ('customer__name',)
    list_filter = ('payment_status',)
    inlines = [InvoiceItemInline]

admin.site.register(QuotationItem)
admin.site.register(CashSale)
admin.site.register(Receipt)
admin.site.register(InvoiceItem)
admin.site.register(CashSaleItem)


