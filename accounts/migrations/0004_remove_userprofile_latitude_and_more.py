# Generated by Django 4.2.1 on 2023-09-03 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_userprofile_address_line_1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='longitude',
        ),
    ]
