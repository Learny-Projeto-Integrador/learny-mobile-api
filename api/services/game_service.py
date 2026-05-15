from api import mongo
from api.services.base_service import mongo_to_dict
        
def get_worlds():
    worlds = mongo.db.world_definitions.find()
    if worlds:
        worlds = mongo_to_dict(worlds)
        return worlds, 200
    else:
        return {"error": "Nenhum mundo encontrado no catálogo"}, 404
    
def get_world_info(code):
    world = mongo.db.world_definitions.find_one({'code': code}, {'_id': 0})

    if not world:
        return {"error": "Nenhum mundo encontrado com o código especificado"}, 404

    # Buscar módulos do mundo
    modules = list(
        mongo.db.module_definitions.find(
            {"worldCode": code},
            {"_id": 0}
        ).sort("order", 1)
    )

    module_codes = [m["code"] for m in modules]

    # Buscar todas as fases desses módulos
    phases = list(
        mongo.db.phase_definitions.find(
            {"moduleCode": {"$in": module_codes}},
            {"_id": 0}
        ).sort("order", 1)
    )

    # Agrupar fases por módulo
    phases_by_module = {}
    for phase in phases:
        module_code = phase["moduleCode"]
        phases_by_module.setdefault(module_code, []).append(phase)

    # Montar resposta final
    for module in modules:
        module["phases"] = phases_by_module.get(module["code"], [])

    world["modules"] = modules

    return world, 200

def get_characters():
    characters = mongo.db.character_definitions.find()
    if characters:
        characters = mongo_to_dict(characters)
        return characters, 200
    else:
        return {"error": "Nenhum personagem encontrado no catálogo"}, 404