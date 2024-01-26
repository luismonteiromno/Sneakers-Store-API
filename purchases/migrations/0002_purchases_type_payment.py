# Generated by Django 5.0.1 on 2024-01-22 00:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0001_initial'),
        ('type_payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='type_payment',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_type_payment', to='type_payments.typepayments', verbose_name='Tipo de pagamento'),
            preserve_default=False,
        ),
    ]