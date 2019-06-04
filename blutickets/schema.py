import graphene
import profiles.schema
import tickets.schema


class Query(
    graphene.ObjectType,
    profiles.schema.Query,
    tickets.schema.Query
):
    pass


class Mutation(
    graphene.ObjectType,
    profiles.schema.Mutation
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
