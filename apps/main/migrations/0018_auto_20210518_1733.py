# Generated by Django 3.1.5 on 2021-05-19 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20210518_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_user_firstName',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_user_lastName',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
