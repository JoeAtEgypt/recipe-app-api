# Generated by Django 3.2.12 on 2022-03-04 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_ingrdient'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ingrdient',
            new_name='Ingredient',
        ),
    ]