# Generated by Django 5.0.2 on 2024-08-14 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0011_novel_rating_count_alter_novel_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='novel',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
