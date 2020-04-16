# api/models.py
import datetime

from graphql_relay.utils import base64

from graphene import relay, Int, String, List
from graphene_mongo import MongoengineObjectType

from api.connections import CountableConnection
from api.models import RankModel, RankModeModel
from api.nodes import RankNode, RankModeNode
    

# Ranking Object
class RankType(MongoengineObjectType):
  class Meta:
    model = RankModel
    interfaces = (RankNode, )
    connection_class = CountableConnection
  
  # reg_dttm을 출력할 때, 처리하는 로직
  def resolve_reg_dttm(parent, info, **input):
    return datetime.datetime.strptime(parent.reg_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

  # upd_dttm을 출력할 때, 처리하는 로직
  def resolve_upd_dttm(parent, info, **input):
    if parent.upd_dttm is not None:
      return datetime.datetime.strptime(parent.upd_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    else:
      return parent.upd_dttm
      

# Ranking Object ---> Mode Object
class RankConnection(CountableConnection):
  class Meta:
    node = RankType


# Mode Object
class RankModeType(MongoengineObjectType):
  class Meta:
    model = RankModeModel
    interfaces = (RankModeNode, )
  
  ranking = relay.ConnectionField(
    RankConnection,
    page=Int(),
    count_for_rows=Int(),
    order=List(String)
  )
  
  @classmethod
  def resolve_ranking(cls, root, info, **input) -> RankConnection:    
    # Pagination
    page = input.get("page") if "page" in input else 1
    count_for_rows = input.get("count_for_rows") if "count_for_rows" in input else 10
    order = input.get("order") if "order" in input else list()
    skip = (page-1) * count_for_rows
    
    # Mongo Object Parse to Edge
    conn_type = cls.ranking.type
    node_name = conn_type._meta.node._meta.name
    datas = RankModel.objects(mode=root.mode).all()
    nodes = datas.order_by(*order).skip(skip).limit(count_for_rows)
    edges = [
      conn_type.Edge(
        node=node, 
        cursor=base64(f"{ node_name }:{ str(node.id) }")
      ) for node in nodes
    ]
    
    # Create new RankConnection Object
    return conn_type(
      edges=edges,
      page_info=relay.PageInfo(
        has_previous_page=True,
        has_next_page=True
      ),
      total_count=len(datas)
    )