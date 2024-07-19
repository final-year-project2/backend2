# Product/tasks.py
from django_q.tasks import async_task
from django.utils import timezone
from .models import Ticket, Winner
from .views import draw_winner
import logging

logger = logging.getLogger(__name__)

def check_and_select_winner(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        if ticket.fully_purchased_at is None:
            logger.info(f'Ticket {ticket.id} has no fully_purchased_at. Skipping winner selection.')
            return

        if ticket.winner_drawn:
            logger.info(f'Ticket {ticket.id} already has a winner drawn. Skipping winner selection.')
            return

        if timezone.now() >= ticket.fully_purchased_at + timezone.timedelta(minutes=5):
            if not Winner.objects.filter(ticket=ticket).exists():
                logger.info(f'Selecting winner for ticket {ticket.id}.')
                draw_winner(ticket.id)
            else:
                logger.info(f'Ticket {ticket.id} already has an associated winner.')
        else:
            # Reschedule the task to run at the appropriate time
            run_at = ticket.fully_purchased_at + timezone.timedelta(minutes=5)
            async_task('Product.tasks.check_and_select_winner', ticket.id, schedule_type='O', next_run=run_at)
            logger.info(f'Rescheduling winner selection for ticket {ticket.id} to {run_at}.')
    except Ticket.DoesNotExist:
        logger.error(f'Ticket with id {ticket_id} does not exist.')
