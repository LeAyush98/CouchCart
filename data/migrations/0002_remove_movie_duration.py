# Generated by Django 4.2.1 on 2023-05-26 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="movie",
            name="duration",
        ),
    ]
