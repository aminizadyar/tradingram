# Generated by Django 3.2.5 on 2021-08-14 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_delete_ticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='symbol',
            name='spread',
            field=models.FloatField(default=0.001),
        ),
    ]
