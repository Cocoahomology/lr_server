import graphene

import price_app.schema


class Query(price_app.schema.Query, graphene.ObjectType):
    # Combine the queries from different apps
    pass


schema = graphene.Schema(query=Query)
