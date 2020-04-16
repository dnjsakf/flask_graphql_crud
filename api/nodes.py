# api/nodes.py
import graphene
from graphene import relay

from api.models import RankModel, RankModeModel

# Custom Node
class RankModeNode(relay.Node):
  class Meta:
    name = 'RankModeNode'
    
  mode = graphene.String()

  # Formating Node ID
  @staticmethod
  def to_global_id(_type, id):
    return f"{_type}:{id}"

  # Get Singgle Node Data
  @staticmethod
  def get_node_from_global_id(info, global_id, only_type=None):
    _type, id = global_id.split(":")

    if only_type:
      assert _type == only_type._meta.name, 'Received not compatible node.'
    return RankModeModel.objects(id=id).first()


# Custom Node
class RankNode(relay.Node):
  class Meta:
    name = 'RankNode'
    
  name = graphene.String()
  score = graphene.Int()

  # Formating Node ID
  @staticmethod
  def to_global_id(_type, id):
    return f"{_type}:{id}"

  # Get Singgle Node Data
  @staticmethod
  def get_node_from_global_id(info, global_id, only_type=None):
    _type, id = global_id.split(":")

    if only_type:
      assert _type == only_type._meta.name, 'Received not compatible node.'
    return RankModel.objects(id=id).first()
