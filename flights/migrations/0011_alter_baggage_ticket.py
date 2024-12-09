# Generated by Django 4.2.7 on 2024-12-09 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0010_baggage_is_checkout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baggage',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='baggages', to='flights.ticket', unique=True),
        ),
    ]