# Generated by Django 5.2 on 2025-04-25 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_app', '0019_invoiceitem_subtotal_alter_invoiceitem_invoice_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales_app.customer'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receipts', to='sales_app.invoice'),
        ),
    ]
