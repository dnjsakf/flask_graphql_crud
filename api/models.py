# api/models.py
from mongoengine import Document
from mongoengine.fields import (
  StringField, IntField, BooleanField
)


class RankModeModel(Document):
  meta = {
    'collection': 'game_rank_modes'
  }
  mode = StringField(description='2048 grame mode.')
  reg_dttm = StringField()
  upd_dttm = StringField()


class RankModel(Document):
  meta = {
    'collection': 'game_ranking'
  }
  mode = StringField(description='2048 grame ranking.')
  name = StringField()
  score = IntField()
  is_mobile = BooleanField()
  reg_dttm = StringField()
  upd_dttm = StringField()

