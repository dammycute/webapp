# Generated by Django 4.2.7 on 2023-11-11 09:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0010_alter_otpmodel_otp_expire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpmodel',
            name='otp_expire',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 11, 11, 10, 1, 23, 494672, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]