# Generated by Django 5.0 on 2024-05-10 10:42

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserAccount', '0003_remove_useraccountmodel_email_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('transaction_type', models.CharField(choices=[('deposite', 'DEPOSITE'), ('withdrawal', 'WITHDRAWAL')], max_length=10)),
                ('transaction_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='UserAccount.wallet')),
            ],
        ),
    ]