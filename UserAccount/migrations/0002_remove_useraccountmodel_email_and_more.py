# Generated by Django 5.0 on 2024-05-15 18:57

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccountmodel',
            name='Email',
        ),
        migrations.AddField(
            model_name='useraccountmodel',
            name='Maximum_otp_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='useraccountmodel',
            name='Maximum_otp_try',
            field=models.CharField(default=3, max_length=2),
        ),
        migrations.AddField(
            model_name='useraccountmodel',
            name='Otp',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='useraccountmodel',
            name='Otp_expre_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useraccountmodel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('transaction_type', models.CharField(choices=[('deposit', 'DEPOSIT'), ('withdrawal', 'WITHDRAWAL')], max_length=10)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='UserAccount.wallet')),
            ],
        ),
    ]