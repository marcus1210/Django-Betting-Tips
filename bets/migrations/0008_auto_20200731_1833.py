# Generated by Django 3.0 on 2020-07-31 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0007_auto_20200731_1715'),
    ]

    operations = [
        migrations.RenameField(
            model_name='openbet',
            old_name='datetime_bet',
            new_name='datetime_scraped',
        ),
    ]
