import graphene
import graphene_django
from .models import Ticket
from graphql_relay.node.node import to_global_id


class MapPosition(graphene.ObjectType):
    lat = graphene.Float()
    long = graphene.Float()


class TicketType(graphene_django.DjangoObjectType):
    map_position = graphene.Field(MapPosition)

    class Meta:
        model = Ticket

    def resolve_id(self, info):
        return to_global_id(self.__class__.__name__, self.id)

    def resolve_map_position(self, info):
        return MapPosition(lat=float(self.map_position.latitude), long=float(self.map_position.longitude))


class Query:
    tickets = graphene.List(TicketType)

    def resolve_tickets(self, info):
        return Ticket.objects.all()
