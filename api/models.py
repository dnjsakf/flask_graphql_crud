# api/models.py
import datetime

from mongoengine import Document
from mongoengine.fields import StringField, BooleanField, IntField

from graphene_mongo import MongoengineObjectType

# MongoDB Model
class RankModel(Document):
  meta = {'collection': 'game_ranking'}
  mode = StringField()
  name = StringField()
  score = IntField()
  is_mobile = BooleanField()
  reg_dttm = StringField()
  upd_dttm = StringField()
  

# Schema Type
class RankType(MongoengineObjectType):
  class Meta:
    model = RankModel
  
  # reg_dttm을 출력할 때, 처리하는 로직
  def resolve_reg_dttm(parent, info, **kwargs):
    return datetime.datetime.strptime(parent.reg_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")

  # upd_dttm을 출력할 때, 처리하는 로직
  def resolve_upd_dttm(parent, info, **kwargs):
    if parent.upd_dttm is not None:
      return datetime.datetime.strptime(parent.upd_dttm, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    else:
      return parent.upd_dttm
    