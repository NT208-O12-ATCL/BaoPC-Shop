# Generated by Django 4.2.5 on 2023-11-30 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('onlineshop', '0002_alter_product_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=255, null=True),
        ),
    ]