from graphene import Field
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
import graphene
from graphql_relay.node.node import to_global_id, from_global_id
from graphene_django.forms.mutation import DjangoModelFormMutation

UserModel = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel

    def resolve_id(self, info):
        print(info)
        return to_global_id(self.__class__.__name__, self.id)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return UserModel.objects.all()


class UserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        username = graphene.String()
        id = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    def mutate(self, info, id, username):
        print(info)
        print(from_global_id(id))
        user = UserModel.objects.get(pk=from_global_id(id)[1])
        user.username = username
        user.save()
        # Notice we return an instance of this mutation
        return UserMutation(user=user)


class Mutation(graphene.ObjectType):
    update_user = UserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
