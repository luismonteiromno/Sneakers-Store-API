# Generated by Django 5.0.1 on 2024-02-19 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0004_purchases_employee_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='total_purchase',
            field=models.FloatField(default=0.0, verbose_name='Total da compra'),
        ),
    ]