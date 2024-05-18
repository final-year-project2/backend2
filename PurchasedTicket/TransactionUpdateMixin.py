from UserAccount.models import Transaction
from django.utils import timezone

def TransactionUpdate(created,amount,transaction_from):
    transaction = Transaction(
            wallet=created,
            amount=amount,
            transaction_type='withdrawal',
            transaction_from = transaction_from,# Assuming deposit; change as needed
            transaction_date=timezone.now()  # Ensure timezone.now is imported
        )
    transaction.save()
