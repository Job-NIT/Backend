# Generated by Django 3.2.9 on 2022-01-15 18:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_project_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='budget',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]