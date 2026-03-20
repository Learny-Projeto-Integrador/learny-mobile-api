from api import mongo
from api.services.base_service import mongo_to_dict
        
def get_worlds():
    worlds = mongo.db.world_definitions.find()
    if worlds:
        worlds = mongo_to_dict(worlds)
        return worlds, 200
    else:
        return {"error": "Nenhum mundo encontrado no catálogo"}, 404
    
def get_world_phases(code):
    world = mongo.db.world_definitions.find_one({'code': code})
    if world:
        phases = world["phases"]
        return phases, 200
    else:
        return {"error": "Nenhum mundo encontrado com o código especificado"}, 404