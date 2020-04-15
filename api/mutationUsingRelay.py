# api/mutation.py
import datetime
import graphene
from api.models import RankModel, RankType

# Create Mutation 정의
class CreateRank(graphene.ClientIDMutation):  
  # 입력받을 파라미터 Field 정의
  class Input:
    mode = graphene.String(required=True)
    name = graphene.String(required=True)
    score = graphene.Int(required=True)
    is_mobile = graphene.Boolean(default_value=False) # 생량 가능

  # 반환 Field 정의
  rank = graphene.Field(RankType)
  success = graphene.Boolean()
  
  # 실행할 Mutation 정의
  @classmethod
  def mutate_and_get_payload(cls, root, info, **input):
    # MongoDB Model 생성
    model = RankModel(
      mode=input.get("mode"),
      name=input.get("name"),
      score=input.get("score"),
      is_mobile=input.get("is_mobile"),
      reg_dttm=datetime.datetime.now().strftime("%Y%m%d%H%M%S") # 현재시간
    )
    # MongoDB에 저장
    model.save()
    
    # 결과 반환
    return CreateRank(
      rank=model,
      success=True
    )
    
# Rank Input Data Fields
class InuptUpdateRankData(graphene.InputObjectType):
  score = graphene.Int()
  is_mobile = graphene.Boolean()
    
# Update Mutation 정의
class UpdateRank(graphene.ClientIDMutation):  
  # 입력받을 파라미터 Field 정의
  class Input:
    mode = graphene.String(required=True)
    name = graphene.String(required=True)
    data = InuptUpdateRankData(required=True)
    
  # 반환 Field 정의
  rank = graphene.Field(RankType)
  success = graphene.Boolean()

  # 실행할 Mutation 정의
  @classmethod
  def mutate_and_get_payload(cls, root, info, mode, name, data):
    # 수정할 MongoDB Model 조회
    model = RankModel.objects(
      mode=mode, 
      name=name
    ).first()
    
    # 입력받은 파라미터로 수정      
    if data.score is not None:
      model.score = data.score
    
    if data.is_mobile is not None:
      model.is_mobile = data.is_mobile
      
    model.upd_dttm = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
    # MongoDB에 저장
    model.save()
    
    # 결과 반환
    return UpdateRank(
      rank=model, 
      success=True
    )

    
# Delete Mutation 정의
class DeleteRank(graphene.ClientIDMutation):
  # 입력받을 파라미터 Field 정의
  class Input:
    mode = graphene.String(required=True)
    name = graphene.String(required=True)
    
  # 반환 Field 정의
  success = graphene.Boolean()

  @classmethod
  def mutate_and_get_payload(cls, root, info, mode, name):
    # MongoDB에서 삭제
    RankModel.objects(
      mode=mode, 
      name=name
    ).delete()
    
    # 삭제되었는지 확인
    success = RankModel.objects(
      mode=mode, 
      name=name
    ).first() == None
    
    # 결과 반환
    return DeleteRank(
      success=success
    )


# Using Relay
class UploadFile(graphene.ClientIDMutation):
  class Input:
    pass

  success = graphene.Boolean()

  @classmethod
  def mutate_and_get_payload(cls, root, info, **input):
    request = info.context

    # files = request.FILES

    return UploadFile(success=True)

# Mutation Field 정의
class MutationUsingRelay(graphene.ObjectType):
  create_rank = CreateRank.Field()
  update_rank = UpdateRank.Field()
  delete_rank = DeleteRank.Field()


'''
mutation {
	create_rank(
    input: {
      mode: "3x3"
      name: "dochi"
      score: 100
    }
  ){
    rank {
      id
      name
    }
  } 
	update_rank(
    input: {
      mode: "3x3"
      name: "dochi"
      data: {
        score: 1000
        is_mobile: false
      }
    }
  ){
    rank {
      id
      name
    }
  }
  delete_rank(
    input: {
      mode: "3x3"
      name: "dochi"
    }){
    success
  }
}
'''