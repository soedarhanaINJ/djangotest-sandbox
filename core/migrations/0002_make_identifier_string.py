# Generated by Django 4.2.5 on 2023-10-09 21:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="backgroundtask",
            name="identifier",
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
