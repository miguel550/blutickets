import graphene
import graphene_django
from .models import Ticket
from graphql_relay.node.node import to_global_id


class TicketType(graphene_django.DjangoObjectType):
    class Meta:
        model = Ticket

    def resolve_id(self, info):
        return to_global_id(self.__class__.__name__, self.id)


class Query:
    tickets = graphene.List(TicketType)

    def resolve_tickets(self, info):
        return Ticket.objects.all()
