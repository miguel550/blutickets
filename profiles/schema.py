from django.core.exceptions import PermissionDenied
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
import graphene
from graphql_relay.node.node import to_global_id, from_global_id

UserModel = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ("password",)

    def resolve_id(self, info):
        return to_global_id(self.__class__.__name__, self.id)


class Query:
    users = graphene.List(UserType)

    def resolve_users(self, info):
        if not info.context.user.is_authenticated:
            return UserModel.objects.none()
        return UserModel.objects.all()


class UserMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        username = graphene.String()
        id = graphene.ID(required=True)

    # The class attributes define the response of the mutation
    user = graphene.Field(UserType)

    def mutate(self, info, id, username):
        parsed_id = from_global_id(id)[1]
        if not info.context.user.id == parsed_id or not info.context.user.is_superuser:
            raise PermissionDenied('For this action you need to be the same user you are modifying or a superuser')

        user = UserModel.objects.get(pk=parsed_id)
        user.username = username
        user.save()
        # Notice we return an instance of this mutation
        return UserMutation(user=user)


class Mutation:
    update_user = UserMutation.Field()

