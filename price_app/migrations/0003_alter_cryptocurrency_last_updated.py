# Generated by Django 5.1.3 on 2024-11-21 19:43

import price_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('price_app', '0002_alter_cryptocurrency_last_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='last_updated',
            field=models.DateTimeField(validators=[price_app.models.validate_past_date]),
        ),
    ]
