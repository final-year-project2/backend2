import logging
from django.utils import timezone
from django_q.tasks import async_task
from .models import Ticket, Winner
from .views import draw_winner

logger = logging.getLogger(__name__)

def check_and_select_winner(ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        logger.info(f'Checking ticket {ticket.id}.')

        if ticket.fully_purchased_at is None:
            logger.info(f'Ticket {ticket.id} has no fully_purchased_at. Skipping winner selection.')
            return

        if ticket.winner_drawn:
            logger.info(f'Ticket {ticket.id} already has a winner drawn. Skipping winner selection.')
            return

        current_time = timezone.now()
        run_at = ticket.fully_purchased_at + timezone.timedelta(minutes=5)

        if current_time >= run_at:
            if not Winner.objects.filter(ticket=ticket).exists():
                logger.info(f'Selecting winner for ticket {ticket.id}.')
                winner_ticket_number, winner_name = draw_winner(ticket.id)
                logger.info(f'Winner selected: Ticket {winner_ticket_number}, Name {winner_name}')
            else:
                logger.info(f'Ticket {ticket.id} already has an associated winner.')
        else:
            # Reschedule the task if it is not yet time
            async_task('Product.tasks.check_and_select_winner', ticket.id, schedule_type='O', next_run=run_at)
            logger.info(f'Rescheduling winner selection for ticket {ticket.id} to {run_at}.')
    except Ticket.DoesNotExist:
        logger.error(f'Ticket with id {ticket_id} does not exist.')
    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')
