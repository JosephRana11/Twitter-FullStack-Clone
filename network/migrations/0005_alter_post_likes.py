# Generated by Django 5.0.1 on 2024-01-12 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
