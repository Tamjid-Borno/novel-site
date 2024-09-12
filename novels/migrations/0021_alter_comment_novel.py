# Generated by Django 5.0.2 on 2024-08-21 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0020_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='novel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='novels.novel'),
        ),
    ]
