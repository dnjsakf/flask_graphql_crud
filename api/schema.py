# api/schema.py
import graphene

from api.query import Query
from api.mutation import Mutation
from api.models import RankType

# Schema 생성
schema = graphene.Schema(
  query=Query,
  mutation=Mutation,
  types=[
    RankType
  ]
)