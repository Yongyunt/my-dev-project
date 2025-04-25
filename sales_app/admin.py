from django.contrib import admin
from sales_app.models import Customer, Quotation, Product, Category, CashSale, Invoice, QuotationItem, Receipt,InvoiceItem,CashSaleItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name','address','phone_number')
    search_fields = ('name',)


class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quotation_date','id', 'customer', 'total_amount' ,'status')
    search_fields = ('customer__name',)
    list_filter = ('status',)
    inlines = [QuotationItemInline]

@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'product', 'quantity', 'unit_price', 'subtotal')
    search_fields = ('quotation__id', 'product__name')

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


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
    list_display = ('invoice_date','id','customer', 'total_amount', 'payment_status')
    search_fields = ('customer__name',)
    list_filter = ('payment_status',)
    inlines = [InvoiceItemInline]

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'unit_price', 'subtotal')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_date','id', 'customer__name','total_amount', 'payment_method')
    list_filter = ('payment_method',)

admin.site.register(CashSale)
admin.site.register(CashSaleItem)


