# Generated by Django 3.2.5 on 2021-08-27 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='data_created',
            new_name='date_created',
        ),
    ]