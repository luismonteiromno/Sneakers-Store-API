# Generated by Django 5.0.1 on 2024-01-20 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sneakers', '0012_adverts_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adverts',
            name='description',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Descrição do Anúncio'),
        ),
    ]