# Generated by Django 5.0 on 2024-04-09 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0002_useraccountmodel_maximum_otp_out_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccountmodel',
            name='Email',
        ),
    ]