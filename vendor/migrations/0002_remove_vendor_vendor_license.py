# Generated by Django 4.2.1 on 2023-07-22 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='vendor_license',
        ),
    ]