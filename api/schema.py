# api/schema.py
import graphene

from api.query import Query
from api.mutation import Mutation
from api.types import RankType, RankModeType

# Schema 생성
schema = graphene.Schema(
  query=Query,
  mutation=Mutation,
  types=[
    RankType,
    RankModeType
  ],
  auto_camelcase=False
)