# Generated by Django 4.2.6 on 2023-10-10 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0002_customuser_referral_balance_customuser_referral_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referrer_code',
            field=models.CharField(blank=True, max_length=7, null=True),
        ),
    ]
