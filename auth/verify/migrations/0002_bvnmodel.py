# Generated by Django 4.2.7 on 2023-11-11 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authApp', '0010_alter_otpmodel_otp_expire'),
        ('verify', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BvnModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_verified', models.BooleanField(default=False)),
                ('transaction_id', models.CharField(max_length=255)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authApp.customerdetails')),
            ],
        ),
    ]
