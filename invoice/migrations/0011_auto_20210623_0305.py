# Generated by Django 3.2.1 on 2021-06-22 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0010_auto_20210622_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceitem',
            name='price',
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.IntegerField(),
        ),
    ]