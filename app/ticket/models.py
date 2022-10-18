from django.db import models
from django.db.models import Count, Case, When


class TicketQueryset(models.QuerySet):
    def close(self):
        return self.update(is_closed=True)

    def open(self):
        return self.update(is_closed=False)


class TicketManager(models.Manager):
    def get_queryset(self):
        return TicketQueryset(self.model, using=self._db)

    def closed(self):
        return self.filter(is_closed=True)

    def opened(self):
        return self.filter(is_closed=False)

    def close_tickets(self, tickets):
        return self.filter(id__in=tickets).close()

    def open_tickets(self, tickets):
        return self.filter(id__in=tickets).open()

    def count_closed_and_opened(self):
        return self.aggregate(
            closed=Count(Case(When(is_closed=True, then=1))),
            opened=Count(Case(When(is_closed=False, then=1))),
        )


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    is_closed = models.BooleanField(default=False)

    objects = TicketManager()
