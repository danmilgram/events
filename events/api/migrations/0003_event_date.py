# Generated by Django 4.1 on 2022-08-23 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_event_room_user_participant_event_room"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2022, 8, 23, 13, 28, 29, 145815, tzinfo=datetime.timezone.utc
                ),
                unique=True,
            ),
        ),
    ]
