# Generated by Django 4.1.7 on 2023-03-11 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_created_by_alter_eventattendee_event_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='capacity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='capacity'),
        ),
    ]
