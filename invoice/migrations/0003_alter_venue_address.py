# Generated by Django 3.2.1 on 2021-06-16 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_invoiceitem_package_venue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
