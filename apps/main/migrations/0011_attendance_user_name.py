# Generated by Django 3.1.5 on 2021-05-14 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_attendance_num_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='user_name',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
