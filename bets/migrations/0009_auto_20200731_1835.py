# Generated by Django 3.0 on 2020-07-31 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0008_auto_20200731_1833'),
    ]

    operations = [
        migrations.RenameField(
            model_name='openbet',
            old_name='datetime_scraped',
            new_name='datetime_bet',
        ),
    ]
