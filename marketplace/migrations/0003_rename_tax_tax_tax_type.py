# Generated by Django 4.2.1 on 2023-09-02 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_tax'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tax',
            old_name='tax',
            new_name='tax_type',
        ),
    ]
