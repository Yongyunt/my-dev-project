from django.db import models
from django.utils.translation import gettext as _, gettext_lazy as _


class CashSale(models.Model):
    cash_sale_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Cash Sale #{self.date}{self.id} | {self.total_amount} บาท | {self.payment_method}"

    class Meta:
        db_table = 'cash_sale'
        verbose_name = _("การขายเงินสด")
        verbose_name_plural = _("Cash Sales")

class Customer(models.Model):
    name = models.CharField(max_length=255)                            # ชื่อลูกค้า
    phone = models.CharField(max_length=20, blank=True, null=True) 
    address = models.TextField(blank=True, null=True)     

    def __str__(self):
        return f"{self.name}({self.address})" 

    class Meta:
        db_table = 'customer'

class Quotation(models.Model):
    STATUS_CHOICES = [
        ('draft', _('แบบร่าง')),
        ('sent', _('ส่งแล้ว')),
        ('revised', _('ปรับแก้ไข')),
        ('approved', _('ลูกค้าอนุมัติ')),
        ('rejected', _('ลูกค้าปฏิเสธ')),
        ('cancelled', _('ยกเลิก')),
        ('converted', _('แปลงเป็นใบแจ้งหนี้')),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="quotations")
    quotation_date = models.DateField(verbose_name=_("วันที่เสนอราคา"))
    total_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name=_("จำนวนเงินรวม")
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name=_("รออนุมัติ")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("วันที่สร้าง"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("วันที่อัปเดต"))

    class Meta:
        db_table = 'quotation'
        verbose_name = _("ใบเสนอราคา")
        verbose_name_plural = _("quotations")

    def __str__(self):
        customer_name = getattr(self.customer, 'name', _("ไม่ระบุชื่อ"))
        return f"ใบเสนอราคา #{self.id} (Customer: {customer_name})"
    
class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name=_("สินค้า"))
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock_quantity = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True, verbose_name=_("รหัสสินค้า")) #รหัสสินค้าแบบไม่ซ้ำ


    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

class Meta:
    db_table = 'product'
    ordering = ['name']

def __str__(self):
    return f"{self.name} ({self.sku})"

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("ชื่อหมวดหมู่"))
    parent_category = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="subcategories",
        verbose_name=_("หมวดหมู่หลัก")
    )

    def __str__(self):
        return f"{self.name} (Parent: {self.parent_category.name if self.parent_category else 'None'})"

    class Meta:
        db_table = 'category'
        verbose_name = _("หมวดหมู่สินค้า")
        verbose_name_plural = _("categories")



class Invoice(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    PAYMENT_STATUS_CHOICES = [
        ('draft', _('แบบร่าง')),
        ('sent', _('ส่งแล้ว')),                   # ส่งใบแจ้งหนี้ให้ลูกค้าแล้ว
        ('partial', _('ชำระบางส่วน')),            # ลูกค้าจ่ายมาแล้วบางส่วน
        ('paid', _('ชำระแล้วทั้งหมด')),           # ลูกค้าชำระครบแล้ว
        ('shipped', _('จัดส่งแล้ว')),
        ('cancelled', _('ยกเลิก')),
        ('pending', _('รอดำเนินการ')),           # สถานะรอดำเนินการ
    ]
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="รอดำเนินการ"
    )
    # products = models.ManyToManyField(
    #     Product, 
    #     through='InvoiceProduct', 
    #     related_name='invoices', 
    #     verbose_name=_("สินค้าในใบแจ้งหนี้")
    # )
    # products = models.ManyToManyField(Product, through='InvoiceProduct')

    # PAYMENT_METHOD_CHOICES = [
    #     ('cash', 'เงินสด'),
    #     ('credit', 'บัตรเครดิต'),
    #     ('bank_transfer', 'โอนผ่านธนาคาร'),
    # ]

    # payment_method = models.CharField(
    #     max_length=50,
    #     choices=PAYMENT_METHOD_CHOICES,
    #     default='cash',
    #     verbose_name=_("วิธีการชำระเงิน (Payment Method)")
    # )

    def __str__(self):
        customer_name = getattr(self.customer, 'name', _("ไม่ระบุชื่อ"))
        return f"Invoice #{self.id} | {customer_name} | {self.total_amount} บาท | {self.payment_status}"

    class Meta:
        db_table = 'invoice'
        verbose_name = _("ใบแจ้งหนี้")
        verbose_name_plural = _("Invoices")




# class QuotationProduct(models.Model): 
#     quotation = models.ForeignKey('Quotation', on_delete=models.CASCADE)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     subtotal = models.DecimalField(max_digits=12, decimal_places=2)

#     class Meta:
#         db_table = 'quotation_item'
#         unique_together = ('quotation', 'product')  # ป้องกันไม่ให้มีสินค้าเดียวกันซ้ำในใบเสนอราคาเดียวกัน

#     def __str__(self):
#         return f"{self.product.name} x {self.quantity} (Quotation #{self.quotation.id})"
    
# class QuotationProduct(models.Model):
#     quotation = models.ForeignKey(
#         'Quotation',
#         on_delete=models.CASCADE,
#         related_name='quotation_products',
#         verbose_name="ใบเสนอราคา"
#     )
#     product = models.ForeignKey(
#         'Product',
#         on_delete=models.CASCADE,
#         verbose_name="สินค้า"
#     )
#     quantity = models.PositiveIntegerField(
#         verbose_name="จำนวน",
#         validators=[MinValueValidator(1)],
#         default=1
#     )
#     unit_price = models.DecimalField(
#         max_digits=10,
#         decimal_places=2,
#         validators=[MinValueValidator(0.01)],
#         verbose_name="ราคาต่อหน่วย"
#     )
#     subtotal = models.DecimalField(
#         max_digits=12,
#         decimal_places=2,
#         verbose_name="รวมเป็นเงิน",
#         editable=False
#     )
#     class Meta:
#         db_table = 'quotation_item'
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['quotation', 'product'],
#                 name='unique_quotation_product'
#             ),
#             models.CheckConstraint(
#                 check=models.Q(subtotal=models.F('quantity') * models.F('unit_price')),
#                 name='check_subtotal_correctness'
#             )
#         ]
#         ordering = ['id']

#     def __str__(self):
#         product_name = getattr(self.product, 'name', _("ไม่ระบุสินค้า"))
#         from decimal import Decimal                                         # Import Decimal for precise arithmetic
#         self.subtotal = Decimal(self.quantity) * Decimal(self.unit_price)  # คำนวณ subtotal โดยใช้ Decimal เพื่อความแม่นยำ
    
#     def save(self, *args, **kwargs):                                        # คำนวณ subtotal เมื่อบันทึกรายการ
#         self.subtotal = self.quantity * self.unit_price                     # คำนวณ subtotal โดยการคูณ quantity กับ unit_price 
#         super().save(*args, **kwargs)
    