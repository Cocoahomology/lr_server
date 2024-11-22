import graphene
from .models import CryptoCurrency
from graphene_django import DjangoObjectType
from datetime import datetime
from .utils import convert_price_from_float_to_decimal


class CryptoCurrencyType(DjangoObjectType):
    class Meta:
        model = CryptoCurrency
        fields = "__all__"


class Query(graphene.ObjectType):
    cryptocurrencys = graphene.List(CryptoCurrencyType)

    def resolve_cryptocurrencys(self, info):
        return CryptoCurrency.objects.all()


# TODO: Mutation accepts a last_updated field.  If it is not provided, it defaults to the current time.
# Check that this meets the specifications.
# TODO: Mutation truncates the price to 8 decimal places.  Check that this meets the specifications.
class CreateCryptoCurrency(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        symbol = graphene.String(required=True)
        price = graphene.Float(required=True)
        last_updated = graphene.DateTime(required=False)

    cryptocurrency = graphene.Field(CryptoCurrencyType)

    def mutate(self, info, name, symbol, price, last_updated=None):
        if last_updated is None:
            last_updated = datetime.now()
        truncated_price = convert_price_from_float_to_decimal(price)
        cryptocurrency = CryptoCurrency(
            name=name, symbol=symbol, price=truncated_price, last_updated=last_updated
        )
        cryptocurrency.save()
        return CreateCryptoCurrency(cryptocurrency=cryptocurrency)


class Mutation(graphene.ObjectType):
    create_cryptocurrency = CreateCryptoCurrency.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
