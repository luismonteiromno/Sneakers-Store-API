# Generated by Django 5.0.1 on 2024-01-24 02:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0015_sneakers_stores'),
        ('store', '0003_store_delivery_store_maximum_delivery_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sneakers',
            name='stores',
        ),
        migrations.AddField(
            model_name='sneakers',
            name='stores',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='stores_sneakers', to='store.store', verbose_name='Lojas disponiveis'),
            preserve_default=False,
        ),
    ]