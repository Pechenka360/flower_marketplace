# Generated by Django 4.2.6 on 2023-11-05 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariation',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='productvariation',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество на складе'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
