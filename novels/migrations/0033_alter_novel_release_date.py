# Generated by Django 5.0.2 on 2024-09-06 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0032_alter_novel_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='release_date',
            field=models.DateField(),
        ),
    ]
