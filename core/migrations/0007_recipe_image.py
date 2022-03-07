# Generated by Django 3.2.12 on 2022-03-07 14:38

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.FileField(null=True, upload_to=core.models.recipe_image_file_path),
        ),
    ]
