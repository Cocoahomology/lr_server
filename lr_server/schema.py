import graphene

import price_app.schema


class Query(price_app.schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


class Mutation(price_app.schema.Mutation, graphene.ObjectType):
    # Combine the mutations from different apps
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
