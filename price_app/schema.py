import graphene
from graphene_django import DjangoObjectType

from .models import CryptoCurrency


class CryptoCurrencyType(DjangoObjectType):
    class Meta:
        model = CryptoCurrency
        fields = "__all__"


class Query(graphene.ObjectType):
    cryptocurrencys = graphene.List(CryptoCurrencyType)

    def resolve_cryptocurrencys(self, info):
        """
        The resolve_posts function is a resolver. It’s responsible for retrieving the posts from the database and returning them to GraphQL.

        :param self: Refer to the current instance of a class
        :param info: Pass along the context of the query
        :return: All post objects from the database
        """
        return CryptoCurrency.objects.all()


schema = graphene.Schema(query=Query)
