# api/datdabase.py
from mongoengine import connect
from api.models import RankModel

MONGO_DTATBASE="graphql-example"
MONGO_HOST="mongomock://localhost"

# Database 연결
conn = connect(MONGO_DTATBASE, host=MONGO_HOST, alias="default")

# 기초 데이터 Insert 함수
def init_db():
  for idx in range(10):
    rank = RankModel(name="heo", mode="4x4", score=2**idx, is_mobile=False, reg_dttm="20200413170848")
    rank.save() # Insert