# Generated by Django 3.1.5 on 2021-05-19 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_auto_20210518_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_user_firstName',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_user_lastName',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
