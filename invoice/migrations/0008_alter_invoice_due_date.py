# Generated by Django 3.2.1 on 2021-06-21 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_auto_20210621_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
