# Generated by Django 5.0.2 on 2024-09-07 04:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0041_alter_novelcontent_content'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_at', models.DateTimeField(auto_now_add=True)),
                ('novel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novels.novel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'novel')},
            },
        ),
    ]
