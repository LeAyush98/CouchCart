# Generated by Django 4.2.1 on 2023-05-27 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0002_remove_movie_duration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="synopsis",
            field=models.CharField(max_length=700),
        ),
    ]
