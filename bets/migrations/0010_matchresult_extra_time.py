# Generated by Django 3.0 on 2020-08-06 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0009_auto_20200731_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchresult',
            name='extra_time',
            field=models.BooleanField(default=False),
        ),
    ]
