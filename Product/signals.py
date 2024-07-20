# from .models import Ticket, Winner  # Import Winner model
# from django_q.tasks import async_task
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.utils import timezone
# import logging

# logger = logging.getLogger(__name__)

# @receiver(post_save, sender=Ticket)
# def schedule_winner_selection(sender, instance, created, **kwargs):
#     if created and instance.fully_purchased_at is not None:
#         # Check if winner has already been drawn manually
#         if instance.winner_drawn:
#             logger.info(f'Winner already drawn manually for Ticket {instance.id}. Skipping automatic selection.')
#             return
        
#         run_at = instance.fully_purchased_at + timezone.timedelta(minutes=5)
#         logger.info(f'Scheduling winner selection for Ticket {instance.id} at {run_at}.')
#         async_task('Product.tasks.check_and_select_winner', instance.id, schedule_type='O', next_run=run_at)
