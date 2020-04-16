# api/query.py
import graphene

from graphene_mongo import MongoengineConnectionField

from api.models import RankModel, RankModeModel
from api.types import RankType, RankModeType

class InputSearchRank(graphene.InputObjectType):
  mode = graphene.String()
  name = graphene.String()
  score = graphene.Int()
  is_mobile = graphene.Boolean()


# Query Field 정의
class Query(graphene.ObjectType):
  ### Fields
  # 모드별 랭킹 목록
  modes_edges = MongoengineConnectionField(RankModeType)
  modes = graphene.List(
    RankModeType,
    mode=graphene.String(default_value="4x4")
  )
  
  # 전체 랭킹 목록
  ranks_edges = MongoengineConnectionField(RankType)
  ranks = graphene.List(
    RankType,
    page=graphene.Int(default_value=1),
    count_for_rows=graphene.Int(default_value=10),
    order=graphene.List(graphene.String),
    search=InputSearchRank()
  )
  
  # 특정 랭킹에 대한 정보
  rank = graphene.Field(RankType, id=graphene.String(required=True))
  
  
  ### Resolvers
  # 모드별 랭킹 목록
  def resolve_modes(parent, info, mode, **input):
    return RankModeModel.objects(mode=mode).all()

  # 전체 랭킹 목록
  def resolve_ranks(parent, info, page, count_for_rows, **kwargs):
    order = kwargs.get("order") if "order" in kwargs else list()
    search = kwargs.get("search") if "search" in kwargs else dict()
    
    page = page if page > 0 else 1
    count_for_rows = count_for_rows if count_for_rows > 0 else 10
    skip = (page-1) * count_for_rows
  
    model = RankModel.objects(**search).order_by(*order).skip(skip).limit(count_for_rows)
  
    return model
    
  # 특정 랭킹에 대한 정보
  def resolve_rank(parent, info, id):
    return RankModel.objects.get(id=id)
