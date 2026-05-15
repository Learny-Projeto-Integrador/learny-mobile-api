from api import mongo

def insert_world_definitions():
    worlds = [
        {
            "code": "WORLD_1",
            "name": "Dino's Forest",
            "picture": "https://pi-learny.s3.us-east-1.amazonaws.com/worlds/banners/world1.png",
            "description": "Floresta do Dino",
            "order": 1,
            "color": "#329F00",
        },
        {
            "code": "WORLD_2",
            "name": "Jigsaw World",
            "picture": "https://pi-learny.s3.us-east-1.amazonaws.com/worlds/banners/world2.png",
            "description": "Mundo quebra-cabeça",
            "order": 2,
            "color": "#25A6DE",
        },
        {
            "code": "WORLD_3",
            "name": "Space Realm",
            "picture": "https://pi-learny.s3.us-east-1.amazonaws.com/worlds/banners/world3.png",
            "description": "Reino Espacial",
            "order": 3,
            "color": "#B060C2",
        },
        {
            "code": "WORLD_4",
            "name": "Pop Party",
            "picture": "https://pi-learny.s3.us-east-1.amazonaws.com/worlds/banners/world4.png",
            "description": "Festa Pop",
            "order": 4,
            "color": "#B82A38",
        },
    ]

    for world in worlds:
        mongo.db.world_definitions.update_one(
            {"code": world["code"]},
            {"$setOnInsert": world},
            upsert=True
        )

def insert_module_definitions():
    modules = [
        {
            "code": "W1_MODULE_1",
            "worldCode": "WORLD_1", 
            "name": "Primeiro Módulo",
            "description": "Descrição do primeiro módulo",
            "order": 1,
        },
        {
            "code": "W1_MODULE_2",
            "worldCode": "WORLD_1", 
            "name": "Segundo Módulo",
            "description": "Descrição do primeiro módulo",
            "order": 2,
        },
        {
            "code": "W1_MODULE_3",
            "worldCode": "WORLD_1", 
            "name": "Terceiro Módulo",
            "description": "Descrição do terceiro módulo",
            "order": 3,
        },
    ]

    for module in modules:
        mongo.db.module_definitions.update_one(
            {"code": module["code"]},
            {"$setOnInsert": module},
            upsert=True
        )

def insert_phase_definitions():
    phases = [
        {
            "code": "W1_M1_PHASE_1",
            "moduleCode": "W1_MODULE_1", 
            "name": "Fase 1", 
            "order": 1, 
            "type": "common"
        },
        {
            "code": "W1_M1_PHASE_2",
            "moduleCode": "W1_MODULE_1", 
            "name": "Fase 2", 
            "order": 2, 
            "type": "common"
        },
        {
            "code": "W1_M1_PHASE_3",
            "moduleCode": "W1_MODULE_1", 
            "name": "Fase 3", 
            "order": 3, 
            "type": "common"
        },
        {
            "code": "W1_M1_PHASE_4",
            "moduleCode": "W1_MODULE_1", 
            "name": "Fase 4", 
            "order": 3, 
            "type": "boss"
        },
    ]

    for phase in phases:
        mongo.db.phase_definitions.update_one(
            {"code": phase["code"]},
            {"$setOnInsert": phase},
            upsert=True
        )

def insert_character_definitions():
    characters = [
        {
            "code": "ANGRYSSAUR",
            "name": "Angryssaur",
            "image": "https://pi-learny.s3.us-east-1.amazonaws.com/characters/angryssaur.png",
            "description": "Descrição do personagem Angryssaur",
            "unlockDescription": "Desbloqueado ao concluir a fase 01 do mundo 01",
            "moduleCode": "W1_MODULE_1"
        },
        {
            "code": "JOHNY_HERO",
            "name": "Johny Hero",
            "image": "https://pi-learny.s3.us-east-1.amazonaws.com/characters/johny-hero.png",
            "description": "Descrição do personagem Johny Hero",
            "unlockDescription": "Desbloqueado ao concluir a fase 01 do mundo 01",
            "moduleCode": "W1_MODULE_2"
        },
        {
            "code": "AYLIEN",
            "name": "Aylien",
            "image": "https://pi-learny.s3.us-east-1.amazonaws.com/characters/aylien.png",
            "description": "Descrição do personagem Aylien",
            "unlockDescription": "Desbloqueado ao concluir a fase 01 do mundo 01",
            "moduleCode": "W1_MODULE_3"
        },
        {
            "code": "RAYCOON",
            "name": "Raycoon",
            "image": "https://pi-learny.s3.us-east-1.amazonaws.com/characters/raycoon.png",
            "description": "Descrição do personagem Raycoon",
            "unlockDescription": "Desbloqueado ao concluir a fase 01 do mundo 01",
            "moduleCode": "W1_MODULE_3"
        },
    ]

    for character in characters:
        mongo.db.character_definitions.update_one(
            {"code": character["code"]},
            {"$setOnInsert": character},
            upsert=True
        )

def insert_mission_definitions():
    missions = [
        {
            "code": "COMPLETE_PHASE_1",
            "name": "Iniciando!",
            "description": "Conclua a fase 01",
            "worldCode": "WORLD_1",
        },
        {
            "code": "COMPLETE_3_PHASES",
            "name": "A todo o vapor!",
            "description": "Conclua 3 fases",
            "worldCode": "WORLD_1"
        },
        {
            "code": "COMPLETE_WORLD_1",
            "name": "Desvendando",
            "description": "Conclua o mundo 01",
            "worldCode": "WORLD_1"
        },
    ]

    for mission in missions:
        mongo.db.mission_definitions.update_one(
            {"code": mission["code"]},
            {"$setOnInsert": mission},
            upsert=True
        )

def insert_base_data():
    insert_world_definitions()
    insert_module_definitions()
    insert_phase_definitions()
    insert_character_definitions()
    insert_mission_definitions()
    



