# Generated by Django 5.0.2 on 2024-08-19 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0015_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='created_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='comment',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.novel'),
        ),
    ]
