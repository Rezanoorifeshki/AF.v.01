# Generated by Django 5.1 on 2025-01-08 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afapp', '0016_product_flux_product_pol'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='photo', verbose_name='2عکس محصول'),
        ),
    ]
