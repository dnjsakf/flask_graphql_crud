# api/datdabase.py
from mongoengine import connect
from api.models import RankModel, RankModeModel

MONGO_DTATBASE="graphql-example"
MONGO_HOST="mongomock://localhost"

# Database 연결
conn = connect(MONGO_DTATBASE, host=MONGO_HOST, alias="default")
print( conn.server_info() )

# 기초 데이터 Insert 함수
def init_db():
  for idx in range(1, 5):
    RankModeModel(mode=f"{ idx }x{ idx }").save()
  
  for idx in range(1000):
    RankModel(
      name="heo", 
      mode="4x4", 
      score=idx, 
      is_mobile=False, 
      reg_dttm="20200413170848"
    ).save()