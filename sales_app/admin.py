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
    list_display = ('id','quotation_date', 'customer', 'total_amount' ,'status')
    search_fields = ('customer__name',)
    list_filter = ('status',)
    inlines = [QuotationItemInline]

class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'unit_price')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product':
            kwargs['queryset'] = Product.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # เมื่อบันทึกสินค้าใน quotation item ให้ดึงราคาจาก product
        if obj.product:
            obj.unit_price = obj.product.unit_price
        super().save_model(request, obj, form, change)

admin.site.register(QuotationItem, QuotationItemAdmin)

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

@admin.register(CashSale)
class CashSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'cash_sale_date', 'total_amount', 'payment_method')
    list_filter = ('payment_method',)

class CashSaleItemAdmin(admin.ModelAdmin):
    list_display = ('cash_sale', 'product', 'quantity', 'unit_price', 'subtotal')
    search_fields = ('cash_sale__id', 'product__name')
    list_filter = ('cash_sale', 'product')
    readonly_fields = ('subtotal',)
    
    def save_model(self, request, obj, form, change):
        # Automatically calculate the subtotal
        obj.subtotal = obj.quantity * obj.unit_price
        super().save_model(request, obj, form, change)

admin.site.register(CashSaleItem, CashSaleItemAdmin)


