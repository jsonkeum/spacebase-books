# Generated by Django 3.0.3 on 2020-02-14 23:06

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0003_auto_20200214_1445"),
    ]

    operations = [
        migrations.RemoveField(model_name="book", name="times_read",),
        migrations.AddField(
            model_name="book",
            name="users",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
