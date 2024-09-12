# Generated by Django 5.0.2 on 2024-08-14 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0009_tag_novel_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='num_ratings',
        ),
        migrations.AlterField(
            model_name='novel',
            name='rating',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=3),
        ),
    ]
