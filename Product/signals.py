from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from django_q.tasks import async_task
import logging
from .models import Ticket

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Ticket)
def schedule_winner_selection(sender, instance, created, **kwargs):
    if created:
        logger.info(f'Ticket {instance.id} created.')
        if instance.fully_purchased_at is not None:
            if instance.winner_drawn:
                logger.info(f'Winner already drawn manually for Ticket {instance.id}. Skipping automatic selection.')
                return

            current_time = timezone.now()
            run_at = instance.fully_purchased_at + timezone.timedelta(minutes=5)

            if current_time >= run_at:
                logger.info(f'Time has already passed for Ticket {instance.id}. Selecting winner now.')
                async_task('Product.tasks.check_and_select_winner', instance.id)
            else:
                logger.info(f'Scheduling winner selection for Ticket {instance.id} at {run_at}.')
                async_task('Product.tasks.check_and_select_winner', instance.id, schedule_type='O', next_run=run_at)
        else:
            logger.info(f'Ticket {instance.id} does not have fully_purchased_at set.')
    else:
        logger.info(f'Ticket {instance.id} updated.')
