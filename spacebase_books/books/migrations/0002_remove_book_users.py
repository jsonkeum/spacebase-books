# Generated by Django 3.0.3 on 2020-02-17 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_reinitial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='users',
        ),
    ]
