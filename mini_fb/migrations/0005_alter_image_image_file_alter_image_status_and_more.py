# Generated by Django 5.1.2 on 2024-10-21 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0004_rename_article_image_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='image',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mini_fb.statusmessage'),
        ),
        migrations.AlterField(
            model_name='image',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]