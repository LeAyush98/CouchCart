# Generated by Django 4.2.1 on 2023-05-27 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0004_alter_movie_synopsis"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="popularity",
            field=models.FloatField(default=5),
        ),
    ]
