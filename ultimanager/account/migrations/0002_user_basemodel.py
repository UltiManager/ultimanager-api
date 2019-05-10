# Generated by Django 2.2.1 on 2019-05-10 12:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [("account", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                help_text="A unique identifier for the instance.",
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="time_created",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="The date and time of the object's creation.",
                verbose_name="creation time",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="time_updated",
            field=models.DateTimeField(
                auto_now=True,
                help_text=(
                    "The date and time of the last update made to the object."
                ),
                verbose_name="last update time",
            ),
        ),
    ]