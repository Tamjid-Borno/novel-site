# Generated by Django 5.0.2 on 2024-08-12 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0007_chapter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
