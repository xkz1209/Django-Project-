# Generated by Django 5.1.2 on 2024-10-21 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0003_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='article',
            new_name='status',
        ),
    ]
