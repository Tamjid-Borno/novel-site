# Generated by Django 5.0.2 on 2024-09-06 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0036_alter_novel_summary'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='novelcontent',
            unique_together={('novel', 'chapter_number')},
        ),
        migrations.AlterModelTable(
            name='novelcontent',
            table=None,
        ),
    ]
