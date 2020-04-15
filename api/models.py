# api/models.py
import datetime

from graphene import relay
from graphene_mongo import MongoengineObjectType

from mongoengine import Document
from mongoengine.fields import (
  StringField, BooleanField, IntField
)

# MongoDB Model
class RankModel(Document):
  meta = {'collection': 'game_ranking'}
  mode = StringField(description='2048 grame mode.')
  name = StringField()
  score = IntField()
  is_mobile = BooleanField()
  reg_dttm = StringField()
  upd_dttm = StringField()
    

class RankNode(relay.Node):
  class Meta:
    name = 'RankNode'

  @staticmethod
  def to_global_id(_type, id):
    return f"{_type}:{id}"

  @staticmethod
  def get_node_from_global_id(info, global_id, only_type=None):
    _type, id = global_id.split(":")

    if only_type:
      assert _type == only_type._meta.name, 'Received not compatible node.'

    return RankModel.objects(id=id).first()


# Schema Type
class RankType(MongoengineObjectType):
  class Meta:
    model = RankModel
    interfaces = (RankNode, )
  
  # reg_dttm을 출력할 때, 처리하는 로직
  def resolve_reg_dttm(parent, info, **kwargs):
    return datetime.datetime.strptime(parent.reg_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

  # upd_dttm을 출력할 때, 처리하는 로직
  def resolve_upd_dttm(parent, info, **kwargs):
    if parent.upd_dttm is not None:
      return datetime.datetime.strptime(parent.upd_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    else:
      return parent.upd_dttm