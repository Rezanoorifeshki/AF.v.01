# Generated by Django 5.1 on 2024-12-25 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afapp', '0010_contactus'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold_count',
            field=models.IntegerField(default=0, verbose_name='تعداد فروش'),
        ),
    ]
