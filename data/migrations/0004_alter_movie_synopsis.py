# Generated by Django 4.2.1 on 2023-05-27 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0003_alter_movie_synopsis"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="synopsis",
            field=models.CharField(max_length=800),
        ),
    ]
