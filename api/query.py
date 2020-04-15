# api/query.py
import graphene

from graphene import relay
from graphene_mongo import MongoengineConnectionField
from api.models import RankModel, RankType, RankNode

class InputSearchRank(graphene.InputObjectType):
  mode = graphene.String()
  name = graphene.String()
  score = graphene.Int()
  is_mobile = graphene.Boolean()


# Query Field 정의
class Query(graphene.ObjectType):
  # Connection Field
  rank_node = RankNode.Field()

  test = MongoengineConnectionField(RankType)

  def resolve_tests(root, info):
      return []

  # 모든 랭킹 목록.
  ranks = graphene.List(
    RankType,
    page=graphene.Int(default_value=1),
    count_for_rows=graphene.Int(default_value=10),
    order=graphene.List(graphene.String),
    search=InputSearchRank()
  )
  
  # 특정 랭킹에 대한 정보.
  rank = graphene.Field(RankType, id=graphene.String(required=True))
  
  # MongoDB에서 모든 랭킹 목록을 조회
  def resolve_ranks(parent, info, page, count_for_rows, **kwargs):
    order = kwargs.get("order") if "order" in kwargs else list()
    search = kwargs.get("search") if "search" in kwargs else dict()
    
    page = page if page > 0 else 1
    count_for_rows = count_for_rows if count_for_rows > 0 else 10
    skip = (page-1) * count_for_rows
  
    model = RankModel.objects(**search).order_by(*order).skip(skip).limit(count_for_rows)
  
    return model
    
  # MongoDB에서 특정 랭킹을 조회.
  def resolve_rank(parent, info, id):
    return RankModel.objects.get(id=id)